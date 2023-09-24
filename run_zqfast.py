# 中青快应用 邀请code http://kyy.baertt.com/h5/fastAppWeb/invite/invite_ground_2.html?share_uid=1040776341&channel=c8000
# author @wangquanfugui233
# cron 一天一次 一次3毛，自动提现 微信支付宝都可以
# 已知 青龙2.16.2 python3.10.13以上不能运行，我是2.16.2 python3.10.11
# 抓userinfo? 只要问号后面的参数就行 
# 变量    自动提现： 1是微信 0是支付宝，不填不行,多账户就@分开
# export zqurl='zzzzzz#1@cccccccccc#0'


import asyncio
import platform
import sys
import os
import subprocess


def check_environment(file_name):
    v, o, a = sys.version_info, platform.system(), platform.machine()
    print(f"Python版本: {v.major}.{v.minor}.{v.micro}, 操作系统类型: {o}, 处理器架构: {a}")
    if (v.minor in [10]) and o == 'Linux' and a in ['x86_64', 'aarch64', 'armv8-a']:
        print("符合运行要求")
        check_so_file(file_name, v.minor, a)
    else:
        if not (v.minor in [10]):
            print("不符合要求: Python版本不是3.10")
        if o != 'Linux':
            print("不符合要求: 操作系统类型不是Linux")
        if a != 'x86_64':
            print("不符合要求: 处理器架构不是x86_64 aarch64 armv8-a")


def check_so_file(filename, py_v, cpu_info):
    if os.path.exists(filename):
        print(f"{filename} 存在")
        import aiozqfast as zq
        asyncio.run(zq.main())
    else:
        print(f"{filename} 不存在,前往下载文件")
        download_so_file(filename, py_v, cpu_info)


def download_so_file(filename, py_v, cpu_info):
    file_base_name = os.path.splitext(filename)[0]
    if cpu_info in ['aarch64', 'armv8-a']:
        github_url = f'https://raw.fgit.cf/wyourname/wool/master/other/{file_base_name}_3{py_v}_aarch64.so'
    if cpu_info == 'x86_64':
        github_url = f'https://raw.fgit.cf/wyourname/wool/master/other/{file_base_name}_3{py_v}_{cpu_info}.so'
    # print(github_url)
    result = subprocess.run(['curl', '-o', filename, github_url])
    if result.returncode == 0:
        print(f"下载完成：{filename},调用checl_so_file funtion")
        check_so_file(filename,py_v,cpu_info)
    else:
        print(f"下载失败：{filename}")

if __name__ == '__main__':
    check_environment('aiozqfast.so')
