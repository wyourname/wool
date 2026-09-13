"""Install and run wynveil. This client contains no code encryption or key issuer."""

from __future__ import annotations

import argparse
import asyncio
import getpass
import hashlib
import importlib
import json
import os
import platform
import re
import stat
import sys
import sysconfig
import urllib.request
from pathlib import Path

ORIGIN = "https://raw.githubusercontent.com/wyourname/wool/master/others/wynveil"
LIBRARY = (
    Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "wynveil"
)
LICENSE = (
    Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    / "wynveil/license.json"
)


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
    request = urllib.request.Request(
        ORIGIN + "/" + path,
        headers={"User-Agent": "wynveil-client/1", "Cache-Control": "no-cache"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        if response.geturl() != request.full_url:
            raise ValueError("download redirected unexpectedly")
        result = response.read(limit + 1)
    if len(result) > limit:
        raise ValueError("download too large")
    return result


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


def install() -> None:
    supported()
    aliases = {
        "x86_64": "x86_64",
        "amd64": "x86_64",
        "aarch64": "arm64",
        "arm64": "arm64",
        "armv7l": "armv7l",
        "armv7": "armv7l",
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
    data = download(item["path"], 25 * 1024 * 1024)
    if (
        len(data) != item["size"]
        or hashlib.sha256(data).hexdigest() != item["sha256"]
        or not data.startswith(b"\x7fELF")
    ):
        raise ValueError("runtime checksum mismatch")
    private_write(LIBRARY / "wynveil.so", data)
    print(f"wynveil 已安装：{arch} / {libc}，支持 Python 3.10–3.14")


def activate(token_file: Path | None, license_file: Path) -> None:
    token = (
        private_read(token_file, 512).decode().strip()
        if token_file
        else getpass.getpass("VToken（输入不显示）: ").strip()
    )
    if not re.fullmatch(r"[A-Za-z0-9_-]{43}", token):
        raise ValueError("invalid VToken format")
    value = {
        "format": "common.license",
        "version": 1,
        "subject": "vtoken-" + hashlib.sha256(token.encode()).hexdigest(),
        "token": token,
    }
    private_write(license_file, json.dumps(value).encode())
    print("VToken 已保存；运行脚本时会在线核验授权并绑定设备。")


def runtime():
    supported()
    path = LIBRARY / "wynveil.so"
    if not path.is_file() or path.is_symlink():
        raise ValueError("run the install command first")
    sys.path.insert(0, str(LIBRARY))
    module = importlib.import_module("wynveil")
    info = module.runtime_info()
    if (
        info["mode"] != "production"
        or not info["signed_tickets"]
        or info.get("code_encryption") is not False
    ):
        raise ValueError("a production runtime is required")
    return module


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("install")
    sub.add_parser("info")
    sub.add_parser("device")
    activation = sub.add_parser("activate")
    activation.add_argument("--token-file", type=Path)
    activation.add_argument("--license-file", type=Path, default=LICENSE)
    run = sub.add_parser("run")
    run.add_argument("script")
    run.add_argument("--config", type=Path)
    run.add_argument("--license-file", type=Path, default=LICENSE)
    run.add_argument("--json-result", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "install":
            install()
        elif args.command == "activate":
            activate(args.token_file, args.license_file)
        elif args.command == "info":
            print(json.dumps(runtime().runtime_info()))
        elif args.command == "device":
            print(runtime().device_public_key())
        elif args.command == "run":
            config = (
                json.loads(private_read(args.config, 4 * 1024 * 1024))
                if args.config
                else None
            )
            if config is not None and not isinstance(config, dict):
                raise ValueError("configuration must be a JSON object")
            os.environ["COMMON_LICENSE_FILE"] = str(args.license_file.absolute())
            module = runtime()

            async def execute():
                return await module.run(args.script, config)

            result = asyncio.run(execute())
            if args.json_result:
                print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    except KeyboardInterrupt:
        return 130
    except Exception as error:
        # Application exceptions can contain credentials; don't print their text.
        print(
            f"wynveil 操作失败（{type(error).__name__}）；请检查平台、网络、配置和授权。",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
