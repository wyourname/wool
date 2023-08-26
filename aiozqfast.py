"""
zq快应用
使用脚本,需要注意5点,这很重要
1.【怕黑号的，真诚的，恳请您不要用】
2.觉得钱少的浪费时间的,请您删除脚本即可，我怕浪费您的空间
4.如果您使用了别的作者的脚本，请勿拿我的和他人的做对比，因为我写的不好，也请您删除我的脚本，因为我的脚本会让你浪费一定的时间
5.请阅览后24小时自行删除脚本

自动提现： 1是微信 0是支付宝，不填不行,多账户就@分开
export zqurl='zzzzzz#1@cccccccccc#0'
抓这个 https://user.youth.cn/v1/user/userinfo.json?zzzzzzzzz...
只要?后面的
这更新基本就是没提就自动提
一天一次

"""

import os
import asyncio
import sys

so_file = 'aiozqfast_310_x86.so'
if os.path.exists(so_file):
    print(so_file)  
    print(f"python版本：{sys.version}，so要求3.10.x,其他版本可能无法运行")
else:
    import subprocess
    print(f"python版本：{sys.version}，so要求3.10.x,其他版本可能无法运行")
    print(f"{so_file} 文件不存在")
    github_url = 'https://raw.githubusercontent.com/your_username/your_repository/your_branch/aiozqfast_310_x86.so'
    subprocess.run(['curl', '-o', so_file, github_url])
    
from aiozqfast_310_x86 import *
asyncio.run(main())
