import asyncio
import aiohttp
from typing import Optional, Dict 
from urllib.parse import urlparse
import time,random
import sys
import os

"""
模板a 采用aiohttp: 作用是 存在不同url,不同host,能自主的选择host，且基础headers变量保持不变，其他headers参数可以自由选择
         
request(url,'get或者post','data可以为空','add_headers为往请求头追加元素必须为字典',headers为替换头)

headers为替换头,当headers 需要修改的参数太多还不如重新弄一个，可以选用这个替换默认头

host 不需要你设置，根据url自动筛选，或者add_headers添加host就会更新了

当 headers里有cookie怎么设置
run方法定义类变量 self.cookie = cookie
async def other_method(self):
    add_header= {"cookie":self.cookie}
    await requests(url,add_headers=add_header)

类内部用async 实现并发可以如下
tasks1 = [self.request(url) for _ in range(并发数)]
responses1 = await asyncio.gather(*tasks1)
for response in responses1:
    print(response)


"""


class template:
    def __init__(self) -> None:
        """
        new model
         
        """
        self.sessions = aiohttp.ClientSession()
        # self._default_headers={   # 没有那么多参数就用这就行了把requst里的注释掉就好了
        #     # 'Host': host,
        #     'User-Agent': 'com.ss.android.ugc.live/260301 (Linux; U; Android 13; zh_CN; M2012K11AC; Build/TKQ1.220829.002; Cronet/TTNetVersion:f2f67850 2023-07-04 QuicVersion:4d847ea3 2023-05-09)',
        #     'Connection': 'close',
        #     'Accept': '*/*',
        #     'Accept-Encoding': 'gzip, deflate',
        #     'sdk-version': '2',
        #     'passport-sdk-version': '203107',
        #     'Cookie': ''
        # }

    
    async def close(self):
        await self.sessions.close()

    async def request(self, url, method='get', data=None, add_headers: Optional[Dict[str, str]] = None, headers=None, dtype='json', max_retries=3):
        host = urlparse(url).netloc
        _default_headers = {
            'Host': host,
            'User-Agent': 'ua',
            'Connection': 'close',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
        }
        retries = 0
        while retries < max_retries:
            try:
                request_headers = headers or _default_headers
                if add_headers:
                    request_headers.update(add_headers)
                async with getattr(self.sessions, method)(url, headers=request_headers, data=data) as response:
                    if response.status == 200:
                        if dtype == 'json':
                            return await response.json()
                        else:
                            return await response.text()
                    else:
                        print(f"请求失败状态码：{response.status}")
                        # 可以选择休眠一段时间再重试，以避免频繁请求
                        await asyncio.sleep(random.randint(3,5))  # 休眠1秒钟
            except Exception as e:
                print(f"请求出现错误：{e}")
                await asyncio.sleep(random.randint(3,5))  # 休眠1秒钟
            retries += 1
        print(f"无法完成请求，已达到最大重试次数 ({max_retries})")
        return None    

    async def expamget(self):
        # Here you can write some code.
        pass

    async def post(self):
        # Here you can write some code.
        pass

    async def run(self,index, ck:str):#
        # This is the starting point of the program.
        # You can call functions inside the class here.
        # Here you can write some code.
        await self.close()

async def check_env():
    # 这里可以写完善一点的获取环境变量功能
    cks = os.getenv('cks')
    if cks is None:
        print("你没有填写cks")
        exit()
    correct_data = []
    for index ,ck in enumerate(cks.split("@")):
        # 也许这里可以添加你的变量检测是否合规
        # Here you can write some code.
        correct_data.append(ck)
    return correct_data

async def main():
    cks_list = await check_env()
    # 检查是否存在环境变量 multi
    use_concurrency = os.environ.get('multi', 'false').lower() == 'true'
    tasks = []
    for index, ck in enumerate(cks_list):
        abc = template()
        task = abc.run(index, ck)
        tasks.append(task)
    if use_concurrency:  # 如果是true 那么就执行并发
        await asyncio.gather(*tasks)  # 并发执行任务
    else:  # 如果是false 那么就串行执行
        for task in tasks:
            await task  

if __name__ == '__main__':
    asyncio.run(main())
