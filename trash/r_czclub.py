"""
不用玩了
new Env("纯甄粉俱乐部")
cron: 8 8 * * *
export czcks='authorization#serialid'
并发 export='cz_multi' 可不填
"""

import asyncio
import aiohttp
from typing import Optional, Dict 
from urllib.parse import urlparse
import time,random
import os
from datetime import datetime
import json


class template:
    def __init__(self) -> None:
        self.sessions = aiohttp.ClientSession()
    
    async def close(self):
        await self.sessions.close()

    async def request(self, url, method='get', data=None, add_headers: Optional[Dict[str, str]] = None, headers=None, dtype='json', max_retries=3):
        host = urlparse(url).netloc
        _default_headers = {
            'Host': host,
            'Connection': 'keep-alive',
            'authorization': self.cookie,
            'charset': 'utf-8',
            'serialid': self.serialid,
            'appid': 'wx888d2a452f4a2a58',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5307 MMWEBSDK/20230805 MMWEBID/2651 MicroMessenger/8.0.41.2441(0x28002951) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'Referer': 'https://servicewechat.com/wx888d2a452f4a2a58/155/page-frame.html',
        }
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
                    # await asyncio.sleep(random.randint(3,5))  # 休眠1秒钟
                    return await response.json()
        except Exception as e:
            print(f"请求出现错误：{e}")
        return None    


    async def user_info(self):
        url = 'https://ucode-openapi.aax6.cn/mnzz/quanyu/memberPoint'
        res =await self.request(url)
        if not res:
            print(f"[用户{self.index}]:请求用户信息出现错误")
            return 
        print(f"[用户{self.index}]:会员id{res['memberId']}|当前积分 {res['pointsBalance']}")
    
    async def check_in(self):   
        # 获取当前日期的时间戳
        today_timestamp = int(time.mktime(datetime.today().date().timetuple()))
        url = 'https://ucode-openapi.aax6.cn/user/checkIn?promotionId=1001681&days=1'
        res = await self.request(url)
        if not res:
            print(f"[用户{self.index}]:获取签到信息出现错误")
            return
        if 'details' not in res:
            print(f"[用户{self.index}]:今天尚未签到")
            await self.sign_in()
            return
        # if 'details' in res:
        #     if today_timestamp <= int(res['details'][-1]['lotteryTime']/1000):
        #         print(f"[用户{self.index}]:今天已经签到了")
        #     else:
        #         print(f"[用户{self.index}]:今天尚未签到")
        await self.sign_in()

    
    async def sign_in(self):
        data = {
        "promotionId": 1001681,
        "promotionCode": "CRM-QD",
        "pointRecordRemark": "连续签到"
        }
        url = 'https://ucode-openapi.aax6.cn/lottery/checkIn'
        data = json.dumps(data)
        res = await self.request(url,'post',data=data)
        if not res:
            print(f"[用户{self.index}]:签到出错了")
            return
        if 'lotteryTime' in res:
            dt = datetime.fromtimestamp(res['lotteryTime']/1000)
            print(f"[用户{self.index}]:签到时间{dt}")
            print(f"[用户{self.index}]:奖励{res['award']['name']}")
        else:
            print(f"[用户{self.index}]:{res['emsg']}")

    async def run(self,index, ck:str):#
        self.cookie,self.serialid = ck.split('#')
        self.index = index
        await self.user_info()
        await self.check_in()
        await self.close()


async def check_env():
    # 这里可以写完善一点的获取环境变量功能
    cks = os.getenv('czcks')
    if cks is None:
        print("你没有填写czcks")
        exit()
    correct_data = []
    for index ,ck in enumerate(cks.split("@")):
        # 也许这里可以添加你的变量检测是否合规
        # Here you can write some code.
        if len(ck.split('#')) !=2:
            print(f"账号{index+1}:ck错啦格式为authorization#serialid")
        else:
            correct_data.append(ck)
    return correct_data

async def main():
    cks_list = await check_env()
    # 检查是否存在环境变量 multi
    use_concurrency = os.environ.get('cz_multi', 'false').lower() == 'true'
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
