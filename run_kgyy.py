# 酷狗音乐
# author @wangquanfugui233
# cron */30 8-18 * * *
# 抓酷狗gateway的url的带有dfid=&appid=&token=&mid=&clientver=&from=client&clienttime=&userid&uuid=有这几个就行，不要求排序，脚本自动的,
# 抓提现的openid,去提现页面,点一下提现至微信就能抓到的了，nickname 也一样,ture=2提现2块 ture=5就提现5块，依次类推
# 变量 export kgyycks='url?后面的参数，不要url?只要参数#openid#nickname#ture=2'


import asyncio
import platform
import sys
import os
import subprocess


def check_environment(file_name):
    v, o, a = sys.version_info, platform.system(), platform.machine()
    print(f"Python版本: {v.major}.{v.minor}.{v.micro}, 操作系统类型: {o}, 处理器架构: {a}")
    if (v.minor in [10]) and o == 'Linux' and a in ['x86_64', 'aarch64', 'armv8']:
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
        import aiokgyy as kg
        asyncio.run(kg.main())
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
        print(f"下载完成：{filename},调用checl_so_file funtion")
        check_so_file(filename,py_v,cpu_info)
    else:
        print(f"下载失败：{filename}")

if __name__ == '__main__':
    check_environment('aiokgyy.so')
