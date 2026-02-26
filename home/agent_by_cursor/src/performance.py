"""
Agent by Cursor - 性能优化模块

优化策略:
1. 内存缓存 - 减少重复的LLM调用
2. 请求批处理 - 合并相似请求
3. 异步并发 - 多任务并行处理
4. 连接池 - 复用HTTP连接
5. 智能路由 - 根据负载选择API
"""

import time
import asyncio
import functools
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import hashlib
import json
from collections import OrderedDict
import threading


# ==================== LRU缓存 ====================

class LRUCache:
    """带TTL的LRU缓存"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.max_size = max_size
        self.ttl = ttl  # Time to live in seconds
        self.cache = OrderedDict()
        self.lock = threading.Lock()
    
    def _is_expired(self, entry) -> bool:
        """检查缓存是否过期"""
        return time.time() - entry['timestamp'] > self.ttl
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        with self.lock:
            if key not in self.cache:
                return None
            
            entry = self.cache[key]
            if self._is_expired(entry):
                del self.cache[key]
                return None
            
            # 更新访问顺序
            self.cache.move_to_end(key)
            return entry['value']
    
    def set(self, key: str, value: Any) -> None:
        """设置缓存"""
        with self.lock:
            # 如果已存在，删除旧值
            if key in self.cache:
                del self.cache[key]
            
            # 如果超过最大值，删除最旧的
            elif len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)
            
            self.cache[key] = {
                'value': value,
                'timestamp': time.time()
            }
    
    def clear(self) -> None:
        """清空缓存"""
        with self.lock:
            self.cache.clear()
    
    def size(self) -> int:
        """获取缓存大小"""
        return len(self.cache)


# ==================== 缓存装饰器 ====================

def cached(max_size: int = 100, ttl: int = 3600):
    """缓存函数结果"""
    
    def decorator(func):
        cache = LRUCache(max_size, ttl)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # 尝试从缓存获取
            result = cache.get(key)
            if result is not None:
                return result
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 存入缓存
            cache.set(key, result)
            
            return result
        
        wrapper.cache = cache  # 暴露缓存对象
        return wrapper
    
    return decorator


def async_cached(max_size: int = 100, ttl: int = 3600):
    """异步缓存函数结果"""
    
    def decorator(func):
        cache = LRUCache(max_size, ttl)
        
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # 尝试从缓存获取
            result = cache.get(key)
            if result is not None:
                return result
            
            # 执行异步函数
            result = await func(*args, **kwargs)
            
            # 存入缓存
            cache.set(key, result)
            
            return result
        
        wrapper.cache = cache
        return wrapper
    
    return decorator


# ==================== 批处理优化 ====================

class BatchProcessor:
    """批处理优化器 - 合并相似请求"""
    
    def __init__(self, batch_size: int = 10, batch_timeout: float = 0.5):
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.pending_requests = []
        self.lock = threading.Lock()
    
    def add_request(self, request_id: str, request_data: Any) -> asyncio.Future:
        """添加请求到批处理队列"""
        future = asyncio.Future()
        
        with self.lock:
            self.pending_requests.append({
                'id': request_id,
                'data': request_data,
                'future': future,
                'timestamp': time.time()
            })
            
            # 如果达到批处理大小，立即执行
            if len(self.pending_requests) >= self.batch_size:
                asyncio.create_task(self._process_batch())
        
        return future
    
    async def _process_batch(self):
        """处理一批请求"""
        with self.lock:
            requests = self.pending_requests[:self.batch_size]
            self.pending_requests = self.pending_sizes[self.batch_size:] if len(self.pending_requests) > self.batch_size else []
        
        if not requests:
            return
        
        try:
            # 批量处理请求
            results = await self._execute_batch([r['data'] for r in requests])
            
            # 设置所有future的结果
            for request, result in zip(requests, results):
                request['future'].set_result(result)
        
        except Exception as e:
            # 所有future都失败
            for request in requests:
                request['future'].set_exception(e)
    
    async def _execute_batch(self, requests: List[Any]) -> List[Any]:
        """执行批量请求逻辑"""
        # 子类实现具体的批处理逻辑
        raise NotImplementedError


class LLMBatchProcessor(BatchProcessor):
    """LLM请求批处理"""
    
    def __init__(self, batch_size: int = 10, batch_timeout: float = 0.5):
        super().__init__(batch_size, batch_timeout)
        self.llm_client = None  # 延迟初始化
    
    async def _execute_batch(self, requests: List[Dict]) -> List[Dict]:
        """批量执行LLM请求"""
        try:
            from src.llm.client import LLMClient
            
            if self.llm_client is None:
                self.llm_client = LLMClient(self._get_config())
            
            # 尝试批量API调用（如果支持）
            results = []
            for request in requests:
                result = await self.llm_client.chat(request['prompt'])
                results.append(result)
            
            return results
        
        except ImportError:
            # 回退到普通模式
            return [{"error": "LLM client not available"}] * len(requests)
    
    def _get_config(self):
        """获取LLM配置"""
        from src.config import Config
        return Config().llm


# ==================== 连接池优化 ====================

import aiohttp
from aiohttp import ClientSession, TCPConnector

class ConnectionPool:
    """HTTP连接池管理"""
    
    def __init__(self, max_connections: int = 100, max_per_host: int = 30):
        self.connector = TCPConnector(
            limit=max_connections,
            limit_per_host=max_per_host,
            enable_cleanup_closed=True,
            force_close=False,
            ttl_dns_cache=300,
            use_dns_cache=True
        )
        self.session: Optional[ClientSession] = None
        self.lock = asyncio.Lock()
    
    async def get_session(self) -> ClientSession:
        """获取或创建aiohttp会话"""
        async with self.lock:
            if self.session is None or self.session.closed:
                self.session = ClientSession(connector=self.connector)
            return self.session
    
    async def close(self):
        """关闭连接池"""
        async with self.lock:
            if self.session and not self.session.closed:
                await self.session.close()
                await self.connector.close()
                self.session = None


# 全局连接池实例
connection_pool = ConnectionPool()


# ==================== 性能监控 ====================

class PerformanceMonitor:
    """性能监控"""
    
    def __init__(self):
        self.metrics = {
            'llm_calls': 0,
            'llm_cache_hits': 0,
            'llm_cache_misses': 0,
            'total_time': 0,
            'avg_time': 0,
            'requests_processed': 0
        }
        self.lock = threading.Lock()
    
    def record_call(self, cached: bool, duration: float):
        """记录一次调用"""
        with self.lock:
            self.metrics['requests_processed'] += 1
            self.metrics['total_time'] += duration
            self.metrics['avg_time'] = (
                self.metrics['total_time'] / self.metrics['requests_processed']
            )
            
            if cached:
                self.metrics['llm_cache_hits'] += 1
            else:
                self.metrics['llm_calls'] += 1
                self.metrics['llm_cache_misses'] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        with self.lock:
            cache_hit_rate = 0
            if self.metrics['llm_cache_hits'] + self.metrics['llm_cache_misses'] > 0:
                cache_hit_rate = (
                    self.metrics['llm_cache_hits'] /
                    (self.metrics['llm_cache_hits'] + self.metrics['llm_cache_misses'])
                ) * 100
            
            return {
                **self.metrics,
                'cache_hit_rate': round(cache_hit_rate, 2)
            }
    
    def reset(self):
        """重置指标"""
        with self.lock:
            for key in self.metrics:
                if key != 'cache_hit_rate':
                    self.metrics[key] = 0


# 全局性能监控实例
perf_monitor = PerformanceMonitor()


# ==================== 智能路由 ====================

class LLMSmartRouter:
    """智能LLM路由 - 根据负载和成本选择最优API"""
    
    def __init__(self):
        self.providers = {
            'openai': {
                'model': 'gpt-4-turbo-preview',
                'cost_per_1k_tokens': 0.01,
                'speed': 1.0,
                'quality': 1.0,
                'capacity': 1000
            },
            'anthropic': {
                'model': 'claude-3-sonnet-20240229',
                'cost_per_1k_tokens': 0.003,
                'speed': 0.9,
                'quality': 0.95,
                'capacity': 2000
            }
        }
        self.current_load = {'openai': 0, 'anthropic': 0}
    
    def select_provider(self, task_complexity: str = 'medium') -> str:
        """根据任务复杂度和当前负载选择提供商"""
        current_time = datetime.now().hour
        
        # 高峰期优先选择容量大的提供商
        peak_hours = range(9, 18)  # 9AM - 6PM
        if current_time in peak_hours:
            return self._select_by_capacity()
        else:
            # 非高峰期优先考虑成本
            return self._select_by_cost(task_complexity)
    
    def _select_by_capacity(self) -> str:
        """根据容量选择"""
        return min(
            self.providers.keys(),
            key=lambda k: self.current_load.get(k, 0) / self.providers[k]['capacity']
        )
    
    def _select_by_cost(self, complexity: str) -> str:
        """根据成本和复杂度选择"""
        if complexity == 'high':
            # 高复杂度选择质量最高的
            return max(self.providers.keys(), key=lambda k: self.providers[k]['quality'])
        else:
            # 中低复杂度选择成本最低的
            return min(self.providers.keys(), key=lambda k: self.providers[k]['cost_per_1k_tokens'])
    
    def record_consumption(self, provider: str, tokens: int):
        """记录消费"""
        self.current_load[provider] += tokens


# 全局智能路由实例
smart_router = LLMSmartRouter()


# ==================== 工具函数 ====================

async def get_optimized_llm_response(prompt: str, complexity: str = 'medium'):
    """获取优化的LLM响应"""
    start_time = time.time()
    
    # 检查缓存
    cache_key = f"llm:{hashlib.md5(prompt.encode()).hexdigest()}"
    cached_result = lru_cache.get(cache_key)
    if cached_result:
        perf_monitor.record_call(cached=True, duration=time.time() - start_time)
        return cached_result
    
    # 选择最优提供商
    provider = smart_router.select_provider(complexity)
    
    # 调用LLM
    try:
        if provider == 'openai':
            result = await call_openai(prompt)
        else:
            result = await call_anthropic(prompt)
        
        # 缓存结果
        lru_cache.set(cache_key, result)
        
        perf_monitor.record_call(cached=False, duration=time.time() - start_time)
        return result
    
    except Exception as e:
        print(f"LLM调用失败: {e}")
        raise


async def call_openai(prompt: str) -> str:
    """调用OpenAI API"""
    response = await openai.ChatCompletion.acreate(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2000
    )
    return response.choices[0].message.content


async def call_anthropic(prompt: str) -> str:
    """调用Anthropic API"""
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


# ==================== 性能分析和建议 ====================

class PerformanceAnalyzer:
    """性能分析器"""
    
    @staticmethod
    def analyze_metrics(metrics: Dict[str, Any]) -> Dict[str, Any]:
        """分析性能指标并提供建议"""
        recommendations = []
        
        # 缓存命中率分析
        cache_hit_rate = metrics['cache_hit_rate']
        if cache_hit_rate < 30:
            recommendations.append({
                'type': 'warning',
                'message': f'缓存命中率较低 ({cache_hit_rate:.1f}%)',
                'suggestion': '考虑增加缓存TTL或调整缓存键策略'
            })
        elif cache_hit_rate > 80:
            recommendations.append({
                'type': 'info',
                'message': f'缓存命中率优秀 ({cache_hit_rate:.1f}%)',
                'suggestion': '缓存策略工作良好'
            })
        
        # 平均响应时间分析
        avg_time = metrics['avg_time']
        if avg_time > 5:
            recommendations.append({
                'type': 'warning',
                'message': f'平均响应时间较长 ({avg_time:.2f}s)',
                'suggestion': '考虑使用更快的模型或启用批处理'
            })
        
        # LLM调用次数分析
        llm_calls = metrics['llm_calls']
        if llm_calls > 1000:
            recommendations.append({
                'type': 'info',
                'message': f'LLM调用次数较多 ({llm_calls})',
                'suggestion': '考虑增加缓存或使用批处理以减少API调用'
            })
        
        return {
            'metrics': metrics,
            'recommendations': recommendations
        }


# 初始化全局LRU缓存
lru_cache = LRUCache(max_size=1000, ttl=3600)
