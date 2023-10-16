"""

new Env("魔盒")
cron: 8 8 * * *
export mhcks='sessionid#提现金额#提现支付宝号#名字'
提现金额 0.3 1 50
3档位 一天一次,停了再手动跑一下,10积分无限刷
# 一个ip一个号
"""

import asyncio
import aiohttp
from typing import Optional, Dict 
from urllib.parse import urlparse
from random import choice,randint
import os
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
            'sessionId': self.sessionid,
            'Connection': 'keep-alive',
            'Accept-Encoding':'gzip',
            'User-Agent':'okhttp/3.10.0'
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
        url = 'https://jkyx-api.chiguavod.com/applet/mf/advertising/integral/info'
        res =await self.request(url,'post')
        if not res:
            print(f"[用户{self.index}]:请求用户信息出现错误")
            return 
        if res['code'] == 200:
            # print(res)
            print(f"[用户{self.index}]:用户名 {res['data']['nickName']}|当前积分 {res['data']['integral']}")
            if 1 > float(res['data']['integral'])/10000 > 0.3:
                if float(self.draw) == 0.3:
                    print(f"[用户{self.index}]:前往提现0.3元")
                    await self.with_draw(0.3)    
            if 2 > float(res['data']['integral'])/10000 >= 1:
                if float(self.draw) == 1.0:
                    print(f"[用户{self.index}]:前往提现1元")
                    await self.with_draw(1.0)
            if 100 > float(res['data']['integral'])/10000 >=50:
                if float(self.draw) == 50.0:
                    print(f"[用户{self.index}]:前往提现50元")
                    await self.with_draw(50.0)
        else:
            print(f"[用户{self.index}]:获取失败{res}")
    
    async def flash_video(self):
        while True:
            url = 'https://jkyx-api.chiguavod.com/applet/mf/advertising/integral/which'
            res = await self.request(url)
            if not res:
                print(f"[用户{self.index}]:请求广告平台信息出现错误")
                return
            if res['code'] == 200:
                print(f"[用户{self.index}]:平台广告类型 {res['data']['advertiserType']}")
                c_advertiser = choice(res['data']['advertisingList'])
                print(f"[用户{self.index}]:本次选择了{c_advertiser['advertisingName']}平台")
                if await self.watch_video(res['data']['advertiserType'],c_advertiser['advertising']):
                    sleep_time = randint(20,30)
                    print(f"[用户{self.index}]:本次休息{sleep_time}")
                    await asyncio.sleep(sleep_time)
                else:
                    break

    async def watch_video(self, adtype, adsing):
        url = 'https://jkyx-api.chiguavod.com/applet/mf/advertising/integral/watch/video'
        data = {"advertiserType":adtype, "advertising":adsing}
        data = json.dumps(data)
        add_headers = {'Content-Type':'application/json; charset=UTF-8','Content-Length':f'{len(data)}'}
        res = await self.request(url,'post',data=data,add_headers=add_headers)
        if not res:
            print(f"[用户{self.index}]:请求获得奖励信息出现错误")
            return False
        if res['code'] == 200:
            print(f"[用户{self.index}]:本次请求获得 {res['data']['integral']},当前积分{res['data']['residueIntegral']}")
            if int(res['data']['integral']) <=0:
                print(f"[用户{self.index}]:本次请求获得积分过低,停止执行")
                return False
            return True
        else:
            print(f"[用户{self.index}]:本次请求未知错误{res}")
            return False
        
    async def with_draw(self, money):
        url = 'https://jkyx-api.chiguavod.com/applet/mf/advertising/integral/withdraw'
        data = {"aliAccount":self.phone,"amount":money,"cashType":1,"realName":self.name}
        data = json.dumps(data)
        add_headers = {'Content-Type':'application/json; charset=UTF-8','Content-Length':f'{len(data)}'}
        res = await self.request(url,'post',data=data,add_headers=add_headers)
        if not res:
            print(f"[用户{self.index}]:请求提现出现错误")
            return 
        if res['code'] == 200:
            print(f"[用户{self.index}]:请求提现{res['msg']}")
        else:
            print(f"[用户{self.index}]:失败，请求提现{res['msg']}")

    async def run(self,index, ck:str):#
        self.sessionid,self.draw,self.phone,self.name = ck.split('#')
        self.index = index
        await self.user_info()
        # await self.flash_video()
        await self.close()


async def check_env():
    # 这里可以写完善一点的获取环境变量功能
    cks = os.getenv('mhcks')
    if cks is None:
        print("你没有填写mhcks")
        exit()
    correct_data = []
    for index ,ck in enumerate(cks.split("@")):
        # 也许这里可以添加你的变量检测是否合规
        # Here you can write some code.
        if len(ck.split('#')) !=4:
            print(f"账号{index+1}:ck错啦格式为sessionid")
        else:
            correct_data.append(ck)
    return correct_data


async def get_msg():
    url = 'http://api.doudoudou.fun/other/message?name=mh'
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as res:
            if res.status ==200:
                res = await res.json()
                print(f"【公告信息】:{res['messages']}")
                return res['run']
            else:
                print("获取脚本信息失败！！！")
                return False


async def main():
    cks_list = await check_env()
    # 检查是否存在环境变量 multi
    await get_msg()
    use_concurrency = os.environ.get('mh_multi', 'false').lower() == 'true'
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
