"""
阅读走不走我的邀请都行,能用我的本就是给面子我了
微信阅读:钢镚
这是我的WXPUSER_TOKEN,你可以直接拿来用
export WXPUSER_TOKEN="AT_aYF2532tqjrD4dX90OrJsuiflscRureX"
微信打开链接:https://wxpusher.zjiecode.com/wxuser/?type=1&id=50341#/follow
关注wxpuser app 订阅公众号就能获取你的uid
export WXPUSER_UID="UID_xxxxx"
||||||
微信阅读:小阅阅
链接:http://2488240.ceu.gbl.6rt3sup6c4iy.cloud/?p=2488240
抓 2488240.ceu.. 下的 cookie: gfsessionid=o-0fIvztHxxxxx; zzbb_info=xxxxxxxxxxx,
把cookie完整复制下来就行
export gbydcks='cookie1@cookie2' 单账号就export gbydcks='cookie'就行了
export multi_gbyd='true'  # 并发开关，可以不填
你不想用我的WXPUSER_TOKEN,这是你的自行注册的教程
如果你是让别人代挂的,你可以让代挂的给你扫一下wxpuser的码,再把uid发送给他就行
必要推送:WXPUSER  前往网站https://wxpusher.zjiecode.com/docs/#/?id=%e6%b3%a8%e5%86%8c%e5%b9%b6%e4%b8%94%e5%88%9b%e5%bb%ba%e5%ba%94%e7%94%a8
查看注册推送教程
以下推送变量
export WXPUSER_TOKEN='AT_XXXXXA...'
export WXPUSER_TOPICID='1111111'   # 这个可以不填,不推荐这个
export WXPUSER_UID='UID_xxxxx@UID_XXXX' WXPUSER_TOPICID和WXPUSER_UID二选一即可 WXPUSER_UID要和cookie数量一致,WXPUSER_UID可以重复填
比如我2个微信阅读只想推送给一个微信 那就export WXPUSER_UID='UID_123456@UID_123456'
前者群发，后者单推个人，推荐后者

new Env('钢镚阅读')
"""


import asyncio
import aiohttp
import hashlib
import random,json
from typing import Optional, Dict 
from urllib.parse import urlparse,parse_qs,quote
import time,re
import os



class Gbyd:
    def __init__(self) -> None:
        self.sessions = aiohttp.ClientSession()
        self.url = 'http://2478987.hqtu4dwdhi2pet.xcgh.qb33ict7e0mj.cloud/'

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
                        print(f"请求失败状态码:{response.status}")
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
    
    async def valid_auth(self):
        ts = int(time.time())
        match = re.search(r'gfsessionid=([^;]+)', self.cookie)
        zzid = match.group(1)
        str1 = f'{ts}&zzid={zzid}'
        sign = await self.create_sign(str1)
        url = self.url +f'auth/valid?time={ts}&zzid={zzid}&sign={sign}'
        res = await self.request(url)
        if not res:
            print("valid 的方法错误,联系开发者吧")
            return 
        if res['code'] == 0:
            print(f"【用户{self.index}】【登录】:模拟登录{res['message']}")
            await asyncio.sleep(3)
        else:
            print(f"【用户{self.index}】【登录】:模拟登录{res['message']}")

    async def user_info(self):
        ts = int(time.time())
        sign = await self.create_sign(ts)
        url = self.url + f"user/info?time={ts}&sign={sign}"
        res = await self.request(url)
        url1 = self.url+ f"user/msg?time={ts}&sign={sign}"
        res1 = await self.request(url1)
        if res:
            if res['code'] == 0:
                print(f"【用户{self.index}】【信息】:id {res['data']['uid']}")
                print(f"【用户{self.index}】【通知】:{res1['data']['msg']}")
                await self.read_info()
            else:
                print(f"【用户{self.index}】【错误】:获取用户信息失败 {res}")
        else:
            print("请求出现了问题，稍后再来看吧")
    
    
    async def read_info(self):
        ts = int(time.time())
        sign = await self.create_sign(ts)
        url = self.url+f"read/info?time={ts}&sign={sign}"
        res = await self.request(url)
        if res:
            if res['code'] == 0:
               print(f"【用户{self.index}】【收入】:今天收入 {res['data']['gold']}, 阅读 {res['data']['read']},当前余额 {res['data']['remain']}金币") 
               return res['data']['remain']
        else:
            print("请求出现了问题,无法获得信息")
    
    async def do_read_task(self):
        await asyncio.sleep(random.randint(2,5))
        for i in range(1,31):
            print(f"【用户{self.index}】【阅读】:开始第{i}次阅读")
            ts = int(time.time())
            sign = await self.create_sign(ts)
            url = self.url + f"read/task?time={ts}&sign={sign}"
            res = await self.request(url)
            if res['code'] == 0:
                link = res['data']['link']
                if await self.varification(link):
                    random_sleep = random.randint(8,15)
                    print(f"【用户{self.index}】【等待】:{random_sleep}秒")
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
                print(f"【用户{self.index}】【结果】:{res['message']}")
                break

    async def complete_task(self):
        ts = int(time.time())
        sign = await self.create_sign(ts)
        url = self.url + 'read/finish'
        data = f'time={ts}&sign={sign}'
        add_header = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8','Origin': f'http://{urlparse(url).netloc}','Content-Length': str(len(data))}
        res = await self.request(url,'post', data=data, add_headers=add_header)
        if res:
            if res['code'] == 0:
                print(f"【用户{self.index}】【奖励】:获得{res['data']['gain']} 已读{res['data']['read']}篇,当前金币 {res['data']['remain']}")
                return True
            else:
                print(f"【用户{self.index}】【阅读】:失败 {res}")
        else:
            print(f"【用户{self.index}】【错误】:发生意外 {res}")
            await self.complete_task()


    async def varification(self,url):
        # print(url)
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        if '__biz' in query_parameters:
            biz_value = query_parameters['__biz'][0]
            if biz_value in self.check_data:
                print(f"【用户{self.index}】【检测】: {self.check_data[biz_value][0]}公众号")
                encoded_url = quote(url)
                await self.wxpuser(f"钢镚【用户{self.index}】检测,请90秒内点击阅读",encoded_url)
                print(f"【用户{self.index}】【等待】:请手动前往wxpuser点击阅读")
                start_time = int(time.time())
                while True:
                    if await self.get_read_state():
                        print(f"【用户{self.index}】【阅读】:已手动阅读,稍微延迟3秒钟")
                        await asyncio.sleep(3)
                        return True
                    if int(time.time())- start_time > 90:
                        print(f"【用户{self.index}】【警告】:90秒到啦,终止本次阅读")
                        return False
                    time.sleep(1)
            else:
                print(f"【用户{self.index}】【文章】:没有检测")
                return True
        else:
            print("__biz parameter not found in the URL")

    async def with_draw(self,balance):
        if balance >= 6000:
            ts = int(time.time())
            sign = await self.create_sign(ts)
            url = self.url + f"withdraw/wechat?time={ts}&sign={sign}"
            res = await self.request(url)
            if res:
                if res['code'] == 0:
                    print(f"【用户{self.index}】【提现】:{res['message']}")
                else:
                    print(f"【用户{self.index}】【提现】:{res['message']}")
            else:
                print("提现出差错了")
        else:
            print(f"【用户{self.index}】【提现】: 未达到提现金额，暂不提现")


    async def wxpuser(self,title,url):
        content = '''
        <!DOCTYPE html>
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
                        0% {
                            background-position: 0% 50%;
                        }
                    
                        50% {
                            background-position: 100% 50%;
                        }
                    
                        100% {
                            background-position: 0% 50%;
                        }
                    }
                    .title {
                        text-align: center;
                        font-size: 25px;
                        display: block;
                    }
                    .button {
                        background-image: linear-gradient(to right, #77A1D3 0%, #79CBCA 51%, #77A1D3 100%);
                        text-align: center;
                        transition: 0.5s;
                        background-size: 200% auto;
                        border-radius: 10px;
                        width: 50%;
                        margin: 25px auto;
                    }
                    .button a {
                        padding: 15px 45px;
                        display: block;
                        text-decoration: none;
                        color: white;
                    }
                    .tips {
                        text-align: center;
                        margin: auto;
                        padding: 10px 0px;
                        box-shadow: rgba(0, 0, 0, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px;
                    }
                </style>
            </head>
            <body>
                <div class="title">用户a钢镚阅读检测,务必在一分钟内点击阅读</div>
                <div class='button'><a href="self.aol/redirect?user=uuu&value=1&timestamp=tsone&wxurl=link">点击阅读检测文章</a></div>
                <div class="tips">
                    <p>如果错过时间未能阅读, 会导致当天收益下降或者没有收益</p>
                    <p>请留意消息推送,时间按照你的定时看</p>
                </div><br>
            </body>
        </html>
        '''
        content = content.replace('用户a',f'用户{self.index}').replace('self.aol',self.aol).replace('uuu',self.cookie).replace('link',url).replace('tsone',str(int(time.time())))
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
        json_data = json.dumps(data)
        wxpuser_url = 'http://wxpusher.zjiecode.com/api/send/message'
        res = await self.request(wxpuser_url,'post',data=json_data, headers={"Content-Type":"application/json"})
        if res['success'] == True:
            print(f"【用户{self.index}】【通知】:检测发送成功！")
        else:
            print(f"【用户{self.index}】【通知】:发送失败！！！！！") 

    async def get_read_state(self,max_retry=3):
        url = self.aol + f'/read/state?user={self.cookie}&value=1'
        try:
            async with aiohttp.ClientSession() as client:
                async with client.get(url) as res:
                    if res.status ==200:
                        res1 = await res.json()
                        if res1['status'] == True:
                            return True
                        else:
                            if res1['status'] == '-1' and max_retry>0:
                                await asyncio.sleep(5)
                                await self.get_read_state(max_retry-1)
                            return False
                    else:
                        return False
        except Exception as e:
            print(f"捕获到请求状态异常:{e}")
            if max_retry == 0:
                return False
            await asyncio.sleep(3)
            await self.get_read_state(max_retry-1)
        
    async def init_check_dict(self, maxretry=3):
        print(f"【用户{self.index}】:初始化阅读后台检测状态")
        url = self.aol + f'/check_dict?user={self.cookie}&value=1'
        async with aiohttp.ClientSession() as client:
            async with client.get(url) as res:
                if res.status ==200:
                    res1 = await res.json()
                    self.check_data = dict(res1['check_dict'])
                    print(f"【用户{self.index}】:初始化状态成功")
                else:
                    if maxretry >0:
                        print(f"【用户{self.index}】:初始化阅读后台检测状态失败")
                        await self.init_check_dict(maxretry-1)
                    else:
                        exit()


    async def process_account(self,index, ck, wxpuser_uid, wxpuser_token, topicid , check_url, sleep_time=None):
        self.aol = check_url
        self.index = index
        if sleep_time:
            print(f"【用户{self.index}】:随机休息{sleep_time}秒，我怕你点不了那么多")
            await asyncio.sleep(sleep_time)
        print(f"【用户{self.index}】【开始】:{'='*10}执行任务{'='*10}")
        self.wxpuser_token = wxpuser_token
        self.topicid=topicid
        self.cookie = ck
        self.wxpuser_uid = wxpuser_uid
        await self.init_check_dict()
        await self.valid_auth()
        await self.user_info()
        await self.do_read_task()
        balance = await self.read_info()
        await self.with_draw(balance=balance)
        await self.close()
        print(f"【用户{self.index}】【结束】:{'='*10}结束执行{'='*10}")

async def test_api(url):
    print("开始测试检测服务可用性")
    api_url = url + '/read/announcement'
    async with aiohttp.ClientSession() as client:
        async with client.get(api_url) as res:
            if res.status ==200:
                result = await res.json()
                print(f"【公告】:{result['messages']}")
                return True
            else:
                return False

async def check_env():
    wxpuser_token = os.getenv("WXPUSER_TOKEN")
    topicid = os.getenv("WXPUSER_TOPICID")
    wxpuser_uid = os.getenv("WXPUSER_UID")
    cks = os.getenv('gbydcks')
    if cks is None:
        print("钢镚ck为空,请去抓包格式:'gfsessionid=o-0fIvztHxxxxx; zzbb_info=xxxxxxxxxxx' 多账户请用@分割")
        print('cookie填写:export gbydcks="gfsessionid=o-0fIvztHxxxxx; zzbb_info=xxxxxxxxxxx"')
        exit()
    if wxpuser_token is None:
        print("wxpuser的apptoken为空,前往官网注册创建一个app,复制应用token和微信关注wxpuser公众号获取uid")
        print("获取完请在配置文件填写:export WXPUSER_TOKEN=AT_aYF2.....\nexport WXPUSER_UID=UID_....")
        exit()
    if topicid is None and wxpuser_uid is None:
        print("wxpuser的topicid和WXPUSER_UID都为空,请至少填写其中一个")
        exit()
    return cks.split("@") , wxpuser_uid.split('@'), topicid, wxpuser_token

async def main():
    aol = []
    for url in ['http://api.doudoudou.fun']:
        if await test_api(url):
            print(f"{url} 联通性测试通过")
            aol.append(url)
    if len(aol) == 0:
        print("当前检测服务不可用,请稍后再试")
        exit()
    cks_list, wx_uids,topicid,wxpuser_token = await check_env()
    use_concurrency = os.environ.get('multi_gbyd', 'false').lower() == 'true'
    from random import choice
    if use_concurrency:
        tasks = []
        random_sleep_list = [i * random.randint(50, 65) for i in range(len(cks_list))]
        for index, ck in enumerate(cks_list):
            abc = Gbyd()
            tasks.append(abc.process_account(index+1, ck, wx_uids[index], wxpuser_token=wxpuser_token, topicid=topicid, check_url=choice(aol),sleep_time=random_sleep_list[index]))
        await asyncio.gather(*tasks)
    else:
        for index, ck in enumerate(cks_list):
            abc = Gbyd()
            await abc.process_account(index+1, ck, wx_uids[index], wxpuser_token=wxpuser_token, topicid=topicid, check_url=choice(aol))
  

if __name__ == '__main__':
    asyncio.run(main())
