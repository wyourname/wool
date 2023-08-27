# 抖音火山
# author @wangquanfugui233
# cron 一天多次，看你的号怎么样，我的号能跑18小时，普通的号就几小时就跑完了,半小时一次吧
# export hscks='url?后面的参数#cookie中的sessionid#x-argus#x-ladon'

import asyncio
import platform
import sys, os, subprocess

def check_environment():
    v, o, a = sys.version_info, platform.system(), platform.machine()
    print(f"Python版本: {v.major}.{v.minor}.{v.micro}, 操作系统类型: {o}, 处理器架构: {a}")
    if (v.minor in [9, 10]) and o == 'Linux' and a == 'x86_64':
        print("符合运行要求,3.9可能能跑不确定")
        return True
    else:
        if not (v.minor in [9, 10]):
            print("不符合要求: Python版本不是3.9或3.10")
        if o != 'Linux':
            print("不符合要求: 操作系统类型不是Linux")
        if a != 'x86_64':
            print("不符合要求: 处理器架构不是x86_64")
        return False
    
def check_so_file(filename):
    if os.path.exists(filename):
        print(f"{filename} 存在")
        return True
    else:
        print(f"{filename} 不存在")
        return False
    
def run_so_file(so_file):
    if check_environment():
        if check_so_file(so_file):
            import aiohs_310_x86 as hs
            asyncio.run(hs.main())
        else:
            github_url = f'https://raw.kgithub.com/wangquanfugui233/wool/master/{so_file}'
            subprocess.run(['curl', '-o', so_file, github_url])
            run_so_file(so_file)

if __name__ == '__main__':
    run_so_file("aiohs_310_x86.so")


