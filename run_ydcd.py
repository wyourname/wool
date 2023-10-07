"""
new Env("有道词典")
new cron("1 8 * * *")
export YDCD_COOKIES='cookie#1'
1代表提现一元
10代表10元
不提就改0
垃圾毛来的不用也罢
dict.youdao.com下的cookie
和旧脚本相比就是改成aiohttp
改善报错信息
提示no login 的时候打开app刷新下就行不需要重抓改天有空再写刷新cookie
有需要并发抢1块钱的可以和我说,我加个开关就行代码已写好
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
        import aioydcd as yd
        asyncio.run(yd.main())
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
        print(f"下载失败{filename}文件失败")

if __name__ == '__main__':
    check_environment('aioydcd.so')
