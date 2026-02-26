#!/usr/bin/env python3
"""
CTF Agent - Web Dashboard
实时监控和可视化CTF解题过程
"""

import sys
import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory
import json
from pathlib import Path
import threading

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ctf-agent-secret-key-2024')

# ==================== 数据模型 ====================

class DashboardData:
    """Dashboard数据管理"""
    
    def __init__(self):
        self.challenges = []
        self.solutions = []
        self.memory = {}
        self.knowledge_base = []
        self.stats = {
            'total_challenges': 0,
            'solved': 0,
            'failed': 0,
            'accuracy': 0,
            'avg_time': 0
        }
        self.load_data()
    
    def load_data(self):
        """加载历史数据"""
        # 加载记忆
        memory_file = Path('memory/enhanced.json')
        if memory_file.exists():
            try:
                with open(memory_file) as f:
                    self.memory = json.load(f)
            except:
                pass
        
        # 加载知识库
        kb_file = Path('knowledge/ctfknowledge.json')
        if kb_file.exists():
            try:
                with open(kb_file) as f:
                    self.knowledge_base = json.load(f)
            except:
                pass
        
        # 更新统计
        self.update_stats()
    
    def update_stats(self):
        """更新统计数据"""
        self.stats['total_challenges'] = len(self.memory)
        self.stats['solved'] = sum(1 for m in self.memory.values() if m.get('solved', False))
        self.stats['failed'] = sum(1 for m in self.memory.values() if not m.get('solved', True) and 'error' in m)
        
        if self.stats['total_challenges'] > 0:
            self.stats['accuracy'] = round(self.stats['solved'] / self.stats['total_challenges'] * 100, 2)
    
    def add_challenge(self, challenge):
        """添加挑战"""
        self.challenges.append({
            'id': len(self.challenges) + 1,
            'name': challenge.get('name', 'Unknown'),
            'category': challenge.get('category', 'misc'),
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        })
        self.stats['total_challenges'] = len(self.challenges)
    
    def update_challenge_status(self, challenge_id, status, result=None):
        """更新挑战状态"""
        for c in self.challenges:
            if c['id'] == challenge_id:
                c['status'] = status
                c['completed_at'] = datetime.now().isoformat()
                if result:
                    c['result'] = result
                break
        self.update_stats()

# 初始化数据
dashboard_data = DashboardData()

# ==================== 路由定义 ====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard页面"""
    return render_template('dashboard.html', data=dashboard_data.stats)

@app.route('/challenges')
def challenges():
    """挑战列表页面"""
    return render_template('challenges.html', challenges=dashboard_data.challenges)

@app.route('/memory')
def memory():
    """记忆页面"""
    return render_template('memory.html', memory=dashboard_data.memory)

@app.route('/knowledge')
def knowledge():
    """知识库页面"""
    return render_template('knowledge.html', kb=dashboard_data.knowledge_base)

# ==================== API 路由 ====================

@app.route('/api/stats')
def api_stats():
    """获取统计数据"""
    return jsonify({
        'success': True,
        'data': dashboard_data.stats
    })

@app.route('/api/challenges')
def api_challenges():
    """获取挑战列表"""
    return jsonify({
        'success': True,
        'data': dashboard_data.challenges
    })

@app.route('/api/challenge/<int:challenge_id>')
def api_challenge_detail(challenge_id):
    """获取挑战详情"""
    challenge = next((c for c in dashboard_data.challenges if c['id'] == challenge_id), None)
    if challenge:
        return jsonify({
            'success': True,
            'data': challenge
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Challenge not found'
        }), 404

@app.route('/api/memory')
def api_memory():
    """获取记忆数据"""
    return jsonify({
        'success': True,
        'data': dashboard_data.memory,
        'count': len(dashboard_data.memory)
    })

@app.route('/api/memory/search')
def api_memory_search():
    """搜索记忆"""
    query = request.args.get('q', '').lower()
    if not query:
        results = list(dashboard_data.memory.values())
    else:
        results = [
            m for m in dashboard_data.memory.values()
            if query in str(m).lower()
        ]
    
    return jsonify({
        'success': True,
        'data': results,
        'count': len(results)
    })

@app.route('/api/knowledge')
def api_knowledge():
    """获取知识库"""
    return jsonify({
        'success': True,
        'data': dashboard_data.knowledge_base,
        'count': len(dashboard_data.knowledge_base)
    })

@app.route('/api/knowledge/search')
def api_knowledge_search():
    """搜索知识库"""
    query = request.args.get('q', '').lower()
    if not query:
        results = dashboard_data.knowledge_base
    else:
        results = [
            k for k in dashboard_data.knowledge_base
            if query in str(k).lower()
        ]
    
    return jsonify({
        'success': True,
        'data': results,
        'count': len(results)
    })

@app.route('/api/solve', methods=['POST'])
def api_solve_challenge():
    """解决挑战"""
    data = request.json
    description = data.get('description', '')
    category = data.get('category', 'misc')
    
    # 模拟解决过程
    challenge_id = len(dashboard_data.challenges) + 1
    dashboard_data.add_challenge({
        'name': f'Challenge {challenge_id}',
        'category': category,
        'description': description
    })
    
    # 模拟异步解决
    def simulate_solve():
        import time
        time.sleep(2)  # 模拟解题时间
        
        # 模拟结果
        result = {
            'flag': 'flag{test_solution}',
            'tool': 'base64_decode',
            'time': 2.0
        }
        
        dashboard_data.update_challenge_status(challenge_id, 'completed', result)
    
    thread = threading.Thread(target=simulate_solve)
    thread.start()
    
    return jsonify({
        'success': True,
        'data': {
            'challenge_id': challenge_id,
            'status': 'solving',
            'message': '开始解题...'
        }
    })

@app.route('/api/tools')
def api_tools():
    """获取工具列表"""
    from tools.toolkit import ToolRegistry
    
    try:
        registry = ToolRegistry()
        tools = list(registry.tools.keys())
        return jsonify({
            'success': True,
            'data': tools,
            'count': len(tools)
        })
    except:
        return jsonify({
            'success': True,
            'data': ['base64_decode', 'rot13', 'xor_bruteforce', 'check_sqli', 'check_xss'],
            'count': 5
        })

# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# ==================== 主函数 ====================

if __name__ == '__main__':
    # 创建必要的目录
    templates_dir = Path('templates')
    static_dir = Path('static')
    data_dir = Path('data')
    
    templates_dir.mkdir(exist_ok=True)
    static_dir.mkdir(exist_ok=True)
    data_dir.mkdir(exist_ok=True)
    
    # 创建templates（如果不存在）
    if not (templates_dir / 'index.html').exists():
        print("Creating default templates...")
        with open(templates_dir / 'index.html', 'w') as f:
            f.write('''<!DOCTYPE html>
<html>
<head>
    <title>CTF Agent Dashboard</title>
</head>
<body>
    <h1>CTF Agent Dashboard</h1>
    <p>Welcome to CTF Agent Dashboard!</p>
    <ul>
        <li><a href="/dashboard">Dashboard</a></li>
        <li><a href="/challenges">Challenges</a></li>
        <li><a href="/memory">Memory</a></li>
        <li><a href="/knowledge">Knowledge Base</a></li>
    </ul>
</body>
</html>''')
    
    print("=" * 60)
    print("CTF Agent Web Dashboard")
    print("=" * 60)
    print(f"Starting server on http://0.0.0.0:5002")
    print(f"Templates: {templates_dir.absolute()}")
    print(f"Static: {static_dir.absolute()}")
    print(f"Data: {data_dir.absolute()}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5002, debug=True)
