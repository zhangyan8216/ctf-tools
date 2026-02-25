#!/bin/bash
#
# 本地 CTF 靶场部署脚本
# 部署多个靶场用于训练 agent
#

echo "========================================"
echo "🎯 本地 CTF 靶场部署"
echo "========================================"

# 创建靶场网络
echo "创建靶场网络..."
docker network create ctf-range 2>/dev/null || echo "网络已存在"

# 1. DVWA (Damn Vulnerable Web Application)
echo ""
echo "1️⃣ 部署 DVWA..."

# 检查是否已存在
DVWA_RUNNING=$(docker ps -q -f name=dvwa)
if [ -n "$DVWA_RUNNING" ]; then
    echo "DVWA 已在运行"
else
    # 运行 DVWA
    docker run -d \
        --name dvwa \
        --network ctf-range \
        -p 8081:80 \
        -e DVWA_USERNAME=admin \
        -e DVWA_PASSWORD=password \
        vulnerables/web-dvwa

    echo "✅ DVWA 部署完成 - http://localhost:8081"
    echo "   默认登录: admin / password"
fi

# 2. bWAPP (Buggy Web Application)
echo ""
echo "2️⃣ 部署 bWAPP..."

# 检查是否已存在
BWAPP_RUNNING=$(docker ps -q -f name=bwapp)
if [ -n "$BWAPP_RUNNING" ]; then
    echo "bWAPP 已在运行"
else
    # 运行 bWAPP
    docker run -d \
        --name bwapp \
        --network ctf-range \
        -p 8082:80 \
        --security-opt seccomp:unconfined \
        raesene/bwapp

    echo "✅ bWAPP 部署完成 - http://localhost:8082"
    echo "   默认登录: bee / bug"
fi

# 3. Juice Shop (OWASP)
echo ""
echo "3️⃣ 部署 OWASP Juice Shop..."

JUICE_RUNNING=$(docker ps -q -f name=juice-shop)
if [ -n "$JUICE_RUNNING" ]; then
    echo "Juice Shop 已在运行"
else
    docker run -d \
        --name juice-shop \
        --network ctf-range \
        -p 8083:3000 \
        bkimminich/juice-shop

    echo "✅ Juice Shop 部署完成 - http://localhost:8083"
fi

# 4. WebGoat
echo ""
echo "4️⃣ 部署 WebGoat..."

WEBGOAT_RUNNING=$(docker ps -q -f name=webgoat)
if [ -n "$WEBGOAT_RUNNING" ]; then
    echo "WebGoat 已在运行"
else
    docker run -d \
        --name webgoat \
        --network ctf-range \
        -p 8084:8080 \
        webgoat/goatandwolf:latest

    echo "✅ WebGoat 部署完成 - http://localhost:8084/WebGoat"
fi

# 5. SQLi-Labs
echo ""
echo "5️⃣ 部署 SQLi-Labs..."

SQLILABS_RUNNING=$(docker ps -q -f name=sqli-labs)
if [ -n "$SQLILABS_RUNNING" ]; then
    echo "SQLi-Labs 已在运行"
else
    docker run -d \
        --name sqli-labs \
        --network ctf-range \
        -p 8085:80 \
        acgpiano/sqli-labs:latest

    echo "✅ SQLi-Labs 部署完成 - http://localhost:8085"
fi

# 6. HackTheBox 模拟环境
echo ""
echo "6️⃣ 部署 HTB 模拟环境..."

# 使用 TryHackMe 的简单靶机
docker pull parrotsec/security-playground &>/dev/null 2>&1 || true

HTB_RUNNING=$(docker ps -q -f name=htb-playground)
if [ -n "$HTB_RUNNING" ]; then
    echo "HTB Playground 已在运行"
else
    docker run -d \
        --name htb-playground \
        --network ctf-range \
        -p 2222:22 \
        -p 8086:80 \
        alpine:latest sh -c "apk add --no-cache openssh nginx && ssh-keygen -A && /usr/sbin/sshd & nginx -g 'daemon off;'"

    echo "✅ HTB Playground 部署完成"
    echo "   SSH: localhost:2222"
    echo "   HTTP: http://localhost:8086"
fi

echo ""
echo "========================================"
echo "✅ 所有靶场部署完成"
echo "========================================"

echo ""
echo "📋 靶场列表:"
echo "  DVWA:         http://localhost:8081 (admin/password)"
echo "  bWAPP:        http://localhost:8082 (bee/bug)"
echo "  Juice Shop:   http://localhost:8083"
echo "  WebGoat:      http://localhost:8084"
echo "  SQLi-Labs:    http://localhost:8085"
echo "  HTB Sim:      http://localhost:8086"

echo ""
echo "🔗 靶场网络: ctf-range"
echo ""
echo "🚀 准备就绪，可以开始训练 Agent！"
echo ""
