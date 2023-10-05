"""
new Env("农好优")
export nhycks='手机号#密码@...'
邀请 http://wap.nonghaoyou.cn/Public/reg/recom/289680
签到需要支付宝授权实名挂着玩

"""


import asyncio
import aiohttp
from typing import Optional, Dict 
from urllib.parse import urlparse
import random,re,json
import os



class template:
    def __init__(self) -> None:
        """
        new model
         
        """
        self.sessions = aiohttp.ClientSession()

    
    async def close(self):
        await self.sessions.close()

    async def request(self, url, method='get', data=None, add_headers: Optional[Dict[str, str]] = None, headers=None, dtype='json', max_retries=3):
        host = urlparse(url).netloc
        _default_headers = {
            'Host': host,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36  XiaoMi/MiuiBrowser/10.8.1 LT-APP/45/104/YM-RT/',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie':''
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
                        elif dtype == 'obj':
                            return response
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

    async def login(self, phone, passwd):
        add_headers = {'Origin':'http://wap.nonghaoyou.cn','Referer':'http://wap.nonghaoyou.cn/Public/login','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
        data = f'username={phone}&password={passwd}&xieyi=on'
        url = 'http://wap.nonghaoyou.cn/Public/login'
        response = await self.request(url, 'post', data=data, add_headers=add_headers,dtype='obj')
        if not response:
            print(f"[用户{self.index}]:登录失败!")
            return False
        cookies = response.headers.getall('Set-Cookie')
        # print(cookies)
    # 使用正则表达式提取BJYADMIN和token的值
        bjyadmin = next((re.search(r'BJYADMIN=([^;]+)', cookie).group(1) for cookie in cookies if 'BJYADMIN=' in cookie), None)
        token = next((re.search(r'token=([^;]+)', cookie).group(1) for cookie in cookies if 'token=' in cookie), None)
        if bjyadmin is not None and token is not None:
            self.cookie = f'BJYADMIN={bjyadmin}; token={token};'
            print(f"[用户{self.index}]:登录成功")
            return True
        else:
            print('未找到BJYADMIN或token')
            return False
    
    async def signinfo(self):
        add_headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Cookie':self.cookie}
        url = 'http://wap.nonghaoyou.cn/Member/signin?xapp-target=blank'
        res = await self.request(url,add_headers=add_headers,dtype='text')
        if not res:
            print(f"[用户{self.index}]:获取签到uid失败")
            return 
        pattern_not_completed = r'<div class="signin-btn" onclick="toSign()">.*?</div>'
        match_not_completed = re.search(pattern_not_completed, res)
        if match_not_completed:
            match = re.search(r"var uid = '([^']+)';", res)
            if match:
                uid = match.group(1)
                print(f"[用户{self.index}]:获取签到uid {uid}")
                await self.complete_sign(uid,url)
            else:
                print("未找到uid值")
        else:
            print(f"[用户{self.index}]:今日已完成签到")

    async def complete_sign(self, uid, referer_url):
        url = 'http://wap.nonghaoyou.cn/Member/ad_video_api'
        add_headers = {'Accept':'application/json, text/javascript, */*; q=0.01','Origin':'http://wap.nonghaoyou.cn','Referer':referer_url,'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Cookie':self.cookie}
        data = f'uid={uid}'
        res = await self.request(url,'post',data=data,add_headers=add_headers, dtype='text')
        if not res:
            print(f"[用户{self.index}]:签到失败,返回None") 
        res = json.loads(res)
        # print(res)
        if res['status'] == 1:
            print(f"[用户{self.index}]:签到成功第{res['num']}次")
            if res['num'] != '9':
                ts = random.randint(15,20)
                print(f"[用户{self.index}]:休息{ts}秒")
                await asyncio.sleep(ts)
                await self.complete_sign(uid, referer_url)
        else:
            print(f"[用户{self.index}]:签到失败第{res}")


    async def user_info(self):
        url = 'http://wap.nonghaoyou.cn/Member/index'
        add_headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',"X-Requested-With":"com.cb.tiaoma.nhy",'Referer':'http://wap.nonghaoyou.cn/','Cookie':self.cookie}
        res = await self.request(url,add_headers=add_headers,dtype='text')
        pattern = r'<div class="my-number">([\d.]+)</div>\s*<div class="my-text">(余额|预估收益|积分)</div>'
        # 使用正则表达式查找匹配的内容
        matches = re.findall(pattern, res)
        # 提取匹配的值
        values = {}
        for match in matches:
            value, item = match
            values[item] = value
        print(f"[用户{self.index}]:余额 {values.get('余额','未找到')}|预估收益 {values.get('预估收益','未找到')}|当前积分 {values.get('积分','未找到')}")


    async def run(self,index, ck):#
        self.index = index
        phone,passwd = ck.split('#')
        if await self.login(phone,passwd):
            await asyncio.sleep(random.randint(3,5))
            await self.user_info()
            await asyncio.sleep(random.randint(3,5))
            await self.signinfo()
        await self.close()


async def get_msg():
    url = 'http://api.doudoudou.fun/other/message?name=nhy'
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
    cks = os.getenv('nhycks')
    if cks is None:
        print("你没有填写nhycks")
        exit()
    correct_data = []
    for index ,ck in enumerate(cks.split("@")):
        # 也许这里可以添加你的变量检测是否合规
        # Here you can write some code.
        if len(ck.split('#'))!=2:
            print(f"账号{index+1}:你确定你填对了嘛！")
        else:
            correct_data.append(ck)
    return correct_data

async def main():
    await get_msg()
    cks_list = await check_env()
    # 检查是否存在环境变量 multi
    use_concurrency = os.environ.get('nhy_multi', 'false').lower() == 'true'
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
