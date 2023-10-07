# cython: language_level=3
# author@ wangquanfugui233

"""
代码请勿用于非法盈利,若用于非法盈利或私自修改代码所造成的损失一切与本人无关,该代码仅用于学习交流,请下载阅览的24小时内删除代码
使用前请认真阅读仓库声明
new Env("农好优")
export nhycks='手机号#密码@...'
邀请 http://wap.nonghaoyou.cn/Public/reg/recom/289680
签到需要支付宝授权实名挂着玩

"""

import asyncio
import platform
import sys
import os
import subprocess


def check_environment(file_name):
    v, o, a = sys.version_info, platform.system(), platform.machine()
    print(f"Python版本: {v.major}.{v.minor}.{v.micro}, 操作系统类型: {o}, 处理器架构: {a}")
    if (v.minor in [10]) and o == 'Linux' and a in ['x86_64', 'aarch64', 'armv8']:
        print("符合运行要求,arm8没试过不知道行不行")
        check_so_file(file_name, v.minor, a)
    else:
        if not (v.minor in [10]):
            print("不符合要求: Python版本不是3.10")
        if o != 'Linux':
            print("不符合要求: 操作系统类型不是Linux")
        if a != 'x86_64':
            print("不符合要求: 处理器架构不是x86_64 aarch64 armv8")


def check_so_file(filename, py_v, cpu_info):
    if os.path.exists(filename):
        print(f"{filename} 存在")
        import nhy as n
        asyncio.run(n.main())
    else:
        print(f"{filename} 不存在,前往下载文件")
        download_so_file(filename, py_v, cpu_info)


def download_so_file(filename, py_v, cpu_info):
    file_base_name = os.path.splitext(filename)[0]
    if cpu_info in ['aarch64', 'armv8']:
        github_url = f'https://raw.fgit.cf/wyourname/wool/master/other/{file_base_name}_3{py_v}_aarch64.so'
    if cpu_info == 'x86_64':
        github_url = f'https://raw.fgit.cf/wyourname/wool/master/other/{file_base_name}_3{py_v}_{cpu_info}.so'
    # print(github_url)
    result = subprocess.run(['curl', '-o', filename, github_url])
    if result.returncode == 0:
        print(f"下载完成：{filename},调用check_so_file funtion")
        check_so_file(filename,py_v,cpu_info)
    else:
        print(f"下载失败：{filename}")

if __name__ == '__main__':
    check_environment('nhy.so')