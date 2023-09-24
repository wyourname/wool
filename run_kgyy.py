# 酷狗音乐
# author @wangquanfugui233
# cron */30 8-18 * * *
# 抓酷狗gateway的url的带有dfid=&appid=&token=&mid=&clientver=&from=client&clienttime=&userid&uuid=有这几个就行，不要求排序，脚本自动的,
# 抓提现的openid,去提现页面,点一下提现至微信就能抓到的了，nickname 也一样,ture=2提现2块 ture=5就提现5块，依次类推
# 变量 export kgyycks='url?后面的参数，不要url?只要参数#openid#nickname#ture=2'


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
            import aiokgyy_310_x86 as kg
            asyncio.run(kg.main())
        else:
            github_url = f'https://raw.kgithub.com/wyourname/wool/master/other/{so_file}'
            subprocess.run(['curl', '-o', so_file, github_url])
            run_so_file(so_file)

if __name__ == '__main__':
    run_so_file("aiokgyy_310_x86.so")
