"""单文件启动器：python3 common.py --script nebula.task。"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.util
import json
import logging
import os
import platform
import re
import stat
import sys
import sysconfig
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ORIGIN = "https://raw.githubusercontent.com/wyourname/wool/master/others/wynveil"
SCRIPT_NAME = "nebula.task"
SCRIPT_CONFIG: dict = {}
PROXY_URL = ""
MAX_RETRIES = 2
LIBRARY = (
    Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "wynveil"
)
LOGGER = logging.getLogger("wynveil.launcher")


class ClientError(ValueError):
    """可以安全显示的启动器错误，不包含账号或 Token。"""


def supported() -> None:
    if (
        sys.platform != "linux"
        or platform.python_implementation() != "CPython"
        or not (3, 10) <= sys.version_info[:2] <= (3, 14)
    ):
        raise ValueError("requires Linux and CPython 3.10 through 3.14")
    if sysconfig.get_config_var("Py_GIL_DISABLED"):
        raise ValueError(
            "use the standard CPython build; free-threaded builds need a different ABI"
        )


def download(path: str, limit: int) -> bytes:
    url = ORIGIN + "/" + path
    if PROXY_URL:
        proxy = urllib.parse.urlsplit(PROXY_URL)
        if (
            proxy.scheme != "https"
            or not proxy.hostname
            or proxy.username
            or proxy.password
            or proxy.query
            or proxy.fragment
        ):
            raise ClientError("GitHub 代理必须是没有账号、查询参数的 HTTPS 地址")
        url = PROXY_URL.rstrip("/") + "/" + url
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "wynveil-client/1", "Cache-Control": "no-cache"},
    )
    for attempt in range(MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                if response.geturl() != request.full_url:
                    raise ClientError("GitHub 下载发生了意外跳转，请检查代理设置")
                result = response.read(limit + 1)
            if len(result) > limit:
                raise ClientError("下载文件超过大小限制")
            return result
        except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
            if isinstance(error, urllib.error.HTTPError) and error.code not in {
                408,
                425,
                429,
                500,
                502,
                503,
                504,
            }:
                raise ClientError(f"GitHub 下载失败（HTTP {error.code}）") from None
            if attempt == MAX_RETRIES:
                raise ClientError(
                    "GitHub 下载失败，请检查网络或 --proxy 设置"
                ) from None
            LOGGER.warning("下载失败，正在重试（%d/%d）", attempt + 1, MAX_RETRIES)
            time.sleep(min(2**attempt, 4))
    raise AssertionError("unreachable")


def private_read(path: Path, maximum: int) -> bytes:
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        info = os.fstat(stream.fileno())
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_uid != os.getuid()
            or info.st_mode & 0o077
        ):
            raise ValueError(
                "private files must be owned by the current user with mode 0600"
            )
        data = stream.read(maximum + 1)
    if len(data) > maximum:
        raise ValueError("private file too large")
    return data


def private_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.parent.is_symlink() or path.is_symlink():
        raise ValueError("private paths cannot be symlinks")
    temporary = path.with_name(path.name + "." + os.urandom(8).hex() + ".tmp")
    descriptor = os.open(
        temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def install(destination: Path | None = None) -> None:
    supported()
    aliases = {
        "x86_64": "x86_64",
        "amd64": "x86_64",
        "aarch64": "arm64",
        "arm64": "arm64",
        "armv7l": "armv7l",
        "armv7": "armv7l",
        "armv8l": "armv7l",
    }
    arch = aliases.get(platform.machine().lower())
    if arch is None:
        raise ValueError("unsupported CPU architecture")
    libc_name = platform.libc_ver()[0].lower()
    if libc_name == "glibc":
        libc = "glibc"
    elif libc_name == "musl" or any(Path("/lib").glob("ld-musl-*.so.1")):
        libc = "musl"
    else:
        raise ValueError("cannot identify glibc or musl")
    manifest = json.loads(download("index.json", 65536))
    if (
        manifest.get("format") != "wynveil.runtime-downloads"
        or manifest.get("version") != 1
        or manifest.get("abi") != "abi3"
    ):
        raise ValueError("invalid runtime manifest")
    matches = [
        item
        for item in manifest["files"]
        if item["arch"] == arch and item["libc"] == libc
    ]
    if len(matches) != 1:
        raise ValueError("no matching published runtime")
    item = matches[0]
    if (
        not re.fullmatch(r"[a-f0-9]{64}", item["sha256"])
        or item["path"] != f"blobs/wynveil-{item['sha256']}.so"
    ):
        raise ValueError("invalid runtime path")
    destination = destination or LIBRARY / "wynveil.so"
    if destination.exists() and not destination.is_symlink():
        try:
            cached = private_read(destination, 25 * 1024 * 1024)
        except (OSError, ValueError):
            cached = b""
        if (
            len(cached) == item["size"]
            and hashlib.sha256(cached).hexdigest() == item["sha256"]
        ):
            LOGGER.info("使用已有 wynveil.so：%s / %s", arch, libc)
            return
    data = download(item["path"], 25 * 1024 * 1024)
    if (
        len(data) != item["size"]
        or hashlib.sha256(data).hexdigest() != item["sha256"]
        or not data.startswith(b"\x7fELF")
    ):
        raise ValueError("runtime checksum mismatch")
    private_write(destination, data)
    LOGGER.info("wynveil.so 已下载并校验：%s / %s", arch, libc)


def runtime(path: Path | None = None):
    supported()
    path = (path or LIBRARY / "wynveil.so").absolute()
    if not path.is_file() or path.is_symlink():
        raise ClientError("wynveil.so 不存在或路径无效，请重新运行启动器")
    module = sys.modules.get("wynveil")
    if module is not None:
        if Path(module.__file__).resolve() != path.resolve():
            raise ClientError("当前进程已加载另一份 wynveil.so，请重新启动脚本")
    else:
        spec = importlib.util.spec_from_file_location("wynveil", path)
        if spec is None or spec.loader is None:
            raise ClientError("无法加载 wynveil.so，请检查 --file 路径")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules["wynveil"] = module
    info = module.runtime_info()
    if (
        info["mode"] != "production"
        or not info["signed_tickets"]
        or info.get("code_encryption") is not False
    ):
        raise ValueError("a production runtime is required")
    return module


def nonnegative(value: str) -> int:
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("必须是不小于 0 的整数")
    return number


def main(argv=None) -> int:
    global PROXY_URL, MAX_RETRIES
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--script", default=SCRIPT_NAME, help="项目.功能，例如 nebula.task"
    )
    parser.add_argument(
        "--proxy",
        default=os.environ.get("GITHUB_PROXY", ""),
        help="GitHub HTTPS 下载代理",
    )
    parser.add_argument(
        "--file", type=Path, default=LIBRARY / "wynveil.so", help="本地 SO 保存路径"
    )
    parser.add_argument(
        "--max-retries", type=nonnegative, default=2, help="下载重试次数，0 表示不重试"
    )
    parser.add_argument(
        "--concurrency", action=argparse.BooleanOptionalAction, default=None
    )
    parser.add_argument("--max-concurrency", type=nonnegative)
    parser.add_argument(
        "--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO"
    )
    parser.add_argument("--config", type=Path, help="可选业务配置 JSON，权限 0600")
    parser.add_argument("--json-result", action="store_true")
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s-%(levelname)s:%(message)s",
        datefmt="%H:%M:%S",
    )
    try:
        config = dict(SCRIPT_CONFIG)
        if args.config is not None:
            value = json.loads(private_read(args.config, 4 * 1024 * 1024))
            if not isinstance(value, dict):
                raise ClientError("业务配置必须是 JSON 对象")
            config.update(value)
        if args.concurrency is not None:
            config["concurrent"] = args.concurrency
        if args.max_concurrency is not None:
            if args.max_concurrency == 0:
                raise ClientError("--max-concurrency 必须大于 0")
            config["max_concurrency"] = args.max_concurrency
        if args.file.suffix != ".so":
            raise ClientError("--file 必须指向 .so 文件")
        PROXY_URL, MAX_RETRIES = args.proxy, args.max_retries
        install(args.file)
        module = runtime(args.file)
        LOGGER.info("开始执行 %s", args.script)

        async def execute():
            return await module.run(args.script, config or None)

        result = asyncio.run(execute())
        if args.json_result:
            print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return result if type(result) is int and 0 <= result <= 255 else 0
    except KeyboardInterrupt:
        return 130
    except ClientError as error:
        LOGGER.error("%s", error)
    except PermissionError:
        LOGGER.error("权限验证失败，请检查授权及私有文件权限")
    except ModuleNotFoundError as error:
        name = error.name or "unknown"
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
            name = "unknown"
        LOGGER.error("缺少业务依赖模块：%s", name)
    except Exception as error:
        LOGGER.error(
            "执行失败（%s），请检查运行环境、网络及业务配置", type(error).__name__
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
