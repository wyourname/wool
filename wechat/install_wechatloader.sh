#!/bin/bash

# 设置脚本的日志文件
LOG_FILE="install_wechatloader.log"
echo "脚本开始执行 $(date)" > $LOG_FILE

# 函数：输出日志
log() {
  echo "$1" | tee -a $LOG_FILE
}

# 函数：检查 Docker 是否安装
check_docker() {
  log "检查 Docker 是否已安装..."
  command -v docker >/dev/null 2>&1
  if [ $? -ne 0 ]; then
    log "Docker 未安装，请先安装 Docker！"
    exit 1
  else
    log "Docker 已安装！"
  fi
}

# 函数：检查容器是否已经存在
check_container_exists() {
  CONTAINER_NAME="wechatloader"
  log "检查容器 $CONTAINER_NAME 是否已存在..."
  docker ps -a --format '{{.Names}}' | grep -w $CONTAINER_NAME >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    log "容器 $CONTAINER_NAME 已存在，准备启动..."
  else
    log "容器 $CONTAINER_NAME 不存在，准备创建..."
  fi
}

# 获取系统架构
# 获取系统架构
ARCH=$(uname -m)

# 输出当前架构
echo "当前系统架构: $ARCH"

# 根据架构选择镜像
if [ "$ARCH" == "aarch64" ]; then
  IMAGE_NAME="wechatloader-arm64:latest"
elif [ "$ARCH" == "x86_64" ]; then
  IMAGE_NAME="wechatloader:latest"
elif [ "$ARCH" == "armv7l" ]; then
  IMAGE_NAME="wechatloader-arm:latest"
else
  echo "不支持的架构：$ARCH"
  exit 1
fi
# 第一步：检查 Docker 是否已安装
check_docker

# 第二步：根据系统架构下载文件
if [ "$ARCH" == "aarch64" ]; then
  log "系统架构为 ARM64，正在下载 wechatloader-arm64.tar.gz..."
  wget https://git.kfc50.us.kg/https://github.com/wyourname/wool/releases/download/v1.0.5/wechatloader-arm64.tar.gz -O wechatloader-arm64.tar.gz
elif [ "$ARCH" == "armv7l" ]; then
  log "系统架构为 arm32，暂不支持，如果你需要请联系作者适配 wechatloader-arm.tar.gz..."
  # wget https://git.kfc50.us.kg/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/wechatloader-arm.tar.gz -O wechatloader-arm.tar.gz]
else
  log "系统架构为 x86_64，正在下载 wechatloader.tar_12_19.tar.gz..."
  wget https://git.kfc50.us.kg/https://github.com/wyourname/wool/releases/download/v1.0.5/wechatloader-amd64.tar.gz -O wechatloader-amd64.tar.gz
fi

# 检查下载是否成功
if [ $? -ne 0 ]; then
  log "下载失败，请检查网络连接或者下载地址！"
  exit 1
else
  log "下载完成：$(ls -1 wechatloader*.tar.gz)"
fi

# 第三步：解压下载的文件
log "正在解压下载的文件..."
tar -xzvf $(ls -1 wechatloader*.tar.gz)

# 检查解压是否成功
if [ $? -ne 0 ]; then
  log "解压失败，请检查文件是否完整！"
  exit 1
else
  log "解压完成：wechatloader.tar"
fi

# 第四步：导入镜像到 Docker
log "正在导入镜像到 Docker..."
docker load < wechatloader.tar

# 检查 Docker 镜像导入是否成功
if [ $? -ne 0 ]; then
  log "镜像导入失败，请检查 Docker 是否安装并配置正确！"
  exit 1
else
  log "镜像导入成功！"
fi

# 第五步：检查容器是否已存在
check_container_exists

# 第六步：创建并启动容器
log "正在创建并启动容器..."
docker run -d -p 8011:8011 --restart=always --name wechatloader $IMAGE_NAME

# 检查容器是否成功启动
if [ $? -ne 0 ]; then
  log "容器启动失败，请检查 Docker 配置或者日志！"
  exit 1
else
  log "容器启动成功，端口 8011 已映射。耐心等待服务启动"
fi

# 输出当前正在运行的容器列表
log "当前正在运行的容器："
docker ps

# 输出脚本结束时间
log "脚本执行完成 $(date)"
