#!/bin/bash
##############################################################################
# VulnHunter Enterprise - 一键部署脚本
# 
# 功能:
#   - 自动检查依赖
#   - 安装Python虚拟环境
#   - 安装项目依赖
#   - 配置环境变量
#   - 启动VulnHunter服务
#   - 设置开机自启
#
# 使用:
#   bash deploy.sh [选项]
#
# 选项:
#   --install     安装VulnHunter
#   --update      更新VulnHunter
#   --start       启动服务
#   --stop        停止服务
#   --restart     重启服务
#   --status      查看状态
#   --uninstall   卸载VulnHunter
#   --help        显示帮助
#
##############################################################################

set -e  # 遇到错误立即退出

# ==================== 配置 ====================
INSTALL_DIR="/opt/vulnhunter"
SERVICE_NAME="vulnhunter"
VENV_DIR="$INSTALL_DIR/venv"
LOG_DIR="/var/log/vulnhunter"
CONFIG_DIR="/etc/vulnhunter"
REPO_URL="https://github.com/zhangyan8216/ctf-tools.git"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ==================== 工具函数 ====================
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# ==================== 检查系统依赖 ====================
check_dependencies() {
    log_info "检查系统依赖..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 未安装!"
        log_info "安装Python 3..."
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv
    fi
    
    # 检查pip
    if ! command -v pip3 &> /dev/null; then
        log_error "pip3 未安装!"
        sudo apt-get install -y python3-pip
    fi
    
    # 检查Git
    if ! command -v git &> /dev/null; then
        log_error "Git 未安装!"
        sudo apt-get install -y git
    fi
    
    # 检查Docker (可选)
    if ! command -v docker &> /dev/null; then
        log_warning "Docker 未安装，Web Dashboard功能可能受限"
        log_info "是否安装Docker? (y/n)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            curl -fsSL https://get.docker.com -o get-docker.sh
            sudo sh get-docker.sh
            sudo usermod -aG docker $USER
        fi
    else
        log_success "Docker 已安装"
    fi
    
    log_success "系统依赖检查完成"
}

# ==================== 创建虚拟环境 ====================
create_venv() {
    log_info "创建Python虚拟环境..."
    
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    
    if [ -d "$VENV_DIR" ]; then
        log_warning "虚拟环境已存在，是否重新创建? (y/n)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            rm -rf "$VENV_DIR"
        else
            log_info "使用现有虚拟环境"
            return
        fi
    fi
    
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    
    # 升级pip
    pip install --upgrade pip setuptools wheel
    
    log_success "虚拟环境创建完成"
}

# ==================== 安装项目依赖 ====================
install_project() {
    log_info "安装VulnHunter..."
    
    cd "$INSTALL_DIR"
    
    # 克隆仓库
    if [ -d "ctf-tools" ]; then
        log_info "更新代码..."
        cd ctf-tools
        git pull origin master
    else
        log_info "克隆代码库..."
        git clone "$REPO_URL" ctf-tools
        cd ctf-tools/home/tools/vuln-hunter
    fi
    
    # 激活虚拟环境
    source "$VENV_DIR/bin/activate"
    
    # 安装依赖
    log_info "安装Python依赖..."
    pip install -r requirements.txt
    pip install -r requirements.txt  # 二次安装确保成功
    
    # 创建日志目录
    sudo mkdir -p "$LOG_DIR"
    sudo chown $USER:$USER "$LOG_DIR"
    
    # 创建配置目录
    sudo mkdir -p "$CONFIG_DIR"
    sudo chown $USER:$USER "$CONFIG_DIR"
    
    log_success "VulnHunter安装完成"
}

# ==================== 配置环境变量 ====================
setup_config() {
    log_info "配置环境变量..."
    
    CONFIG_FILE="$CONFIG_DIR/config.env"
    
    if [ -f "$CONFIG_FILE" ]; then
        log_warning "配置文件已存在，是否覆盖? (y/n)"
        read -r response
        if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            log_info "使用现有配置"
            return
        fi
    fi
    
    cat > "$CONFIG_FILE" << 'EOF'
# ==================== VulnHunter 配置 ====================

# API配置
VULNHUNTER_API_KEY=your-api-key-here
LOG_LEVEL=INFO

# 指纹配置
USER_AGENT=VulnHunter/1.0

# 代理配置（可选）
# HTTP_PROXY=http://proxy:8080
# HTTPS_PROXY=http://proxy:8080

# AI配置（可选）
# OPENAI_API_KEY=sk-proj-your-key
# ANTHROPIC_API_KEY=sk-ant-your-key

# 数据库配置（可选）
# DB_URL=postgresql://user:password@localhost:5432/vulnhunter

# Redis配置（可选）
# REDIS_URL=redis://localhost:6379/0
EOF
    
    log_warning "请编辑配置文件: $CONFIG_FILE"
    log_info "设置好API密钥后按回车继续..."
    read -r
    
    log_success "配置文件已创建"
}

# ==================== 创建systemd服务 ====================
create_service() {
    log_info "创建systemd服务..."
    
    SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
    
    sudo bash -c "cat > $SERVICE_FILE" << 'EOF'
[Unit]
Description=VulnHunter Enterprise Service
After=network.target

[Service]
Type=simple
User=vulnhunter
Group=vulnhunter
WorkingDirectory=/opt/vulnhunter/ctf-tools/home/tools/vuln-hunter
Environment="PATH=/opt/vulnhunter/venv/bin"
EnvironmentFile=/etc/vulnhunter/config.env
ExecStart=/opt/vulnhunter/venv/bin/python3 run.py --web
Restart=always
RestartSec=10

# 日志
StandardOutput=append:/var/log/vulnhunter/vulnhunter.log
StandardError=append:/var/log/vulnhunter/vulnhunter-error.log

[Install]
WantedBy=multi-user.target
EOF
    
    # 创建专用用户
    if ! id "$SERVICE_NAME" &>/dev/null; then
        log_info "创建系统用户: $SERVICE_NAME"
        sudo useradd -r -s /bin/false -d "$INSTALL_DIR" "$SERVICE_NAME"
        sudo chown -R $SERVICE_NAME:$SERVICE_NAME "$INSTALL_DIR"
        sudo chown -R $SERVICE_NAME:$SERVICE_NAME "$CONFIG_DIR"
        sudo chown -R $SERVICE_NAME:$SERVICE_NAME "$LOG_DIR"
    fi
    
    # 重新加载systemd
    sudo systemctl daemon-reload
    
    # 启用开机自启
    sudo systemctl enable "$SERVICE_NAME"
    
    log_success "systemd服务已创建"
}

# ==================== 启动服务 ====================
start_service() {
    log_info "启动VulnHunter服务..."
    
    sudo systemctl start "$SERVICE_NAME"
    
    # 等待服务启动
    sleep 5
    
    # 检查状态
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        log_success "VulnHunter服务启动成功!"
        log_info "访问地址: http://localhost:5001"
    else
        log_error "VulnHunter服务启动失败!"
        log_info "查看日志: sudo journalctl -u $SERVICE_NAME -n 50"
    fi
}

# ==================== 停止服务 ====================
stop_service() {
    log_info "停止VulnHunter服务..."
    
    sudo systemctl stop "$SERVICE_NAME"
    
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        log_error "服务停止失败!"
        exit 1
    else
        log_success "VulnHunter服务已停止"
    fi
}

# ==================== 重启服务 ====================
restart_service() {
    log_info "重启VulnHunter服务..."
    
    sudo systemctl restart "$SERVICE_NAME"
    
    sleep 5
    
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        log_success "VulnHunter服务重启成功!"
    else
        log_error "服务重启失败!"
    fi
}

# ==================== 查看状态 ====================
check_status() {
    log_info "VulnHunter服务状态:"
    echo ""
    
    # 服务状态
    sudo systemctl status "$SERVICE_NAME" --no-pager || true
    
    echo ""
    log_info "日志查看:"
    echo "  sudo journalctl -u $SERVICE_NAME -f"
    echo "  tail -f $LOG_DIR/vulnhunter.log"
    
    echo ""
    log_info "Web界面: http://localhost:5001"
}

# ==================== 更新VulnHunter ====================
update_vulnhunter() {
    log_info "更新VulnHunter..."
    
    cd "$INSTALL_DIR/ctf-tools"
    
    # 拉取最新代码
    git pull origin master
    
    # 安装依赖更新
    source "$VENV_DIR/bin/activate"
    cd home/tools/vuln-hunter
    pip install -r requirements.txt --upgrade
    
    # 重启服务
    restart_service
    
    log_success "VulnHunter更新完成!"
}

# ==================== 卸载VulnHunter ====================
uninstall_vulnhunter() {
    log_warning "这将完全删除VulnHunter!"
    log_warning "确认继续? (yes/no)"
    read -r response
    
    if [[ "$response" != "yes" ]]; then
        log_info "取消卸载"
        return
    fi
    
    # 停止服务
    sudo systemctl stop "$SERVICE_NAME"
    sudo systemctl disable "$SERVICE_NAME"
    
    # 删除服务文件
    sudo rm -f "/etc/systemd/system/${SERVICE_NAME}.service"
    sudo systemctl daemon-reload
    
    # 删除目录
    sudo rm -rf "$INSTALL_DIR"
    sudo rm -rf "$CONFIG_DIR"
    sudo rm -rf "$LOG_DIR"
    
    # 删除用户
    sudo userdel -r "$SERVICE_NAME" 2>/dev/null || true
    
    log_success "VulnHunter已完全卸载!"
}

# ==================== 显示帮助 ====================
show_help() {
    cat << 'EOF'
VulnHunter Enterprise - 一键部署脚本

用法:
    bash deploy.sh [选项]

选项:
    --install     安装VulnHunter
    --update      更新VulnHunter
    --start       启动服务
    --stop        停止服务
    --restart     重启服务
    --status      查看状态
    --uninstall   卸载VulnHunter
    --help        显示此帮助

示例:
    bash deploy.sh --install      # 首次安装
    bash deploy.sh --start        # 启动服务
    bash deploy.sh --status       # 查看状态
    bash deploy.sh --update       # 更新版本
    bash deploy.sh --uninstall    # 完全卸载

更多信息请访问: https://github.com/zhangyan8216/ctf-tools
EOF
}

# ==================== 主函数 ====================
main() {
    case "${1:-}" in
        --install)
            check_dependencies
            create_venv
            install_project
            setup_config
            create_service
            start_service
            ;;
        --update)
            update_vulnhunter
            ;;
        --start)
            start_service
            ;;
        --stop)
            stop_service
            ;;
        --restart)
            restart_service
            ;;
        --status)
            check_status
            ;;
        --uninstall)
            uninstall_vulnhunter
            ;;
        --help|*)
            show_help
            ;;
    esac
}

# 执行主函数
main "$@"
