"""
用我脚本怕黑号的,大可不必用我的,请删除脚本,觉得自己目前的脚本还行的也请忽略,多有得罪请勿见怪
export hscks="url后面的参数就行#cookie#x-argus#x-ladon"
带自动提现需要提前绑定好支付宝
帮我助力一下也好啊

8【长按翻译可复制】看别人领包红不如来 n:/ 亲自体验ϒɪƝʠȌƯ[调皮]Shan颁huÕxoxo却此整比令很说方瞑


"""

import os
import asyncio
import sys

so_file = 'aiohs_310_x86.so'
if os.path.exists(so_file):
    print(so_file)  
    print(f"python版本：{sys.version}，so要求3.10.x,其他版本可能无法运行")
else:
    import subprocess
    print(f"python版本：{sys.version}，so要求3.10.x,其他版本可能无法运行")
    print(f"{so_file} 文件不存在")
    github_url = 'https://raw.kgithub.com/wangquanfugui233/zq_fast/master/aiohs_310_x86.so'
    subprocess.run(['curl', '-o', so_file, github_url])
    
from aiohs_310_x86 import *
asyncio.run(main())
