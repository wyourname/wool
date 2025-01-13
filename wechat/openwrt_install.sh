#!/bin/sh

# 设置严格模式
set -euo pipefail

# 设置脚本的日志文件 
LOG_FILE="/tmp/install_wechatloader.log"
CONTAINER_NAME="wechatloader"
WORK_DIR="/tmp/wechatloader_install"

# 函数：检查root权限
check_root() {
    if [ "$(id -u)" -ne 0 ]; then
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
            log "$cmd 未安装，正在尝试使用 opkg 安装..."
            opkg update && opkg install "$cmd" || {
                log "无法安装 $cmd，请手动安装后重试。"
                exit 1
            }
        fi
    done
}

# 函数：获取系统架构并选择镜像
select_image() {
    ARCH=$(uname -m)
    log "当前系统架构: $ARCH"

    case $ARCH in
        "arm64" | "aarch64")
            IMAGE_NAME="wechatloader-arm64:latest"
            DOWNLOAD_URL="https://git.kfc50.us.kg/https://github.com/wyourname/wool/releases/download/v1.1.0/wechatloader-arm64.tar.gz"
            LAYERS_URL="https://git.kfc50.us.kg/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/layers-arm64"
            MAIN_URL="https://git.kfc50.us.kg/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/main-arm64"
            ;;
        "armv7" | "armv7l" | "armv7a" | "armv7b" | "arm")
            IMAGE_NAME="wechatloader-arm32:latest"
            DOWNLOAD_URL="https://git.kfc50.us.kg/https://github.com/wyourname/wool/releases/download/v1.1.0/wechatloader-arm32.tar.gz"
            LAYERS_URL="https://git.kfc50.us.kg/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/layers-arm"
            MAIN_URL="https://git.kfc50.us.kg/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/main-arm"
            ;;
        "x86_64")
            IMAGE_NAME="wechatloader:latest"
            DOWNLOAD_URL="https://git.kfc50.us.kg/https://github.com/wyourname/wool/releases/download/v1.1.0/wechatloader-amd64.tar.gz"
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

# 函数：重装容器
reinstall_container() {
    log "开始重装容器..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    docker rmi "$IMAGE_NAME" 2>/dev/null || true

    install_container
}

install_container() {
    download_file "$DOWNLOAD_URL" "wechatloader.tar.gz"
    tar xzf wechatloader.tar.gz
    docker load < wechatloader.tar

    start_container

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

# 主程序
main() {
    check_root
    init_workspace
    check_requirements
    select_image

    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        log "发现已存在的容器"
        while true; do
            echo
            echo "请选择操作："
            echo "0. 退出"
            echo "1. 重装容器"
            read -p "输入选择 (1/0): " choice

            case "$choice" in
                0)
                    log "退出安装"
                    exit 0
                    ;;
                1)
                    log "执行重装操作"
                    reinstall_container
                    break
                    ;;
                *)
                    echo "无效的选择，请重新输入"
                    ;;
            esac
        done
    else
        log "未发现已存在的容器，开始全新安装"
        install_container
    fi

    log "安装完成，容器状态："
    docker ps | grep "$CONTAINER_NAME"
}

# 执行主程序
main "$@"
