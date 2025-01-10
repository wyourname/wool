#!/bin/bash

# 设置严格模式
set -euo pipefail

# 设置脚本的日志文件 
LOG_FILE="/tmp/install_wechatloader.log"
CONTAINER_NAME="wechatloader"
WORK_DIR="/tmp/wechatloader_install"

# 函数：检查root权限
check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo "请使用 root 权限运行此脚本"
        exit 1
    fi
}

# 函数：初始化工作目录
init_workspace() {
    mkdir -p "$WORK_DIR"
    cd "$WORK_DIR"
    echo "脚本开始执行 $(date)" > "$LOG_FILE"
    chmod 644 "$LOG_FILE"
}

# 函数：输出日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 函数：检查必要的命令
check_requirements() {
    local requirements="docker wget tar unzip"
    for cmd in $requirements; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            log "正在安装 $cmd..."
            apt-get update && apt-get install -y "$cmd"
        fi
    done
}

# 函数：检查 Docker 服务状态
check_docker_service() {
    log "检查 Docker 服务状态..."
    if ! systemctl is-active --quiet docker; then
        log "Docker 服务未运行，正在启动..."
        systemctl start docker
        sleep 3
    fi
}

# 函数：获取系统架构并选择镜像
select_image() {
    ARCH=$(uname -m)
    log "当前系统架构: $ARCH"

    case $ARCH in
        "aarch64")
            IMAGE_NAME="wechatloader-arm64:latest"
            DOWNLOAD_URL="https://git.kfc50.us.kg/https://github.com/wyourname/wool/releases/download/v1.0.5/wechatloader-arm64.tar.gz"
            LAYERS_URL="https://git.kfc50.us.kg/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/layers-arm64"
            MAIN_URL="https://git.kfc50.us.kg/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/main-arm64"
            ;;
        "x86_64")
            IMAGE_NAME="wechatloader:latest"
            DOWNLOAD_URL="https://git.kfc50.us.kg/https://github.com/wyourname/wool/releases/download/v1.0.5/wechatloader-amd64.tar.gz"
            LAYERS_URL="https://git.kfc50.us.kg/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/layers-amd64"
            MAIN_URL="https://git.kfc50.us.kg/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/main-amd64"
            ;;
        *)
            log "不支持的系统架构: $ARCH"
            exit 1
            ;;
    esac
}

# 函数：下载文件
download_file() {
    local url="$1"
    local output="$2"
    log "正在下载: $output"
    if ! wget --timeout=10 --tries=3 -q "$url" -O "$output"; then
        log "下载失败: $output"
        return 1
    fi
    return 0
}

# 函数：修补容器
patch_container() {
    log "开始更新容器..."
    
    # 获取架构相关的文件后缀
    local arch_suffix
    case $(uname -m) in
        "x86_64")  arch_suffix="amd64" ;;
        "aarch64") arch_suffix="arm64" ;;
        *) log "不支持的架构"; exit 1 ;;
    esac
    
    # 创建临时目录
    local temp_dir=$(mktemp -d)
    cd "$temp_dir"

    # 下载所需文件（保留原始文件名）
    download_file "$LAYERS_URL" "layers-${arch_suffix}"
    download_file "$MAIN_URL" "main-${arch_suffix}"
    download_file "https://git.kfc50.us.kg/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/static.zip" "static.zip"

    # 解压并复制文件
    unzip -q static.zip
    
    # 复制文件到容器（使用正确的文件名）
    docker cp static/. "$CONTAINER_NAME:/app/static/"
    docker cp "layers-${arch_suffix}" "$CONTAINER_NAME:/app/layers-${arch_suffix}"
    docker cp "main-${arch_suffix}" "$CONTAINER_NAME:/app/main-${arch_suffix}"

    # 重启容器
    docker restart "$CONTAINER_NAME"
    
    # 清理临时文件
    cd - > /dev/null
    rm -rf "$temp_dir"
    
    log "容器修补完成"
}

# 函数：重装容器
reinstall_container() {
    log "开始重装容器..."
    
    # 停止并删除现有容器
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    docker rmi "$IMAGE_NAME" 2>/dev/null || true

    install_container
}

install_container(){
  # 下载并加载新镜像
    download_file "$DOWNLOAD_URL" "wechatloader.tar.gz"
    tar xzf wechatloader.tar.gz
    docker load < wechatloader.tar
    
    # 启动新容器
    start_container
    
    # 清理文件
    rm -f wechatloader.tar.gz wechatloader.tar
}


# 函数：启动容器
start_container() {
    log "正在启动容器..."
    if ! docker run -d -p 8011:8011 --restart=always --name "$CONTAINER_NAME" "$IMAGE_NAME"; then
        log "容器启动失败"
        exit 1
    fi
    log "容器启动成功"
}

get_user_choice() {
    # 确保从终端读取输入
    while true; do
        printf "请选择操作：\n1. 修补容器\n2. 重装容器\n"
        printf "输入选择 (1/2): "
        read choice </dev/tty
        
        case "$choice" in
            "1"|"2")
                return "$choice"
                ;;
            *)
                echo "无效的选择，请输入 1 或 2"
                ;;
        esac
    done
}

# 主程序
main() {
    check_root
    init_workspace
    check_requirements
    check_docker_service
    select_image

    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        log "发现已存在的容器"
        get_user_choice
        choice=$?
        
        if [ "$choice" -eq 1 ]; then
            patch_container
        elif [ "$choice" -eq 2 ]; then
            reinstall_container
        fi
    else
        log "未发现已存在的容器，开始全新安装"
        install_container
    fi

    log "安装完成，容器状态："
    docker ps | grep "$CONTAINER_NAME"
}

# 执行主程序
main "$@"