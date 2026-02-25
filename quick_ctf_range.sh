#!/bin/bash
#
# 快速本地靶场 - 使用 Python + 已有环境
# 不需要下载大镜像，快速启动
#

echo "========================================"
echo "🚀 快速本地靶场部署"
echo "========================================"

# 1. DVWA (Docker - 已下载)
echo "1️⃣ 检查 DVWA..."
DVWA_RUNNING=$(docker ps --format '{{.Names}}' | grep dvwa)
if [ -n "$DVWA_RUNNING" ]; then
    echo "   ✅ DVWA 已运行: http://localhost:8081"
else
    echo "   ⚠️  DVWA 未运行，需要手动启动: bash /setup_ctf_range.sh"
fi

# 2. 使用 testphp.vulnweb.com (真实漏洞站点)
echo ""
echo "2️⃣ 在线靶场 (真实环境)"
echo "   ✅ DVWA 在线: http://testphp.vulnweb.com"
echo "   ✅ 可用于: SQLi, XSS 测试"

# 3. 检查本地 Python 靶场
echo ""
echo "3️⃣ 准备 Python 本地靶场..."

# 创建简单的 Web 靶场
mkdir -p /tmp/ctf_targets

# 创建 XSS 靶场
cat > /tmp/ctf_targets/xss_target.py << 'EOFPYTHON'
#!/usr/bin/env python3
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get('name', 'Guest')
    template = f"""
    <html>
    <head><title>XSS Target</title></head>
    <body>
    <h1>Hello, {name}!</h1>
    <p>Flag: flag{{xss_test_successful}}</p>
    </body>
    </html>
    """
    return render_template_string(template)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    return f"""
    <html>
    <body>
    <h1>Search Results</h1>
    <p>You searched for: {query}</p>
    <p>No results found.</p>
    <p>Flag: flag{{xss_reflected}}</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8087)
EOFPYTHON

# 创建 API 靶场
cat > /tmp/ctf_targets/api_target.py << 'EOFPYTHON'
#!/usr/bin/env python3
from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

# 模拟数据库
users = [
    {"id": 1, "username": "admin", "flag": "flag{sql_injection_works}"},
    {"id": 2, "username": "user", "flag": "flag{try_harder}"},
]

@app.route('/api/users')
def get_users():
    """SQL 注入靶场 - 简化版"""
    user_id = request.args.get('id', '1')

    try:
        # 简单模拟
        user_id_int = int(user_id)
        for user in users:
            if user['id'] == user_id_int:
                return jsonify({"status": "success", "user": user})

        return jsonify({"status": "error", "message": "User not found"})

    except ValueError:
        # 尝试 SQL 注入
        user_id = user_id.replace("'", "")
        user_id = user_id.replace(" ", "")

        return jsonify({
            "status": "error",
            "message": "Invalid ID",
            "hint": "Try UNION based injection"
        })

@app.route('/api/decode')
def decode_api():
    """Base64 解码靶场"""
    encoded = request.args.get('data', '')
    try:
        decoded = base64.b64decode(encoded).decode('utf-8')
        return jsonify({"status": "success", "decoded": decoded})
    except:
        return jsonify({"status": "error", "message": "Invalid base64"})

@app.route('/api/flag')
def get_flag():
    """简单 Flag 靶场"""
    return jsonify({
        "flag": "flag{api_target_success}",
        "message": "Congratulations!"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
EOFPYTHON

chmod +x /tmp/ctf_targets/*.py

echo "   ✅ 本地靶场已创建"
echo "   - XSS 靶场: http://localhost:8087"
echo "   - API 靶场: http://localhost:8088"

# 4. 启动本地靶场（后台）
echo ""
echo "4️⃣ 启动本地靶场..."

# 检查是否需要 Flask
python3 -c "import flask" 2>/dev/null
if [ $? -eq 0 ]; then
    # 检查是否已运行
    XSS_RUNNING=$(lsof -ti:8087 2>/dev/null)
    API_RUNNING=$(lsof -ti:8088 2>/dev/null)

    if [ -z "$XSS_RUNNING" ]; then
        python3 /tmp/ctf_targets/xss_target.py > /tmp/xss_target.log 2>&1 &
        echo "   ✅ XSS 靶场已启动: http://localhost:8087"
    else
        echo "   ✅ XSS 靶场已运行: http://localhost:8087"
    fi

    if [ -z "$API_RUNNING" ]; then
        python3 /tmp/ctf_targets/api_target.py > /tmp/api_target.log 2>&1 &
        echo "   ✅ API 靶场已启动: http://localhost:8088"
    else
        echo "   ✅ API 靶场已运行: http://localhost:8088"
    fi
else
    echo "   ⚠️  Flask 未安装，跳过本地靶场"
    echo "   安装: pip3 install flask"
fi

# 汇总
echo ""
echo "========================================"
echo "✅ 靶场部署完成"
echo "========================================"

echo ""
echo "📋 可用靶场:"
echo ""
echo "本地靶场:"
echo "  DVWA:        http://localhost:8081"
echo "  XSS Target:  http://localhost:8087"
echo "  API Target:  http://localhost:8088"
echo ""
echo "在线真实靶场:"
echo "  DVWA Online: http://testphp.vulnweb.com"
echo ""
echo "🎯 准备就绪，可以开始训练 Agent！"
echo ""
echo "🚀 运行训练:"
echo "  python3 /CTF_TRAINING.py"
echo ""
