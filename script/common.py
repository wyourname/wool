"""
通用代码
这是一份傻逼代码，使用说明 随缘了,不接受小白
代码请勿用于非法盈利，一切与本人无关，该代码仅用于学习交流，请阅览下载24小时内删除代码
"""
SCRIPT_NAME = "test"  # 脚本名称 记得修改这里


DOWNLOAD_URL = 'https://files.doudoudou.top/?f=/script/others'
DOWNLOAD_URL2 = 'https://raw.githubusercontent.com/wyourname/wool/master/others'
import logging
import asyncio
import platform
import sys
import os
import subprocess

logging.basicConfig(level=logging.INFO)

def check_environment(file_name):
    v, o, a = sys.version_info, platform.system(), platform.machine()
    logging.info(f"Python版本: {v.major}.{v.minor}.{v.micro}, 操作系统类型: {o}, 处理器架构: {a}")
    if (v.minor in [9, 10, 11, 12]) and o == 'Linux' and a in ['x86_64', 'aarch64', 'armv8', 'armv7l']:
        logging.info("符合运行要求,ARMv7,ARMv8请自行尝试")
        check_so_file(file_name, v.minor, a)
    else:
        if not (v.minor in [9, 10, 11, 12]):
            logging.info("不符合要求: Python版本不是3.9 3.10 3.11 3.12中的一种")
            return
        if o != 'Linux':
            logging.info("不符合要求: 操作系统类型不是Linux")
            return
        if a not in ['x86_64', 'aarch64', 'armv8', 'armv7l']:
            logging.info("不符合要求: 处理器架构不是x86_64 aarch64 armv8 armv7中的一种")
            return

def check_so_file(filename, py_v, cpu_info):
    if os.path.exists(filename):
        logging.info(f"本仓库通用文件: {filename}存在")
        import common
        asyncio.run(common.main(SCRIPT_NAME))
    else:
        logging.info(f"本仓库通用文件: {filename}不在本地,将前往作者仓库拉取")
        download_so_file(filename, py_v, cpu_info)

def run_command(command):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    final_out = ''
    for line in process.stdout:
        line = line.strip()
        final_out = line
        if "%" in line:
            logging.info(line)
    process.stdout.close()
    process.wait()
    return process.returncode, final_out

def download_so_file(filename, py_v, cpu_info):
    file_base_name = os.path.splitext(filename)[0]
    if cpu_info in ['aarch64', 'armv8']:
        url = DOWNLOAD_URL + f'/{file_base_name}_3{py_v}_aarch64.so'
    elif cpu_info == 'x86_64':
        url = DOWNLOAD_URL + f'/{file_base_name}_3{py_v}_{cpu_info}.so'
    elif 'armv7' in cpu_info:
        url = DOWNLOAD_URL + f'/{file_base_name}_3{py_v}_armv7.so'
    command = ['curl', '-#', '-o', filename, '-w', '%{http_code}', url]
    result, stdout = run_command(command)
    if stdout == '200' and result == 0:
        logging.info(f"本仓库通用文件下载成功: {filename}")
        check_so_file(filename, py_v, cpu_info)
    else:
        logging.info(f"{filename}下载失败,请手动切换到备用下载url:{DOWNLOAD_URL2} 将DOWNLOAD_URL2改为DOWNLOAD_URL即可")
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    check_environment('common.so')

