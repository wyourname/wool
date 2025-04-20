"""
通用代码
用于学习交流，请在下载24小时内删除代码
使用 task common.py --script=test --proxy=https://git.365676.xyz --file=common.so --max-retries=2 --no-retry
其中 script 为脚本名称，proxy 为代理地址，file 为文件名，max-retries 为最大重试次数，no-retry 为禁用重试机制
script 为必填参数，其他参数为可选参数，不填则使用默认值

"""

# 配置
SCRIPT_NAME = "test"  # 脚本名称，默认值


try:
    import logging
    import asyncio
    import platform
    import sys
    import os
    import re
    import enum
    import functools
    import aiohttp
    import aiofiles
    import argparse  # 添加argparse模块用于解析命令行参数
    from typing import Tuple, Optional, List, Dict, Any, Callable
except ImportError as e:
    print(f"缺少必要的模块，请安装: {e}")
    exit(1)


# URL配置
PROXY_URL = 'https://git.365676.xyz'   # 可以改成你的代理
BASE_URL = 'https://raw.githubusercontent.com/wyourname/wool/master/others'
ALPINE_URL = 'https://raw.githubusercontent.com/wyourname/wool/master/others/alpine'


logger = logging.getLogger(__name__)
if not logger.handlers: 
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s-%(levelname)s:%(message)s',
        datefmt='%H:%M:%S'
    ))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    # 设置为不向上传播日志，避免重复日志
    logger.propagate = False

# 使用枚举定义容器类型
class ContainerType(enum.Enum):
    UNKNOWN = "unknown"
    ALPINE = "alpine"
    DEBIAN = "debian"

# 使用枚举定义CPU架构
class CpuArchitecture(enum.Enum):
    X86_64 = "x86_64"
    AARCH64 = "aarch64"
    ARMV8 = "armv8"
    ARMV7 = "armv7l"

# 使用枚举定义环境检查结果
class EnvCheckResult(enum.Enum):
    SUCCESS = "success"
    INVALID_PYTHON = "invalid_python"
    INVALID_OS = "invalid_os"
    INVALID_ARCH = "invalid_arch"

# 解析命令行参数
def parse_arguments():
    parser = argparse.ArgumentParser(description='脚本下载器')
    parser.add_argument('--script', dest='script_name', type=str,
                        help='指定要执行的脚本名称')
    parser.add_argument('--proxy', dest='proxy_url', type=str,
                        help='指定代理URL')
    parser.add_argument('--file', dest='file_name', type=str, default='common.so',
                        help='指定要下载的文件名')
    parser.add_argument('--no-retry', dest='no_retry', action='store_true',
                        help='禁用重试机制')
    parser.add_argument('--max-retries', dest='max_retries', type=int, default=2,
                        help='设置最大重试次数')
    return parser.parse_args()

# 获取脚本名称，优先使用命令行参数
def get_script_name():
    args = parse_arguments()
    if args.script_name:
        logger.info(f"使用命令行参数指定的脚本名称: {args.script_name}")
        return args.script_name
    else:
        logger.info(f"使用默认脚本名称: {SCRIPT_NAME}")
        return SCRIPT_NAME

# 获取代理URL，优先使用命令行参数
def get_proxy_url():
    args = parse_arguments()
    if args.proxy_url:
        logger.info(f"使用命令行参数指定的代理URL: {args.proxy_url}")
        return args.proxy_url
    return PROXY_URL

# 获取最大重试次数
def get_max_retries():
    args = parse_arguments()
    if args.no_retry:
        return 0
    return args.max_retries

# 异常处理装饰器
def exception_handler(func):
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"执行 {func.__name__} 时出错: {e}")
            return None
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"执行 {func.__name__} 时出错: {e}")
            return None
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper

@exception_handler
def detect_container() -> Tuple[bool, Optional[ContainerType]]:
    is_container = os.path.exists('/.dockerenv')
    container_type = None
    
    if not is_container:
        return False, None
    if os.path.exists('/etc/os-release'):
        with open('/etc/os-release', 'r') as f:
            os_info = f.read().lower()
            if 'alpine' in os_info:
                return True, ContainerType.ALPINE
            if 'debian' in os_info:
                return True, ContainerType.DEBIAN
    if os.path.exists('/etc/alpine-release'):
        return True, ContainerType.ALPINE
    if os.path.exists('/etc/debian_version'):
        return True, ContainerType.DEBIAN
    
    return True, ContainerType.UNKNOWN

@exception_handler
def get_environment_info() -> Tuple[int, str, str]:
    """获取当前环境信息"""
    v = sys.version_info
    o = platform.system()
    a = platform.machine()
    return v.minor, o, a

@exception_handler
def check_environment(file_name: str) -> EnvCheckResult:
    """检查运行环境是否符合要求"""
    # 检查命令行参数，优先使用命令行指定的文件名
    args = parse_arguments()
    if args.file_name:
        file_name = args.file_name
        logger.info(f"使用命令行参数指定的文件名: {file_name}")
    
    py_minor, os_type, arch = get_environment_info()
    logger.info(f"Python版本: 3.{py_minor}, 操作系统: {os_type}, 架构: {arch}")
    
    # 检测容器环境
    is_container, container_type = detect_container()
    if is_container:
        logger.info(f"检测到容器环境: {container_type.value if container_type else '未知类型'}")
    
    # 检查Python版本
    if py_minor not in [9, 10, 11, 12]:
        logger.error("不符合要求: Python版本不是3.9、3.10、3.11或3.12")
        return EnvCheckResult.INVALID_PYTHON
    
    # 检查操作系统
    if os_type != 'Linux':
        logger.error("不符合要求: 操作系统类型不是Linux")
        return EnvCheckResult.INVALID_OS
    
    # 检查CPU架构
    valid_architectures = [arch.value for arch in CpuArchitecture]
    if arch not in valid_architectures:
        logger.error(f"不符合要求: 处理器架构不支持(需要{', '.join(valid_architectures)})")
        return EnvCheckResult.INVALID_ARCH
    
    # 环境检查通过，进行后续操作
    logger.info("环境符合运行要求")
    asyncio.run(process_so_file(file_name, py_minor, arch, container_type))
    return EnvCheckResult.SUCCESS

@exception_handler
async def process_so_file(filename: str, py_v: int, cpu_info: str, container_type: Optional[ContainerType]) -> bool:
    # 添加重试计数器
    if not hasattr(process_so_file, 'retry_count'):
        process_so_file.retry_count = 0
    
    # 获取最大重试次数
    MAX_RETRIES = get_max_retries()
    if process_so_file.retry_count >= MAX_RETRIES:
        logger.error(f"已达到最大重试次数({MAX_RETRIES})，停止尝试")
        return False
    
    if not os.path.exists(filename):
        logger.info(f"文件{filename}不存在，正在下载...")
        return await download_so_file(filename, py_v, cpu_info, container_type)
    
    logger.info(f"本地已存在文件: {filename}")
    try:
        import common
        # 获取脚本名称，优先使用命令行参数
        script_name = get_script_name()
        await common.main(script_name)
        # 成功后重置计数器
        process_so_file.retry_count = 0
        return True
    except Exception as e:
        logger.error(f"加载{filename}失败: {e}")
        # 增加重试计数
        process_so_file.retry_count += 1
        os.remove(filename)
        return await download_so_file(filename, py_v, cpu_info, container_type)

@exception_handler
async def download_so_file(filename: str, py_v: int, cpu_info: str, container_type: Optional[ContainerType]) -> bool:
    """异步下载.so文件"""
    file_base_name = os.path.splitext(filename)[0]
    
    # 确定下载URL，使用命令行参数指定的代理URL
    base_download_url = get_download_url(container_type)
    if container_type == ContainerType.ALPINE:
        logger.info(f"使用Alpine专用下载链接: {base_download_url}")
    
    # 根据CPU架构构建URL
    url = build_download_url(base_download_url, file_base_name, py_v, cpu_info)
    if not url:
        return False
    
    logger.info(f"正在从 {url} 下载文件...")
    
    # 使用aiohttp下载并显示进度条
    success = await download_with_progress(url, filename)
    
    if success:
        logger.info(f"文件下载成功: {filename}")
        return await process_so_file(filename, py_v, cpu_info, container_type)
    
    # 下载失败
    logger.error(f"下载失败: {url}")
    if os.path.exists(filename):
        os.remove(filename)
    
    # 如果是Alpine，尝试使用普通链接
    if container_type == ContainerType.ALPINE:
        logger.info("尝试使用标准链接下载...")
        return await download_so_file(filename, py_v, cpu_info, None)
    
    return False

def get_download_url(container_type: Optional[ContainerType]) -> str:
    """根据容器类型获取下载URL"""
    # 获取代理URL，优先使用命令行参数
    proxy_url = get_proxy_url()
    
    # 设置基本URL
    if not proxy_url:
        base_url = ALPINE_URL if container_type == ContainerType.ALPINE else BASE_URL
    else:
        proxy = proxy_url if proxy_url.endswith('/') else f"{proxy_url}/"
        base_url = f"{proxy}{ALPINE_URL}" if container_type == ContainerType.ALPINE else f"{proxy}{BASE_URL}"
    
    return base_url

def build_download_url(base_url: str, file_base_name: str, py_v: int, cpu_info: str) -> Optional[str]:
    """构建下载URL"""
    if cpu_info in [CpuArchitecture.AARCH64.value, CpuArchitecture.ARMV8.value]:
        return f"{base_url}/{file_base_name}_3{py_v}_aarch64.so"
    elif cpu_info == CpuArchitecture.X86_64.value:
        return f"{base_url}/{file_base_name}_3{py_v}_{cpu_info}.so"
    elif cpu_info == CpuArchitecture.ARMV7.value:
        return f"{base_url}/{file_base_name}_3{py_v}_armv7.so"
    else:
        logger.error(f"不支持的CPU架构: {cpu_info}")
        return None

@exception_handler
async def download_with_progress(url: str, filename: str) -> bool:
    """使用aiohttp下载文件并显示进度条"""
    session = aiohttp.ClientSession()
    async with session:
        response = await session.get(url)
        if response.status != 200:
            logger.error(f"HTTP请求失败，状态码: {response.status}")
            return False
        total_size = int(response.headers.get('content-length', 0))
        return await save_file_with_progress(response, filename, total_size)
    


async def save_file_with_progress(response, filename: str, total_size: int) -> bool:
    """保存文件并显示进度条"""
    downloaded_size = 0
    chunk_size = 8192 
    progress_bar_length = 30  
    async with aiofiles.open(filename, 'wb') as f:
        async for chunk in response.content.iter_chunked(chunk_size):
            await f.write(chunk)
            downloaded_size += len(chunk)
            await update_progress_bar(downloaded_size, total_size, progress_bar_length)
    print()
    return True


async def update_progress_bar(downloaded_size: int, total_size: int, bar_length: int) -> None:
    """更新并显示下载进度条"""
    progress = downloaded_size / total_size if total_size else 0
    arrow = '=' * int(bar_length * progress)
    spaces = ' ' * (bar_length - len(arrow))

    if total_size >= 1024 * 1024:  # MB级别
        size_str = f"{downloaded_size/(1024*1024):.2f}MB/{total_size/(1024*1024):.2f}MB"
    else:  # KB级别
        size_str = f"{downloaded_size/1024:.2f}KB/{total_size/1024:.2f}KB"

    print(f"\r下载进度: [{arrow}{spaces}] {int(progress*100)}% {size_str}", end='', flush=True)

if __name__ == '__main__':
    # 解析命令行参数并执行环境检查
    args = parse_arguments()
    logger.info(f"启动代码执行器...")
    # 开始下载和检查过程
    check_environment(args.file_name if args.file_name else 'common.so')
