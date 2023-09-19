# 中青快应用提现30，给老哥单独做的提现
# 0 支付宝 1微信
# export zqtxrl='zzzzzz#0@cccccccccc#1'


import asyncio
import platform
import sys, os, subprocess

def check_environment():
    v, o, a = sys.version_info, platform.system(), platform.machine()
    print(f"Python版本: {v.major}.{v.minor}.{v.micro}, 操作系统类型: {o}, 处理器架构: {a}")
    if (v.minor in [10]) and o == 'Linux' and a == 'x86_64':
        print("符合运行要求")
        return True
    else:
        if not (v.minor in [10]):
            print("不符合要求: Python版本不是3.10")
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
            import zqtx30 as zq
            asyncio.run(zq.main())
        else:
            github_url = f'https://raw.fgit.cf/wyourname/wool/master/zqtx30.so'
            subprocess.run(['curl', '-o', so_file, github_url])
            run_so_file(so_file)

if __name__ == '__main__':
    run_so_file("zqtx30.so")
