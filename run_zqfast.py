# 中青快应用 邀请code http://kyy.baertt.com/h5/fastAppWeb/invite/invite_ground_2.html?share_uid=1040776341&channel=c8000
# author @wangquanfugui233
# cron 一天一次 一次3毛，自动提现 微信支付宝都可以
# 已知 青龙2.16.2 python3.10.13以上不能运行，我是2.16.2 python3.10.11
# 抓userinfo? 只要问号后面的参数就行 
# 变量    自动提现： 1是微信 0是支付宝，不填不行,多账户就@分开
# export zqurl='zzzzzz#1@cccccccccc#0'


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
            import aiozqfast_310_x86 as zq
            asyncio.run(zq.main())
        else:
            github_url = f'https://raw.fgit.cf/wyourname/wool/master/{so_file}'
            subprocess.run(['curl', '-o', so_file, github_url])
            run_so_file(so_file)

if __name__ == '__main__':
    run_so_file("aiozqfast_310_x86.so")