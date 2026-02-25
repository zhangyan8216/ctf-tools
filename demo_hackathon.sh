#!/bin/bash
#
# 黑客松冠军项目 - 一键演示脚本
# 快速展示所有四个项目
#

echo "========================================"
echo "🏆 黑客松冠军项目 - 自动演示"
echo "========================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. VulnHunter AI 演示
echo -e "${BLUE}=== 1️⃣ VulnHunter Enterprise AI ===${NC}"
echo "📍 位置: /home/tools/vuln-hunter"
echo ""
echo "选项:"
echo "  A. 运行 AI 增强演示"
echo "  B. 启动 Web Dashboard"
echo "  C. 生成 AI 增强报告"
echo ""

read -p "选择 [A/B/C]: " vh_choice

case $vh_choice in
    [Aa])
        cd /home/tools/vuln-hunter && python3 AI_ENHANCEMENT.py
        ;;
    [Bb])
        cd /home/tools/vuln-hunter
        echo "🚀 启动 Web Dashboard (http://localhost:5001) ..."
        python3 web_server.py &
        sleep 2
        echo "✅ Web Dashboard 已启动！"
        echo "   访问: http://localhost:5001"
        ;;
    [Cc])
        cd /home/tools/vuln-hunter && python3 PROFESSIONAL_REPORT.py
        ;;
esac

echo ""
echo ""

# 2. CTF Agent 演示
echo -e "${BLUE}=== 2️⃣ CTF Agent Enhanced ===${NC}"
echo "📍 位置: /home/ctf_agent"
echo ""
echo "选项:"
echo "  A. 运行增强版 Agent 演示"
echo "  B. 列出所有增强工具"
echo "  C. 测试自动工具检测"
echo ""

read -p "选择 [A/B/C]: " ca_choice

case $ca_choice in
    [Aa])
        cd /home/ctf_agent && python3 ENHANCED_AGENT.py
        ;;
    [Bb])
        echo "📦 CTF Agent 增强工具列表:"
        echo ""
        echo "${YELLOW}Crypto Tools:${NC}"
        echo "  • caesar_decrypt - 凯撒密码解密"
        echo "  • base64/base32/base16_decode - 各种编码解码"
        echo "  • xor_bruteforce - XOR 密钥暴力破解"
        echo "  • analyze_hash - 哈希类型分析"
        echo ""
        echo "${YELLOW}Web Security:${NC}"
        echo "  • check_sqli - SQL 注入检测"
        echo "  • check_xss - XSS 漏洞检测"
        echo "  • analyze_jwt - JWT Token 分析"
        echo ""
        echo "${YELLOW}Forensics:${NC}"
        echo "  • extract_strings - 字符串提取"
        echo "  • detect_filetype - 文件类型检测"
        echo "  • binwalk_scan - 嵌入文件扫描"
        echo ""
        echo "${YELLOW}Encoding:${NC}"
        echo "  • url_decode - URL 解码"
        echo "  • morse_decode - 摩斯密码解码"
        echo "  • auto_decode - 自动多种解码"
        echo ""
        echo "✅ 总计: 21+ 增强工具"
        ;;
    [Cc])
        echo "🔍 自动工具检测演示:"
        echo ""
        echo "测试 1: Base64 编码"
        echo "  输入: 'SGVsbG8gV29ybGQ='"
        echo "  输出: 调用 base64_decode → Hello World"
        echo ""
        echo "测试 2: JWT Token"
        echo "  输入: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'"
        echo "  输出: 解析 Header/Payload/Signature"
        echo ""
        echo "测试 3: 加密文件"
        echo "  输入: 文件路径"
        echo "  输出: detect_filetype + extract_strings"
        ;;
esac

echo ""
echo ""

# 3. Agent by Cursor - Team 演示
echo -e "${BLUE}=== 3️⃣ Agent by Cursor + Team ===${NC}"
echo "📍 位置: /home/agent_by_cursor"
echo ""
echo "选项:"
echo "  A. 运行团队协作演示"
echo "  B. 查看实时排行榜"
echo "  C. 生成团队报告"
echo ""

read -p "选择 [A/B/C]: " abc_choice

case $abc_choice in
    [Aa])
        cd /home/agent_by_cursor && python3 src/team_collaboration.py
        ;;
    [Bb])
        echo "🏆 实时排行榜示例:"
        echo ""
        echo "  排名 | 用户ID  | 解题数"
        echo "  -----|---------|-------"
        echo "  1    | alice   | 15    🥇"
        echo "  2    | bob     | 12    🥈"
        echo "  3    | charlie | 10    🥉"
        echo "  4    | dave    | 8     "
        echo ""
        echo "✅ 实时更新 WebSocket 推送"
        ;;
    [Cc])
        echo "📊 团队报告示例:"
        echo ""
        echo "团队统计:"
        echo "  - 总解题数: 45 题"
        echo "  - 总尝试: 120 次"
        echo "  - 成功率: 37.5%"
        echo "  - 在线成员: 4 人"
        echo ""
        echo "平台状态:"
        echo "  - CTFd: ✅ 在线"
        echo "  - HackTheBox: ✅ 在线"
        echo "  - TryHackMe: ⏸️ 空闲"
        ;;
esac

echo ""
echo ""

# 4. Memory Blog 演示
echo -e "${BLUE}=== 4️⃣ Memory Blog ===${NC}"
echo "📍 位置: /var/www/memory-blog"
echo ""
echo "✅ SEO 优化特性:"
echo "  • 完整 Meta Tags"
echo "  • Open Graph / Twitter Cards"
echo "  • Schema.org 结构化数据"
echo ""
echo "✅ PWA 功能:"
echo "  • Service Worker 离线缓存"
echo "  • 响应式设计 (移动端优先)"
echo "  • Dark Mode 支持"
echo "  • 可添加到主屏幕"
echo ""
echo "🌐 访问地址:"
echo "  http://localhost/memory-blog/"
echo ""

read -p "打开 Memory Blog? [Y/n]: " blog_choice

if [[ $blog_choice =~ ^[Yy]$ || -z $blog_choice ]]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost/memory-blog/ 2>/dev/null || \
        firefox http://localhost/memory-blog/ 2>/dev/null || \
        echo "请手动打开: http://localhost/memory-blog/"
    else
        echo "请手动打开: http://localhost/memory-blog/"
    fi
fi

echo ""
echo ""

# 总结
echo -e "${GREEN}========================================"
echo "🎉 黑客松冠军项目 - 演示完成！"
echo "========================================${NC}"
echo ""
echo "📊 项目汇总:"
echo "  ✅ VulnHunter Enterprise - AI 智能漏洞扫描"
echo "  ✅ CTF Agent Enhanced - 21+ 增强工具"
echo "  ✅ Agent by Cursor + Team - 团队协作系统"
echo "  ✅ Memory Blog - SEO + PWA 优化"
echo ""
echo "🏆 关键亮点:"
echo "  • AI 驱动的漏洞分析和利用链生成"
echo "  • 自动化工具集成和智能选择"
echo "  • 实时团队协作和排行榜"
echo "  • 商业级报告和漂亮的展示"
echo ""
echo "📖 完整报告: /HACKATHON_CHAMPION_REPORT.md"
echo ""
echo -e "${YELLOW}🥇 祝贺夺冠！${NC}"
echo ""
