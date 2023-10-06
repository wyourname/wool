import asyncio
import aiohttp
from typing import Optional, Dict 
from urllib.parse import urlparse
import time,random
from datetime import datetime
import os



class template:
    def __init__(self) -> None:
        """
        new model
         
        """
        self.sessions = aiohttp.ClientSession()
        self.url = 'https://www.kozbs.com/demo/wx/'

    
    async def close(self):
        await self.sessions.close()

    async def request(self, url, method='get', data=None, add_headers: Optional[Dict[str, str]] = None, headers=None, dtype='json', max_retries=3):
        host = urlparse(url).netloc
        _default_headers = {
            ':authority': host,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8447',
            'xweb_xhr': '1',
            'x-dts-token': self.token,
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://servicewechat.com/wx6b6c5243359fe265/99/page-frame.html',
            'accept-language': 'zh-CN,zh;q=0.9m',
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

    async def user_info(self):
        url = self.url + f'user/getUserIntegral'
        res = await self.request(url)
        if not res:
            print(f"[用户{self.index}]:The request to get information failed with an empty response")
            return 
        if res['errno'] == 0:
            # print(res)
            print(f"[user{self.index}]:nickname {res['data']['list'][0]['userName']} Current points {res['data']['integer']}")
            self.userid = res['data']['list'][0]['userId']
        else:
            print(f"[user{self.index}]:error_msg {res}")
    
    async def sign_in(self):
        url = self.url +f'home/signDay?userId={self.userid}'
        res = await self.request(url)
        if not res:
            print(f"[user{self.index}]:The request to get information failed with an empty response")
            return 
        if res['errno'] == 0:
            print(f"[user{self.index}]:Check if the sign-in for today has been completed")
            if res['data']['isSign'] == 0:
                print(f"[user{self.index}]:Signed in today")
            if res['data']['isSign'] == 1:
                print(f"[user{self.index}]:It seems like there was no sign-in, but don't worry, this is the sign-in request.")
        else:
            print(f"[user{self.index}]:error_msg {res}")
    
    async def share_task(self):
        for _ in range(3):
            url = self.url + f'user/addIntegralByShare?userId={self.userid}'
            res = await self.request(url)
            if not res:
                print(f"[用户{self.index}]:The request to get information failed with an empty response")
                break
            if res['errno'] == 0:
                print(f"[user{self.index}]:share {res['errmsg']},Rest for 3 seconds.")
                await asyncio.sleep(3)
            else:
                print(f"[user{self.index}]:error_msg {res}")


    async def integral_info(self):
        url = self.url + f'user/getUserIntegral?userId={self.userid}'
        res = await self.request(url)
        if not res:
                print(f"[用户{self.index}]:The request to get information failed with an empty response")
        if res['errno'] == 0:
            today_date = datetime.now().strftime('%Y-%m-%d')
            today_integral_total = sum(item['integral'] for item in res['data']['list'] if item['createTime'].startswith(today_date))
            print(f"[user{self.index}]:Total points earned today {today_integral_total}, Current total points {res['data']['integer']} ")
        else:
            print(f"[user{self.index}]:error_msg {res}")
    

    async def run(self,index, ck):#
        self.index = index
        self.token = ck
        await self.user_info()
        await self.sign_in()
        await self.share_task()
        await self.integral_info()
        await self.close()

async def get_msg():
    url = 'http://api.doudoudou.fun/other/message?name=zbs'
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as res:
            if res.status ==200:
                res = await res.json()
                print(f"【公告信息】:{res['messages']}")
                # print(res)
                return res['run']
            else:
                print("获取脚本信息失败！！！")
                return False

async def check_env():
    # 这里可以写完善一点的获取环境变量功能
    cks = os.getenv('zbscks')
    if cks is None:
        print("你没有填写zbscks")
        exit()
    correct_data = []
    for index ,ck in enumerate(cks.split("@")):
        # 也许这里可以添加你的变量检测是否合规
        # Here you can write some code.
        correct_data.append(ck)
    return correct_data

async def main():
    await get_msg()
    cks_list = await check_env()
    # 检查是否存在环境变量 multi
    use_concurrency = os.environ.get('zbs_multi', 'false').lower() == 'true'
    tasks = []
    for index, ck in enumerate(cks_list):
        abc = template()
        task = abc.run(index+1, ck)
        tasks.append(task)
    if use_concurrency:  # 如果是true 那么就执行并发
        await asyncio.gather(*tasks)  # 并发执行任务
    else:  # 如果是false 那么就串行执行
        for task in tasks:
            await task  

if __name__ == '__main__':
    asyncio.run(main())
