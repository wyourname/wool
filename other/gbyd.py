"""
微信阅读：钢镚
链接：http://2488240.ceu.gbl.6rt3sup6c4iy.cloud/?p=2488240
抓 2488240.ceu.. 下的 cookie: gfsessionid=o-0fIvztHxxxxx; zzbb_info=xxxxxxxxxxx,
把cookie完整复制下来就行
export gbydcks='cookie1@cookie2' 单账号就export gbydcks='cookie'就行了

必要推送：WXPUSER  前往网站https://wxpusher.zjiecode.com/docs/#/?id=%e6%b3%a8%e5%86%8c%e5%b9%b6%e4%b8%94%e5%88%9b%e5%bb%ba%e5%ba%94%e7%94%a8
查看注册推送教程
以下推送变量
export WXPUSER_TOKEN='AT_XXXXXA...'
export WXPUSER_TOPICID='1111111'或者 export WXPUSER_UID='UID_xxxxx' 二选一即可
前者群发，后者单推个人，推荐后者
"""


import asyncio
import aiohttp
import requests
import hashlib
import random,json
from typing import Optional, Dict 
from urllib.parse import urlparse,parse_qs,quote
import time
import os



class template:
    def __init__(self) -> None:
        self.sessions = aiohttp.ClientSession()
        self.url = 'http://2478987.hqtu4dwdhi2pet.xcgh.qb33ict7e0mj.cloud/'
        for url in ['http://api.doudoudou.fun','http://api.hwayla.top']:
            if self.test_api(url):
                print(f"url:{url} 测试通过")
                self.aol = url
                break
        
    def test_api(self,url):
        print("开始测试检测服务可用性")
        api_url = url + '/read/announcement'
        res = requests.get(api_url)
        if res.status_code == 200:
            result = res.json()
            print(f"【公告】：{result['messages']}")
            return True
        else:
            return False

    async def close(self):
        await self.sessions.close()

    async def request(self,url,method='get',data=None, add_headers: Optional[Dict[str,str]]=None, headers=None):
        host = urlparse(url).netloc
        # self._default_headers['Host'] = host
        _default_headers={
            'Host': host,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh',
            'Cookie': self.cookie,
        }
        try:
            request_headers = headers or _default_headers
            if add_headers:
                request_headers.update(add_headers)
            async with getattr(self.sessions, method)(url,headers = request_headers, data=data) as response:
                    if response.status == 200:
                        return await response.json()     #返回text或json 看情况如json就response.json()
                    else:
                        print(f"请求失败状态码：{response.status}")
                        return await response.json()    # 同理由可得
        except Exception as e:
            print(e)
            return None

    async def create_sign(self,ts):
        key=f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={ts}'
        hash = hashlib.sha256()
        hash.update(key.encode())
        sign = hash.hexdigest()
        return sign

    async def user_info(self):
        ts = int(time.time())
        sign = await self.create_sign(ts)
        url = self.url + f"user/info?time={ts}&sign={sign}"
        res = await self.request(url)
        url1 = self.url+ f"user/msg?time={ts}&sign={sign}"
        res1 = await self.request(url1)
        if res:
            if res['code'] == 0:
                print(f"【用户】：{res['data']['uid']}")
                print(f"【通知】：{res1['data']['msg']}")
                await self.read_info()
            else:
                print(f"【错误】：获取用户信息失败 {res}")
        else:
            print("请求出现了问题，稍后再来看吧")
    
    
    async def read_info(self):
        ts = int(time.time())
        sign = await self.create_sign(ts)
        url = self.url+f"read/info?time={ts}&sign={sign}"
        res = await self.request(url)
        if res:
            if res['code'] == 0:
               print(f"【收入】：今天收入 {res['data']['gold']}, 阅读 {res['data']['read']},当前余额 {res['data']['remain']}金币") 
               return res['data']['remain']
        else:
            print("请求出现了问题,无法获得信息")
    
    async def do_read_task(self):
        await asyncio.sleep(random.randint(2,5))
        for i in range(1,31):
            print(f"【阅读】:开始第{i}次阅读")
            ts = int(time.time())
            sign = await self.create_sign(ts)
            url = self.url + f"read/task?time={ts}&sign={sign}"
            res = await self.request(url)
            if res['code'] == 0:
                link = res['data']['link']
                if await self.varification(link):
                    random_sleep = random.randint(8,15)
                    print(f"【等待】：{random_sleep}秒")
                    await asyncio.sleep(random_sleep)
                    ts1 = int(time.time())
                    url1 = self.url+ f"user/msg?time={ts1}&sign={sign}"
                    await self.request(url1)
                    result = await self.complete_task()
                    if result is False:
                        break
                else:
                    break
                await asyncio.sleep(random.randint(1,3))
            else:
                print(f"【结果】：{res['message']}")
                break

    async def complete_task(self):
        ts = int(time.time())
        sign = await self.create_sign(ts)
        url = self.url + 'read/finish'
        data = f'time={ts}&sign={sign}'
        add_header = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8','Origin': f'http://{urlparse(url).netloc}','Content-Length': str(len(data))}
        res = await self.request(url,'post',data=data,add_headers=add_header)
        if res:
            if res['code'] == 0:
                print(f"【奖励】:获得{res['data']['gain']} 已读{res['data']['read']}篇,当前金币 {res['data']['remain']}")
                return True
            else:
                print(f"【阅读】:失败 {res}")
        else:
            print(f"【错误】:发生意外 {res}")
            await self.complete_task()


    async def varification(self,url):
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        if '__biz' in query_parameters:
            biz_value = query_parameters['__biz'][0]
            if biz_value in self.check_data:
                print(f"【检测】: {self.check_data[biz_value][0]}公众号")
                encoded_url = quote(url)
                await self.wxpuser("钢镚检测,请1分钟内点击阅读",encoded_url)
                print("【等待】：请手动前往wxpuser点击阅读")
                for i in range(1,61):
                    if await self.get_read_state():
                        print("【阅读】：已手动阅读,稍微延迟5秒钟")
                        await asyncio.sleep(5)
                        return True
                    if i == 60:
                        print("超时未阅读，终止本次阅读")
                        return False
                    time.sleep(1)
            else:
                print(f"【文章】：没有检测")
                return True
        else:
            print("__biz parameter not found in the URL")

    async def with_draw(self,balance):
        if balance >= 3000:
            ts = int(time.time())
            sign = await self.create_sign(ts)
            url = self.url + f"withdraw/wechat?time={ts}&sign={sign}"
            res = await self.request(url)
            if res:
                if res['code'] == 0:
                    print(f"【提现】：{res['message']}")
                else:
                    print(res)
            else:
                print("提现出差错了")
        else:
            print("【提现】: 未达到提现金额，暂不提现")


    async def wxpuser(self,title,url):
        # 此处代码抄袭了别人html的代码，见谅
        content = '''<!DOCTYPE html>
                <html lang="zh-CN">
                <head>
                <meta charset="UTF-8">
                <title>TITLE</title>
                <style type=text/css>
                    body {
                        background-image: linear-gradient(120deg, #fdfbfb 0%, #a5d0e5 100%);
                        background-size: 300%;
                        animation: bgAnimation 6s linear infinite;
                    }
                    @keyframes bgAnimation {
                        0% {background-position: 0% 50%;}
                        50% {background-position: 100% 50%;}
                        100% {background-position: 0% 50%;}
                    }
                </style>
                </head>
                <body>
                    <p>钢镚阅读检测</p><br>
                    <p><a href="self.aol/redirect?user=abc&value=1&timestamp=1900&wxurl=link">点击阅读检测文章</a></p><br>
                </body>
            </html>
        '''
        content = content.replace('self.aol',self.aol).replace('link',url).replace('abc',self.cookie).replace('1900',str(int(time.time())))
        data = {
            "appToken": self.wxpuser_token,
            "content": content,
            "summary": title,
            "contentType": 2,
        }
        if self.topicid is not None:
            data["topicIds"] = [int(self.topicid)]
        if self.wxpuser_uid is not None:
            data["uids"] = [self.wxpuser_uid]
        # print(content)
        json_data = json.dumps(data)
        wxpuser_url = 'http://wxpusher.zjiecode.com/api/send/message'
        res = await self.request(wxpuser_url,'post',data=json_data, headers={"Content-Type":"application/json"})
        if res['success'] == True:
            print(f"【通知】：检测发送成功！")
        else:
            print(f"【通知】：发送失败！！！！！") 

    async def get_read_state(self):
        url = self.aol + f'/read/state?user={self.cookie}&value=1'
        res = await self.request(url)
        if res['status'] == True:
            return True
        else:
            return False
        
    async def check_read(self):
        url = self.aol + f'/check_dict?user={self.cookie}&value=1'
        res = await self.request(url)
        if res and res['status'] == 200:
            self.check_data = res['check_dict']
        else:
            print(f"索取字典出现错误:{res}")

    async def check_env(self):
        self.wxpuser_token = os.getenv("WXPUSER_TOKEN")
        self.topicid = os.getenv("WXPUSER_TOPICID")
        wxpuser_uid = os.getenv("WXPUSER_UID")
        cks = os.getenv('gbydcks')
        if cks is None:
            print("钢镚ck为空，请去抓包格式：'o-0fIvztHsv.....; zzbb_info=%7B%22o......' 多账户请用@分割")
            await self.close()
            exit()
        if self.wxpuser_token is None:
            print("wxpuser的apptoken为空，前往官网注册创建一个app")
            await self.close()
            exit()
        if self.topicid is None and wxpuser_uid is None:
            print("wxpuser的topicid和WXPUSER_UID都为空，请至少填写其中一个")
            await self.close()
            exit()
        return cks.split("@") , wxpuser_uid.split('@')

    async def run(self):
        cks_list,wx_uids = await self.check_env()
        for ck in cks_list:   # 碰到#需要变数组同理也可得
            print(f"{'='*7}开始第{cks_list.index(ck)+1}账号{'='*7}")
            self.cookie = ck
            self.wxpuser_uid = wx_uids[cks_list.index(ck)]
            await self.check_read()
            await self.user_info()
            await self.do_read_task()
            balance = await self.read_info()
            await self.with_draw(balance=balance)
            print(f"{'='*7}结束第{cks_list.index(ck)+1}账号{'='*7}")
        await self.close()

async def main():
    abc = template()
    await abc.run()  
        

if __name__ == '__main__':
    asyncio.run(main())
