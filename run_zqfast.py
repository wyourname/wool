# 中青快应用
# author @wangquanfugui233
# cron 一天一次 一次3毛，自动提现 微信支付宝都可以
# 抓userinfo? 只要问号后面的参数就行 
# 变量    自动提现： 1是微信 0是支付宝，不填不行,多账户就@分开
# export zqurl='zzzzzz#1@cccccccccc#0'

"""
使用脚本,需要注意5点,这很重要
1.【怕黑号的，真诚的，恳请您不要用】
2.觉得钱少的浪费时间的,请您删除脚本即可，我怕浪费您的空间
3.代码是公开的，你可以自己二次修改，如果你是大佬，请放过小弟的脚本,因为我知道你有能力写的更好
4.如果您使用了别的作者的脚本，请勿拿我的和他人的做对比，因为我写的不好，也请您删除我的脚本，因为我的脚本会让你浪费一定的时间
5.请阅览后24小时自行删除脚本


自动提现： 1是微信 0是支付宝，不填不行,多账户就@分开
export zqurl='zzzzzz#1@cccccccccc#0'
抓这个 https://user.youth.cn/v1/user/userinfo.json?zzzzzzzzz...
只要?后面的
"""


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
            github_url = f'https://raw.kgithub.com/wangquanfugui233/wool/master/{so_file}'
            subprocess.run(['curl', '-o', so_file, github_url])
            run_so_file(so_file)

if __name__ == '__main__':
    run_so_file("aiozqfast_310_x86.so")