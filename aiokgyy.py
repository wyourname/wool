"""
用我脚本怕黑号的,大可不必用我的,请删除脚本,觉得自己目前的脚本还行的也请忽略,多有得罪请勿见怪

提现的openid,去提现页面,点一下提现至微信就能抓到的了nickname也一样
url?后面的xxxx即可只要xxxx
【包含】   《dfid=&appid=&token=&mid=&clientver=&from=client&clienttime=&userid&uuid...这几个参数即可》 【不要求排序相同】
export kgyycks='xxxx#openid#nickname#ture=2

ture=2 提2块
ture=5 5块
ture=10 10
ture=20 20
其他不提

一天8小时 半小时一次
"""

import os
import asyncio
import sys

so_file = 'aiokgyy_310_x86.so'
if os.path.exists(so_file):
    print(so_file)  
    print(f"python版本：{sys.version}，so要求3.10.x,其他版本可能无法运行")
else:
    import subprocess
    print(f"python版本：{sys.version}，so要求3.10.x,其他版本可能无法运行")
    print(f"{so_file} 文件不存在")
    github_url = 'https://raw.kgithub.com/wangquanfugui233/zq_fast/master/aiokgyy_310_x86.so'
    subprocess.run(['curl', '-o', so_file, github_url])
    
from aiokgyy_310_x86 import *
asyncio.run(main())
