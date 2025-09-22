"""
通用代码 - 脚本下载器和执行器
命令行使用说明：
python common.py [参数选项]

参数详解：
--script SCRIPT_NAME        指定要执行的脚本名称 (默认: test)
                            示例: --script abc

--proxy PROXY_URL           指定代理服务器URL (默认: https://git.365676.xyz)
                            示例: --proxy https://your-proxy.com

--file FILE_NAME            指定要下载的文件名 (默认: common.so)
                            示例: --file myfile.so

--max-retries MAX_RETRIES   设置最大重试次数，设置为0禁用重试 (默认: 2)
                            示例: --max-retries 3

--concurrency               是否启用脚本并发参数 (开关参数，无需值)
                            示例: --concurrency

--max-concurrency NUM      设置最大并发数 (默认: 5)
                            示例: --max-concurrency 10

使用示例：
# 基本使用
python common.py --script theater

# 完整参数示例
python common.py --script theater --proxy https://git.365676.xyz --file common.so --max-retries 2 --concurrency --max-concurrency 3

# 禁用重试
python common.py --script test --max-retries 0

# 使用自定义代理
python common.py --script myapp --proxy https://my-proxy.com --file myapp.so

# 青龙基本用法
task common.py --script 脚本名 --concurrency
或者
python3 common.py --script 脚本名 --concurrency

功能说明：
1. 自动检测运行环境（Python版本、操作系统、CPU架构）
2. 检测容器环境（Docker、Alpine、Debian等）
3. 根据环境自动下载对应的.so文件
4. 支持重试机制和进度条显示
5. 自动设置环境变量供脚本使用
6. 支持代理服务器下载

环境变量设置：
- {script_name}_concurrency: 并发开关状态
- {script_name}_max_concurrency: 最大并发数
- GITHUB_PROXY: 代理服务器地址

环境要求：
- Python 3.9-3.12
- Linux 操作系统
- 支持的CPU架构: x86_64, aarch64, armv8, armv7l
- 依赖包: aiohttp, aiofiles
码友如需借鉴请带上原作者出处
"""

import logging
import asyncio
import platform
import sys
import os
import enum
import functools
import argparse
import subprocess
from pathlib import Path
from typing import Tuple, Optional

try:
    import aiohttp
    import aiofiles
except ImportError as e:
    print(f"缺少必要的模块，请安装: pip install aiohttp aiofiles")
    sys.exit(1)

# 配置
SCRIPT_NAME = "test"

# URL配置
PROXY_URL = 'https://git.365676.xyz'
BASE_URL = 'https://raw.githubusercontent.com/wyourname/wool/master/others'
ALPINE_URL = 'https://raw.githubusercontent.com/wyourname/wool/master/others/alpine'

# 配置日志
def setup_logger(log_level='INFO'):
    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            fmt='%(asctime)s-%(levelname)s:%(message)s',
            datefmt='%H:%M:%S'
        ))
        _logger.setLevel(getattr(logging, log_level))
        _logger.addHandler(handler)
        _logger.propagate = False
    return _logger

# 初始化时使用默认日志级别，稍后会根据配置更新
logger = setup_logger()


# 使用枚举定义容器类型
class ContainerType(enum.Enum):
    UNKNOWN = "unknown"
    ALPINE = "alpine"
    DEBIAN = "debian"


# 使用枚举定义CPU架构
class CpuArchitecture(enum.Enum):
    x86 = 'x86'
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


class Config:
    """配置类，单例模式避免重复解析参数"""
    _instance = None
    _args = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._parse_arguments()
        return cls._instance
    
    @classmethod
    def _parse_arguments(cls):
        parser = argparse.ArgumentParser(description='脚本下载器')
        parser.add_argument('--script', dest='script_name', type=str,
                            help='指定要执行的脚本名称')
        parser.add_argument('--proxy', dest='proxy_url', type=str,
                            help='指定代理URL')
        parser.add_argument('--file', dest='file_name', type=str, default='common.so',
                            help='指定要下载的文件名')
        parser.add_argument('--max-retries', dest='max_retries', type=int, default=2,
                            help='设置最大重试次数，设置为0禁用重试')
        parser.add_argument('--concurrency', dest='concurrency', action='store_true',
                            help='是否启用script并发参数')
        parser.add_argument('--max-concurrency', dest='max_concurrency', type=int, 
                            default=5, help='设置最大并发数')
        parser.add_argument('--log-level', dest='log_level', type=str, 
                            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO',
                            help='设置日志级别')
        cls._args = parser.parse_args()
    
    @property
    def script_name(self):
        return self._args.script_name or SCRIPT_NAME
    
    @property
    def proxy_url(self):
        proxy = self._args.proxy_url or PROXY_URL
        if not proxy.endswith("/"):
            proxy += "/"
        return proxy
    
    @property
    def file_name(self):
        return self._args.file_name
    
    @property
    def max_retries(self):
        return self._args.max_retries
    
    @property
    def concurrency(self):
        return self._args.concurrency
    
    @property
    def max_concurrency(self):
        return self._args.max_concurrency
    
    @property
    def log_level(self):
        return self._args.log_level

config = Config()


def set_environment():
    """设置环境变量"""
    script_name = config.script_name
    os.environ[f'{script_name}_concurrency'] = str(config.concurrency)
    os.environ[f'{script_name}_max_concurrency'] = str(config.max_concurrency)
    os.environ['GITHUB_PROXY'] = config.proxy_url
    logger.info(f"设置环境变量: {script_name}_concurrency={config.concurrency}")
    logger.info(f"设置环境变量: {script_name}_max_concurrency={config.max_concurrency}")
    logger.info(f"设置环境变量: GITHUB_PROXY={config.proxy_url}")


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

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper


@exception_handler
def detect_container() -> Tuple[bool, Optional[ContainerType]]:
    """检测容器环境和类型"""
    if not os.path.exists('/.dockerenv'):
        return False, None
    
    # 检查容器类型的优先级顺序
    container_checks = [
        ('/etc/alpine-release', ContainerType.ALPINE),
        ('/etc/debian_version', ContainerType.DEBIAN),
    ]
    
    for file_path, container_type in container_checks:
        if os.path.exists(file_path):
            return True, container_type
    
    # 检查 /etc/os-release
    if os.path.exists('/etc/os-release'):
        try:
            with open('/etc/os-release', 'r') as f:
                os_info = f.read().lower()
                if 'alpine' in os_info:
                    return True, ContainerType.ALPINE
                if 'debian' in os_info:
                    return True, ContainerType.DEBIAN
        except IOError:
            pass
    
    return True, ContainerType.UNKNOWN


@exception_handler
def get_environment_info() -> Tuple[int, str, str]:
    """获取当前环境信息"""
    v = sys.version_info
    o = platform.system()
    a = platform.machine()
    return v.minor, o, a


@exception_handler
def check_environment(file_name: str = None) -> EnvCheckResult:
    """检查运行环境是否符合要求"""
    file_name = file_name or config.file_name
    logger.info(f"使用文件名: {file_name}")

    py_minor, os_type, arch = get_environment_info()
    logger.info(f"Python版本: 3.{py_minor}, 操作系统: {os_type}, 架构: {arch}")

    # 检测容器环境
    is_container, container_type = detect_container()
    if is_container:
        logger.info(f"检测到容器环境: {container_type.value if container_type else '未知类型'}")

    # 环境验证
    validations = [
        (py_minor in [9, 10, 11, 12, 13], EnvCheckResult.INVALID_PYTHON,
         "不符合要求: Python版本不是3.9、3.10、3.11、3.12、13"),
        (os_type == 'Linux', EnvCheckResult.INVALID_OS, 
         "不符合要求: 操作系统类型不是Linux"),
        (arch in [a.value for a in CpuArchitecture], EnvCheckResult.INVALID_ARCH,
         f"不符合要求: 处理器架构不支持(需要{', '.join([a.value for a in CpuArchitecture])})")
    ]
    
    for is_valid, error_result, error_msg in validations:
        if not is_valid:
            logger.error(error_msg)
            return error_result

    # 环境检查通过，进行后续操作
    logger.info("环境符合运行要求")
    asyncio.run(process_so_file(file_name, py_minor, arch, container_type))
    return EnvCheckResult.SUCCESS


class RetryCounter:
    """重试计数器类"""
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
    
    def reset(self):
        self.count = 0
    
    def exceeded(self, max_retries):
        return self.count >= max_retries

retry_counter = RetryCounter()

@exception_handler
async def process_so_file(filename: str, py_v: int, cpu_info: str, container_type: Optional[ContainerType]) -> bool:
    """处理.so文件，包含重试逻辑"""
    if retry_counter.exceeded(config.max_retries):
        logger.error(f"已达到最大重试次数({config.max_retries})，停止尝试")
        return False
    if not os.path.exists(filename):
        logger.info(f"文件{filename}不存在，正在下载...")
        check_result = await download_so_file(filename, py_v, cpu_info, container_type)
    else:
        check_result = True
    if not check_result:
        logger.info(f"文件{filename}不存在，退出执行程序！")
        return False
    if container_type.value == ContainerType.ALPINE:
        fix_missing_libs(filename)
    try:
        # 动态导入.so文件
        import importlib.util
        spec = importlib.util.spec_from_file_location("common", filename)
        if spec is None or spec.loader is None:
            raise ImportError(f"无法加载模块规范: {filename}")
        
        common_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(common_module)
        
        # 检查是否有main函数
        if hasattr(common_module, 'main'):
            main_func = getattr(common_module, 'main')
            await main_func(config.script_name)
        else:
            logger.info(f"模块 {filename} 加载成功，但没有找到main函数")
        
        retry_counter.reset()
        return True
    except ImportError as e:
        logger.error(f"导入{filename}失败: {e}")
        retry_counter.increment()
        if os.path.exists(filename):
            os.remove(filename)
        return await download_so_file(filename, py_v, cpu_info, container_type)
    except Exception as e:
        logger.error(f"执行{filename}失败: {e}")
        retry_counter.increment()
        if os.path.exists(filename):
            os.remove(filename)
        return await download_so_file(filename, py_v, cpu_info, container_type)


@exception_handler
async def download_so_file(filename: str, py_v: int, cpu_info: str, container_type: Optional[ContainerType]) -> bool:
    """异步下载.so文件"""
    file_base_name = os.path.splitext(filename)[0]

    # 确定下载URL，使用命令行参数指定的代理URL
    base_download_url = get_download_url()
    url = build_download_url(base_download_url, file_base_name, py_v, cpu_info, container_type)
    if not url:
        return False
    logger.info(f"正在从 {url} 下载文件...")
    # 使用aiohttp下载并显示进度条
    success = await download_with_progress(url, filename)

    if success:
        logger.info(f"文件下载成功: {filename}")
        return True
    # 下载失败
    logger.error(f"下载失败: {url}")
    if os.path.exists(filename):
        os.remove(filename)
    return False


def get_download_url() -> str:
    """根据容器类型获取下载URL"""
    proxy_url = config.proxy_url
    # 如果使用了自定义代理（不是默认代理），构建代理URL
    return f"{proxy_url}{BASE_URL}"


def fix_missing_libs(so_path: str):
    """自动检测缺失库并创建软链（仅 Alpine）"""
    if not Path(so_path).exists():
        logger.warning(f"{so_path} 不存在，无法检测依赖")
        return
    try:
        # ldd 检查动态依赖
        result = subprocess.run(["ldd", so_path], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"执行ldd命令失败: {e}")
        return
    except Exception as e:
        logger.error(f"修复缺失库失败: {e}")
        return
    # 提取缺失的库
    missing_libs = [
        line.split()[0]
        for line in result.stdout.splitlines()
        if "not found" in line
    ]
    if not missing_libs:
        logger.info("没有缺失的依赖库")
        return

    logger.info(f"检测到缺失库: {missing_libs}")

    # 处理每个缺失的库
    for lib in missing_libs:
        handle_missing_lib(lib)

def handle_missing_lib(lib: str):
    """处理单个缺失的库"""
    # 从缺失库名去掉版本号进行匹配
    lib_base = lib.split(".so")[0] + ".so"
    try:
        # 在系统里查找可用同名库
        find_result = subprocess.run(
            ["find", "/usr", "-name", f"{lib_base}*"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        logger.warning(f"查找库 {lib} 失败: {e}")
        return
    except Exception as e:
        logger.error(f"查找库 {lib} 时发生错误: {e}")
        return

    paths = find_result.stdout.splitlines()
    if not paths:
        logger.warning(f"未找到 {lib} 对应的系统库，请手动安装")
        return
    source = paths[0]
    target = Path("/usr/lib") / lib

    if target.exists():
        return
    try:
        os.symlink(source, target)
        logger.info(f"软链 {source} -> {target} 已创建")
    except FileExistsError:
        # 处理竞态条件：另一个进程可能已经创建了软链接
        logger.debug(f"软链 {target} 已存在")
    except OSError as e:
        logger.warning(f"创建软链 {source} -> {target} 失败: {e}")

def build_download_url(base_url: str, file_base_name: str, py_v: int, cpu_info: str, container_type: Optional[ContainerType]) -> Optional[str]:
    """构建下载URL"""
    if container_type == ContainerType.ALPINE:
        end_type = '_musl'
    else:
        end_type = ''
    if cpu_info in [CpuArchitecture.AARCH64.value, CpuArchitecture.ARMV8.value]:
        return f"{base_url}/{file_base_name}_3{py_v}_aarch64{end_type}.so"
    elif cpu_info in [CpuArchitecture.X86_64.value ,CpuArchitecture.x86.value]:
        return f"{base_url}/{file_base_name}_3{py_v}_{cpu_info}{end_type}.so"
    elif cpu_info == CpuArchitecture.ARMV7.value:
        return f"{base_url}/{file_base_name}_3{py_v}_armv7{end_type}.so"
    else:
        logger.error(f"不支持的CPU架构: {cpu_info}")
        return None


@exception_handler
async def download_with_progress(url: str, filename: str) -> bool:
    """使用aiohttp下载文件并显示进度条"""
    timeout = aiohttp.ClientTimeout(total=300, connect=30)  # 总超时5分钟，连接超时30秒

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"HTTP请求失败，状态码: {response.status}")
                    return False
                total_size = int(response.headers.get('content-length', 0))
                return await save_file_with_progress(response, filename, total_size)
    except aiohttp.ClientError as e:
        logger.error(f"网络连接错误: {e}")
        return False
    except asyncio.TimeoutError:
        logger.error("下载超时")
        return False


async def save_file_with_progress(response, filename: str, total_size: int) -> bool:
    """保存文件并显示进度条"""
    downloaded_size = 0
    chunk_size = 8192

    try:
        async with aiofiles.open(filename, 'wb') as f:
            async for chunk in response.content.iter_chunked(chunk_size):
                await f.write(chunk)
                downloaded_size += len(chunk)
                update_progress_bar(downloaded_size, total_size)
        print()  # 换行

        # 验证文件大小
        if total_size > 0 and downloaded_size != total_size:
            logger.error(f"文件大小不匹配: 期望{total_size}字节，实际{downloaded_size}字节")
            return False

        # 验证文件是否为空
        if downloaded_size == 0:
            logger.error("下载的文件为空")
            return False

        return True
    except Exception as e:
        logger.error(f"保存文件失败: {e}")
        return False


def update_progress_bar(downloaded_size: int, total_size: int) -> None:
    """更新并显示下载进度条"""
    if total_size == 0:
        return

    progress = downloaded_size / total_size
    bar_length = 30
    filled_length = int(bar_length * progress)
    bar = '=' * filled_length + ' ' * (bar_length - filled_length)

    # 格式化大小显示
    def format_size(size):
        if size >= 1024 * 1024:
            return f"{size / (1024 * 1024):.2f}MB"
        return f"{size / 1024:.2f}KB"

    size_str = f"{format_size(downloaded_size)}/{format_size(total_size)}"
    print(f"\r下载进度: [{bar}] {int(progress * 100)}% {size_str}", end='', flush=True)


def main():
    """主函数"""
    try:
        # 更新日志级别
        logger.setLevel(getattr(logging, config.log_level))

        logger.info("启动代码执行器...")

        # 设置环境变量
        set_environment()

        result = check_environment()
        if result == EnvCheckResult.SUCCESS:
            logger.info("执行完成")
        else:
            logger.error(f"执行失败: {result.value}")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("用户中断执行")
        sys.exit(0)
    except Exception as e:
        logger.error(f"执行过程中发生错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
