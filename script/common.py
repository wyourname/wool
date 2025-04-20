"""
通用代码
用于学习交流，请在下载24小时内删除代码
"""
import logging
import asyncio
import platform
import sys
import os
import subprocess
import re
import enum
import functools
import aiohttp
import aiofiles
from typing import Tuple, Optional, List, Dict, Any, Callable

# 配置
SCRIPT_NAME = "test"  # 脚本名称

# URL配置
PROXY_URL = 'https://git.365676.xyz'   # 可以改成你的代理
BASE_URL = 'https://raw.githubusercontent.com/wyourname/wool/master/others'
ALPINE_URL = 'https://raw.githubusercontent.com/wyourname/wool/master/others/alpine'

# 日志配置 - 只配置当前模块的日志器，不影响全局
logger = logging.getLogger(__name__)
if not logger.handlers:  # 防止重复添加处理器
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

# 使用枚举定义下载工具
class DownloadTool(enum.Enum):
    CURL = "curl"
    WGET = "wget"
    AIOHTTP = "aiohttp"

# 使用枚举定义环境检查结果
class EnvCheckResult(enum.Enum):
    SUCCESS = "success"
    INVALID_PYTHON = "invalid_python"
    INVALID_OS = "invalid_os"
    INVALID_ARCH = "invalid_arch"

# 异常处理装饰器
def exception_handler(func):
    """装饰器：捕获并处理函数执行过程中的异常"""
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
    
    # 根据函数是否是协程函数返回不同的包装器
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper

@exception_handler
def detect_container() -> Tuple[bool, Optional[ContainerType]]:
    """检测当前是否在容器中运行，以及容器类型"""
    is_container = os.path.exists('/.dockerenv')
    container_type = None
    
    if not is_container:
        return False, None
        
    # 通过/etc/os-release检测
    if os.path.exists('/etc/os-release'):
        with open('/etc/os-release', 'r') as f:
            os_info = f.read().lower()
            if 'alpine' in os_info:
                return True, ContainerType.ALPINE
            if 'debian' in os_info:
                return True, ContainerType.DEBIAN
    
    # 通过特定文件检测
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
    if not os.path.exists(filename):
        logger.info(f"文件{filename}不存在，正在下载...")
        return await download_so_file(filename, py_v, cpu_info, container_type)
    
    logger.info(f"本地已存在文件: {filename}")
    try:
        import common
        await common.main(SCRIPT_NAME)
        return True
    except Exception as e:
        logger.error(f"加载{filename}失败: {e}")
        os.remove(filename)
        return await download_so_file(filename, py_v, cpu_info, container_type)

@exception_handler
async def download_so_file(filename: str, py_v: int, cpu_info: str, container_type: Optional[ContainerType]) -> bool:
    """异步下载.so文件"""
    file_base_name = os.path.splitext(filename)[0]
    
    # 确定下载URL
    base_download_url = get_download_url(container_type)
    if container_type == ContainerType.ALPINE:
        logger.info(f"使用Alpine专用下载链接: {base_download_url}")
    
    # 根据CPU架构构建URL
    url = build_download_url(base_download_url, file_base_name, py_v, cpu_info)
    if not url:
        return False
    
    logger.info(f"正在从 {url} 下载文件...")
    
    # 尝试使用不同工具下载
    for tool in [DownloadTool.AIOHTTP, DownloadTool.CURL, DownloadTool.WGET]:
        if await try_download(tool, url, filename):
            logger.info(f"文件下载成功: {filename}")
            return await process_so_file(filename, py_v, cpu_info, container_type)
    
    # 所有工具都下载失败
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
    # 设置基本URL
    if not PROXY_URL:
        base_url = ALPINE_URL if container_type == ContainerType.ALPINE else BASE_URL
    else:
        proxy = PROXY_URL if PROXY_URL.endswith('/') else f"{PROXY_URL}/"
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
async def try_download(tool: DownloadTool, url: str, filename: str) -> bool:
    """尝试使用指定工具下载文件"""
    if tool == DownloadTool.AIOHTTP:
        return await download_with_aiohttp(url, filename)
    elif tool == DownloadTool.CURL and check_command_exists('curl'):
        return await download_with_curl(url, filename)
    elif tool == DownloadTool.WGET and check_command_exists('wget'):
        return await download_with_wget(url, filename)
    return False

@exception_handler
async def download_with_aiohttp(url: str, filename: str) -> bool:
    """使用aiohttp下载文件"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return False
                
                async with aiofiles.open(filename, 'wb') as f:
                    await f.write(await response.read())
                return True
    except:
        # aiohttp可能未安装，静默失败
        return False

@exception_handler
async def download_with_curl(url: str, filename: str) -> bool:
    """使用curl下载文件"""
    command = ['curl', '-#', '-o', filename, '-w', '%{http_code}', url]
    result, stdout = await run_command(command)
    return stdout == '200' and result == 0

@exception_handler
async def download_with_wget(url: str, filename: str) -> bool:
    """使用wget下载文件"""
    command = ['wget', '-q', '-O', filename, url]
    result, _ = await run_command(command)
    return result == 0

@exception_handler
async def run_command(command: List[str]) -> Tuple[int, str]:
    """异步执行shell命令并返回结果"""
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )
    
    stdout_data = await process.stdout.read()
    await process.wait()
    
    output = stdout_data.decode('utf-8', errors='ignore').strip()
    return process.returncode, output

@exception_handler
def check_command_exists(command: str) -> bool:
    """检查系统中是否存在指定命令"""
    try:
        subprocess.run(
            ['which', command], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            check=True
        )
        return True
    except subprocess.SubprocessError:
        return False

if __name__ == '__main__':
    check_environment('common.so')
