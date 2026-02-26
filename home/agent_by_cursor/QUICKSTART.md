# 🤝 Agent by Cursor + Team - 快速开始指南

## 📋 目录
- [安装指南](#安装指南)
- [快速启动](#快速启动)
- [核心功能演示](#核心功能演示)
- [团队协作](#团队协作)
- [配置说明](#配置说明)
- [使用技巧](#使用技巧)
- [常见问题](#常见问题)

---

## 🛠️ 安装指南

### 系统要求
- Python 3.10+
- 现代浏览器（Chrome/Firefox/Safari）
- 1GB+ 可用磁盘空间
- WebSocket支持

### 步骤1: 进入项目目录
```bash
cd /home/agent_by_cursor
```

### 步骤2: 创建虚拟环境（推荐）
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 步骤3: 安装依赖
```bash
# 安装所有依赖
pip install -r requirements.txt

# 开发依赖（可选）
pip install pytest pytest-asyncio pytest-cov mypy black flake8
```

### 步骤4: 配置环境
```bash
# 复制配置模板
cp .env.example .env

# 编辑.env文件
nano .env
```

### 步骤5: 验证安装
```bash
python3 -c "import openai, yaml; print('✅ 依赖安装成功')"
python3 -m src.main --validate-config
python3 -m pytest tests/ -v --collect-only
```

---

## 🚀 快速启动

### 方式1: 单机模式（Quick Start）

#### 最简单的启动方式：
```bash
# 创建本地测试题目
cat > local_test.yaml << EOF
name: "测试题目"
description: "Base64解码: SGVsbG8="
category: "crypto"
hint: "使用base64解码工具"
EOF

# 运行Agent
python3 -m src.main --challenge local_test.yaml
```

#### 交互模式：
```bash
python3 -m src.main --interactive
```

输入示例：
```
🎮 CTF Agent - 交互模式

📝 请输入题目描述:
> 这道题给了一串base64编码: SGVsbG8gQ1RG

🏷️ 题目分类 (crypto/web/pwn/reverse/forensics):
> crypto

🔑 提示 (可选，回车跳过):
> 

开始解题...

✅ 解题成功！
Flag: Hello CTF
工具: base64_decode
用时: 2.3秒
```

### 方式2: CTFd集成模式（团队协作）

#### 准备工作
```bash
# 1. 在CTFd中访问 Settings -> Access Tokens
# 2. 创建一个token

# 3. 配置.env文件
cat > .env << EOF
# CTFd配置
CTFD_BASE_URL=https://ctf.example.com
CTFD_TOKEN=your-ctfd-token-here

# LLM配置
OPENAI_API_KEY=sk-proj-your-openai-key

# 可选：Web服务端口
WEB_PORT=8000

# 可选：WebSocket端口
WS_PORT=8001
EOF
```

#### 启动团队模式
```bash
# 方式1: 自动解题模式
python3 -m src.main

# 方式2: 启动Web服务（支持团队协作）
python3 -m src.main --web-server

# 访问Web界面
open http://localhost:8000
```

### 方式3: 实时协作模式（WebSocket）

#### 启动WebSocket服务器
```bash
# 启动服务器
python3 -m src.main --websocket --listen 0.0.0.0:8001
```

#### 连接客户端
```python
# Python客户端示例
import asyncio
import websockets

async def connect_agent():
    uri = "ws://localhost:8001/ws"
    async with websockets.connect(uri) as websocket:
        # 发送题目
        await websocket.send(json.dumps({
            "type": "challenge",
            "description": "Base64: SGVsbG8=",
            "category": "crypto"
        }))
        
        # 接收结果
        response = await websocket.recv()
        result = json.loads(response)
        print(result['flag'])

asyncio.run(connect_agent())
```

#### JavaScript客户端示例
```javascript
// 浏览器中连接
const ws = new WebSocket('ws://localhost:8001/ws');

ws.onopen = () => {
    console.log('已连接到Agent服务器');
    
    // 发送题目
    ws.send(JSON.stringify({
        type: 'challenge',
        description: 'Base64: SGVsbG8=',
        category: 'crypto'
    }));
};

ws.onmessage = (event) => {
    const result = JSON.parse(event.data);
    console.log('Flag:', result.flag);
};
```

---

## 🎯 核心功能演示

### 1. 单题解答回顾

命令行：
```bash
python3 -m src.main --challenge example_challenge.yaml
```

输出：
```
[INFO] 加载题目: example_challenge.yaml
[INFO] 分类: crypto
[INFO] 开始思考...
[THOUGHT] 这是一个base64编码的题目
[THINKI] 我应该使用base64_decode工具
[ACTION] 调用工具: base64_decode("SGVsbG8=")
[RESULT] Hello
[THOUGHT] 结果看起来像是答案，格式正确
[FINAL] Flag: Hello
```

### 2. 批量处理

```bash
# 处理目录下所有题目
python3 -m src.main --batch ./challenges/ --output results.json

# 处理特定类别
python3 -m src.main --batch ./challenges/ --category crypto
python3 -m src.main --batch ./challenges/ --category web
```

### 3. 记忆查询

#### 查看所有已解决的题目
```bash
python3 src/cli_cli.py memory show
```

输出：
```
已解决的题目:

1. Base64 Demo (crypto)
   Flag: Hello
   工具: base64_decode
   时间: 2026-02-26 10:00:00

2. Caesar Cipher (crypto)
   Flag: World
   工具: caesar_decrypt
   时间: 2026-02-26 10:05:00
```

#### 搜索特定题目
```bash
python3 src/cli_cli.py memory show_challenge 1
```

#### 清空记忆
```bash
python3 src/cli_cli.py memory clear
```

### 4. 知识库管理

#### 搜索知识
```bash
python3 src/cli_cli.py knowledge search "Base64 解码"
```

输出：
```
找到 2 条相关知识:

1. Base64 解码方法
   解决方案: 使用base64_decode工具
   示例代码: base64_decode("SGVsbG8=")
   
2. Base64 编码检测
   解决方案: 检查字符串是否只包含Base64字符
   示例: if re.match(r'^[A-Za-z0-9+/]+=*$', s):
```

#### 添加知识
```bash
python3 src/cli_cli.py knowledge add << EOF
category: crypto
problem: 如何识别Base64编码
solution: 检查是否只包含A-Za-z0-9+/=
code: 
  if re.match(r'^[A-Za-z0-9+/]+=*$', s):
      return "可能是Base64"
EOF
```

### 5. 工具测试

#### 测试特定工具
```bash
python3 src/cli_cli.py tools test base64_decode
```

输出：
```
测试工具: base64_decode

输入: SGVsbG8=
输出: Hello
✅ 测试通过
```

#### 列出所有工具
```bash
python3 src/cli_cli.py tools list
```

输出：
```
可用工具列表:

Crypto工具:
  - base64_decode: Base64解码
  - rot13: ROT13编解码
  - xor_bruteforce: XOR暴力破解
  - caesar_decrypt: 凯撒密码
  - analyze_hash: 哈希分析

Web工具:
  - check_sqli: SQL注入检测
  - check_xss: XSS检测
  - parse_cookies: Cookie解析
  - analyze_jwt: JWT分析

Forensics工具:
  - extract_strings: 字符串提取
  - detect_filetype: 文件类型检测
  - binwalk_scan: Binwalk扫描
  - extract_metadata: 元数据提取
```

---

## 👥 团队协作

### 场景1: 多人协作解题

#### 架构
```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ 队员A    │     │ 队员B    │     │ 队员C    │
│ 浏览器   │     │ 浏览器   │     │ 浏览器   │
└────┬─────┘     └────┬─────┘     └────┬─────┘
     │                 │                 │
     └────────┬────────┴────────┬────────┘
              │                 │
      ┌───────▼─────────────────▼────────┐
      │   WebSocket Server (8001)        │
      │   Agent by Cursor + Team         │
      └────────────────┬─────────────────┘
                       │
              ┌────────▼────────┐
              │   CTFd平台      │
              │  (ctfd.example) │
              └─────────────────┘
```

#### 启动服务器
```bash
# 队员A启动服务器
python3 -m src.main --websocket --listen 0.0.0.0:8001
```

#### 队员B/C加入
```javascript
// 在浏览器控制台或客户端中连接
const ws = new WebSocket('ws://server-ip:8001/ws');

// 注册用户
ws.send(JSON.stringify({
    type: 'register',
    user_id: 'team_member_b'
}));

// 订阅更新
ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'challenges'
}));
```

### 场景2: 实时排行榜

#### WebSocket更新
```javascript
// 订阅排行榜
ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'leaderboard'
}));

// 接收实时更新
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.channel === 'leaderboard') {
        updateLeaderboard(data.leaderboard);
    }
});

function updateLeaderboard(data) {
    console.log('实时排行榜:');
    data.forEach((team, index) => {
        console.log(`${index + 1}. ${team.name}: ${team.score}分`);
    });
}
```

### 场景3: 共享解题状态

```javascript
// 发送当前进度
ws.send(JSON.stringify({
    type: 'progress',
    challenge_id: 'web_100',
    status: 'working',
    current_tool: 'base64_decode'
}));

// 接收队友进度
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'progress') {
        console.log(`${data.user} 正在解决 ${data.challenge_id}`);
        console.log(`当前工具: ${data.current_tool}`);
    }
};
```

---

## ⚙️ 配置说明

### 环境变量: .env

```bash
# ==================== LLM配置 ====================
OPENAI_API_KEY=sk-proj-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# 模型选择
OPENAI_MODEL=gpt-4-turbo-preview
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# ==================== CTFd配置 ====================
CTFD_BASE_URL=https://ctf.example.com
CTFD_TOKEN=your-ctfd-access-token
CTFD_AUTO_SUBMIT=true

# ==================== 服务器配置 ====================
WEB_HOST=0.0.0.0
WEB_PORT=8000
WS_PORT=8001

# ==================== 性能配置 ====================
MAX_ITERATIONS=10
TOOL_TIMEOUT=30
CONCURRENT_CHALLENGES=3

# ==================== 缓存配置 ====================
ENABLE_CACHE=true
CACHE_TTL=3600
CACHE_DIR=./cache

# ==================== 日志配置 ====================
LOG_LEVEL=INFO
LOG_FILE=./logs/agent.log
LOG_MAX_SIZE=10MB
LOG_BACKUP_COUNT=5

# ==================== Docker配置（可选）====================
DOCKER_ENABLED=false
DOCKER_IMAGE=ctf-tools:latest
DOCKER_TIMEOUT=300
```

### 配置文件: config.yaml

```yaml
# LLM配置
llm:
  provider: openai  # openai 或 anthropic
  model: gpt-4-turbo-preview
  api_key: ${OPENAI_API_KEY}  # 从环境变量读取
  temperature: 0.3
  max_tokens: 2000
  timeout: 120

# Solver配置
solver:
  max_iterations: ${MAX_ITERATIONS:-10}
  tool_timeout: ${TOOL_TIMEOUT:-30}
  concurrent_challenges: ${CONCURRENT_CHALLENGES:-3}
  enable_cache: ${ENABLE_CACHE:-true}

# 工具配置
tools:
  # Crypto工具
  crypto:
    base64_decode: true
    rot13: true
    xor_bruteforce: true
    caesar_decrypt: true
    
  # Web工具
  web:
    check_sqli: true
    check_xss: true
    analyze_jwt: true
    
  # Forensics工具
  forensics:
    extract_strings: true
    detect_filetype: true
    binwalk_scan: true
    
  # 是否使用外部工具
  external_tools:
    enable_pwntools: false  # 需要系统安装pwntools
    enable_ghidra: false   # 需要系统安装Ghidra

# CTFd配置
ctfd:
  base_url: ${CTFD_BASE_URL}
  token: ${CTFD_TOKEN}
  auto_submit: ${CTFD_AUTO_SUBMIT:-true}
  retry_on_fail: true
  min_score: 50  # 只解分值>=50的题目

# WebSocket服务器配置
websocket:
  enabled: true
  host: ${WEB_HOST:-0.0.0.0}
  port: ${WS_PORT:-8001}
  ping_interval: 30
  ping_timeout: 10

# 缓存配置
cache:
  enabled: ${ENABLE_CACHE:-true}
  ttl: ${CACHE_TTL:-3600}
  dir: ${CACHE_DIR:-./cache}

# 日志配置
logging:
  level: ${LOG_LEVEL:-INFO}
  file: ${LOG_FILE:-./logs/agent.log}
  max_size: ${LOG_MAX_SIZE:-10MB}
  backup_count: ${LOG_BACKUP_COUNT:-5}
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 记忆系统
memory:
  enabled: true
  file: ./memory/memory.db
  max_entries: 1000

# 知识库
knowledge:
  enabled: true
  file: ./knowledge/ctfknowledge.json
  auto_update: true
```

---

## 📊 使用技巧

### 技巧1: 性能优化

```yaml
# config.yaml
solver:
  # 增加并发数（需合理分配API调用）
  concurrent_challenges: 5
  
  # 减少最大尝试次数
  max_iterations: 5

llm:
  # 使用更便宜的模型
  model: gpt-3.5-turbo
```

### 技巧2: 节省API成本

```yaml
# 启用缓存
cache:
  enabled: true
  ttl: 7200  # 2小时

# 减少LLM调用
llm:
  max_tokens: 1500  # 减少输出token
```

### 技巧3: 自定义题目格式

```yaml
# custom_challenge.yaml
name: "自定义题目"
description: |
  题目描述：给了一串编码
  Data: U2FsdGVkX1+vupppZksvRf5pq5g5XjFRlipRkwB0K1Y=
  Hint: AES加密，需要密钥
category: crypto
difficulty: medium
files:
  - encrypted.bin
points: 100
tags:
  - crypto
  - aes
  - encryption
```

### 技巧4: 批量处理脚本

```bash
#!/bin/bash
# batch_process.sh

CHALLENGES_DIR=$1
 OUTPUT_DIR=$2

mkdir -p "$OUTPUT_DIR"

for file in "$CHALLENGES_DIR"/*.yaml; do
    echo "Processing: $file"
    python3 -m src.main --challenge "$file" --output "$OUTPUT_DIR/$(basename $file .yaml).json"
done

echo "Batch processing complete!"
```

使用：
```bash
chmod +x batch_process.sh
./batch_process.sh ./challenges/ ./results/
```

### 技巧5: 监控和调试

```bash
# 启用详细日志
export LOG_LEVEL=DEBUG
python3 -m src.main

# 监控内存
watch -n 1 'ps aux | grep python3 | grep Agent'

# 查看WebSocket连接
lsof -i :8001
```

---

## 🧪 测试

### 运行测试
```bash
# 安装测试依赖
pip install pytest pytest-asyncio pytest-cov

# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_crypto.py -v

# 生成覆盖率报告
pytest --cov=src --cov-report=html

# 查看覆盖率
open htmlcov/index.html
```

### 编写测试示例

```python
# tests/test_solver.py
import pytest
from src.solver.solver import Solver
from src.config import Config


def test_base64_challenge():
    """测试Base64题目"""
    solver = Solver(Config())
    
    challenge = {
        "description": "Base64: SGVsbG8=",
        "category": "crypto"
    }
    
    result = solver.solve(challenge)
    assert result is not None
    assert "Hello" in result.get("flag", "")


def test_invalid_challenge():
    """测试无效题目"""
    solver = Solver(Config())
    
    challenge = {
        "description": "无效题目",
        "category": "invalid"
    }
    
    result = solver.solve(challenge)
    assert result.get("status") == "failed"
```

---

## ❓ 常见问题

### Q1: CTFd连接失败？
```bash
# 检查网络
ping ctf.example.com

# 检查Token
curl -H "Authorization: Token YOUR_TOKEN" \
  https://ctf.example.com/api/v1/challenges

# 查看日志
tail -f logs/agent.log
```

### Q2: WebSocket连接断开？
```bash
# 增加重连间隔
config.yaml:
  websocket:
    ping_interval: 60  # 增加到60秒
    
# 或使用持久化连接
const ws = new WebSocket('ws://server:8001/ws');
ws.onclose = () => {
    setTimeout(() => connect(), 5000);  // 5秒后重连
};
```

### Q3: API使用成本高？
```yaml
# 使用更便宜的模型
llm:
  model: gpt-3.5-turbo  # 比 gpt-4 便宜 10倍

# 启用缓存
cache:
  enabled: true
  ttl: 86400  # 24小时

# 限制并发
solver:
  concurrent_challenges: 1
```

### Q4: 记忆占用太大？
```bash
# 清空记忆
python3 src/cli_cli.py memory clear

# 或限制记忆条目
memory:
  max_entries: 100  # 从1000减少到100
```

### Q5: 工具调用失败？
```bash
# 测试工具
python3 src/cli_cli.py tools test base64_decode

# 检查依赖
pip list | grep -i crypto

# 查看详细错误
LOG_LEVEL=DEBUG python3 -m src.main --challenge test.yaml
```

---

## 📚 更多资源

- [完整文档](README.md)
- [API文档](docs/API.md)
- [WebSocket协议](docs/WEBSOCKET_PROTOCOL.md)
- [团队最佳实践](docs/TEAM_BEST_PRACTICES.md)
- [示例代码](examples/)
- [贡献指南](CONTRIBUTING.md)

---

## 💡 最佳实践

### 团队协作
1. **明确分工** - 按题目类型分配（Crypto/Web/Pwn）
2. **实时沟通** - 使用WebSocket共享进度
3. **避免重复** - 共享记忆和知识库
4. **备份状态** - 定期导出memory

### 性能优化
1. **合理配置并发** - 根据API限制调整
2. **启用缓存** - 减少重复计算
3. **选择合适模型** - 平衡成本和速度
4. **监控资源** - 定期检查内存和日志

### 安全建议
1. **保护API密钥** - 使用环境变量
2. **限制访问** - WebSocket鉴权
3. **审计日志** - 定期审查操作记录
4. **备份重要数据** - memory和knowledge

---

**祝团队协作愉快！Flag Get! 🚩👥**
