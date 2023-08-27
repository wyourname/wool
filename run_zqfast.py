# 中青快应用
# author @wangquanfugui233
# cron 一天一次 一次3毛，自动提现 微信支付宝都可以
# 抓userinfo? 只要问号后面的参数就行 
# 变量    自动提现： 1是微信 0是支付宝，不填不行,多账户就@分开
# export zqurl='zzzzzz#1@cccccccccc#0'

# 我想在这里吐槽qq群里一两个白嫖的人，用着我开源脚本，还骂着我的人。
# 怎么滴？写出来给给你用，你用的是我写的第一个版本，多账号用不了是因为我没测试过，
# 你自己又不会类，自己不会函数封装，不会改，还怪我代码写的差？写了新版你又不用，真就白嫖屁事多
# 我说我本意是分享，你说我偷撸，觉得我没那么高大上，我确实没那么高大上，但是请你认清一下自己，你又不是我亲哥，我干嘛分享给你，
# 我没发出来是因为群里大佬的脚本收益比我高，我就不好意发垃圾脚本出来，我怕你们嘲笑
# 还有你们真是白眼狼，写个脚本不容易，这个一个人头能让我挣0.2，你们却没一个走我的邀请，还说不吃邀请，
# 拜托大哥，我本来就没啥毛薅，也没有上过什么付费车跑抖音快手，我就想多挣2毛钱，仅此而已，我是一个吝啬的人，
# 哪怕是花钱买脚本我都舍不得，我能自己写就自己写，不能我也绝对不上车


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
            import aiozqfast_310_x86 as zq
            asyncio.run(zq.main())
        else:
            github_url = f'https://raw.kgithub.com/wangquanfugui233/wool/master/{so_file}'
            subprocess.run(['curl', '-o', so_file, github_url])
            run_so_file(so_file)

if __name__ == '__main__':
    run_so_file("aiozqfast_310_x86.so")