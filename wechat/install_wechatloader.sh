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
  return $?
}

# 函数：获取系统架构并选择镜像
select_image() {
  ARCH=$(uname -m)
  log "当前系统架构: $ARCH"

  case $ARCH in
    "aarch64")
      IMAGE_NAME="wechatloader-arm64:latest"
      DOWNLOAD_URL="https://git.kfc50.us.kg/https://github.com/wyourname/wool/releases/download/v1.0.5/wechatloader-arm64.tar.gz"
      ;;
    "x86_64")
      IMAGE_NAME="wechatloader:latest"
      DOWNLOAD_URL="https://git.kfc50.us.kg/https://github.com/wyourname/wool/releases/download/v1.0.5/wechatloader-amd64.tar.gz"
      ;;
    "armv7l")
      IMAGE_NAME="wechatloader-arm:latest"
      log "系统架构为 arm32，暂不支持。如果需要，请联系作者适配 wechatloader-arm.tar.gz..."
      exit 1
      ;;
    *)
      log "不支持的架构：$ARCH"
      exit 1
      ;;
  esac
}

# 函数：下载文件
download_file() {
  log "正在下载镜像文件..."
  wget $DOWNLOAD_URL -O wechatloader.tar.gz
  if [ $? -ne 0 ]; then
    log "下载失败，请检查网络连接或下载地址！"
    exit 1
  else
    log "下载完成：wechatloader.tar.gz"
  fi
}

# 函数：解压下载的文件
extract_file() {
  log "正在解压下载的文件..."
  tar -xzvf wechatloader.tar.gz
  if [ $? -ne 0 ]; then
    log "解压失败，请检查文件是否完整！"
    exit 1
  else
    log "解压完成：wechatloader.tar"
  fi
}

# 函数：导入镜像到 Docker
load_docker_image() {
  log "正在导入镜像到 Docker..."
  docker load < wechatloader.tar
  if [ $? -ne 0 ]; then
    log "镜像导入失败，请检查 Docker 是否安装并配置正确！"
    exit 1
  else
    log "镜像导入成功！"
  fi
}

# 函数：修补容器
patch_container() {
  log "正在修补容器 $CONTAINER_NAME..."
  
  # 下载 static.zip 文件
  log "正在下载 static.zip 文件..."
  wget https://git.kfc50.us.kg/https:// -O static.zip
  if [ $? -ne 0 ]; then
    log "下载 static.zip 失败，请检查网络连接！"
    exit 1
  fi

  # 解压 static.zip
  log "正在解压 static.zip..."
  unzip static.zip -d static
  if [ $? -ne 0 ]; then
    log "解压 static.zip 失败！"
    exit 1
  fi

  # 将解压的文件拷贝到容器的 /app/static 目录
  log "正在将 static 文件拷贝到容器..."
  docker cp static/. $CONTAINER_NAME:/app/static/
  if [ $? -ne 0 ]; then
    log "拷贝文件失败，请检查容器路径！"
    exit 1
  else
    log "修补完成！"
  fi
}

# 函数：重装容器
reinstall_container() {
  log "重装容器流程："
  
  # 停止并删除现有容器
  log "停止并删除容器 $CONTAINER_NAME..."
  docker stop $CONTAINER_NAME
  docker rm $CONTAINER_NAME
  
  # 删除镜像
  log "删除镜像 $IMAGE_NAME..."
  docker rmi $IMAGE_NAME

  # 重新下载文件、导入镜像并启动容器
  download_file
  extract_file
  load_docker_image
  start_container
}

# 函数：创建并启动容器
start_container() {
  log "正在创建并启动容器..."
  docker run -d -p 8011:8011 --restart=always --name wechatloader $IMAGE_NAME

  # 检查容器是否成功启动
  if [ $? -ne 0 ]; then
    log "容器启动失败，请检查 Docker 配置或者日志！"
    exit 1
  else
    log "容器启动成功，端口 8011 已映射。"
  fi
}

# 函数：输出当前正在运行的容器列表
list_running_containers() {
  log "当前正在运行的容器："
  docker ps
}

# 主程序开始
log "脚本开始执行 $(date)"

# 第一步：检查 Docker 是否已安装
check_docker

# 第二步：根据系统架构选择镜像和下载文件
select_image

# 第三步：检查容器是否存在
check_container_exists
if [ $? -eq 0 ]; then
  log "容器 $CONTAINER_NAME 已存在！"
  
  # 询问用户是否修补容器或重装容器
  echo "容器 $CONTAINER_NAME 已存在，请选择操作："
  echo "1. 修补容器"
  echo "2. 重装容器"
  read -p "请输入选择 (1/2): " action_choice
  
  case $action_choice in
    1)
      patch_container
      ;;
    2)
      reinstall_container
      ;;
    *)
      log "无效的选择！"
      exit 1
      ;;
  esac
else
  log "容器不存在，正在创建并启动新容器..."
  start_container
fi

# 第四步：输出正在运行的容器
list_running_containers

# 输出脚本结束时间
log "脚本执行完成 $(date)"
