"""
export rrbcks='手机号&uid&token' # 自动提现，提前绑定支付宝,每天6毛,容易黑，过一天就好了，一天2次

我不推荐玩这个和三合一，太坑了，但是脚本都写了没办法

邀请链接http://ebb.nianshuiyong.cloud/user/index.html?mid=1700837019170766848任务类型多，综合收益高；简单易上手，提现秒到账；拉新推广，享受永久分成；大额提现，享受专属客服（若链接打不开，可复制到手机浏览器里打开）

必要推送:WXPUSER  前往网站https://wxpusher.zjiecode.com/docs/#/?id=%e6%b3%a8%e5%86%8c%e5%b9%b6%e4%b8%94%e5%88%9b%e5%bb%ba%e5%ba%94%e7%94%a8
查看注册推送教程
以下推送变量
export WXPUSER_TOKEN='AT_XXXXXA...'
export WXPUSER_TOPICID='1111111'   # 这个可以不填 
export WXPUSER_UID='UID_xxxxx@UID_XXXX'  # 推荐填这个

WXPUSER_TOPICID和WXPUSER_UID二选一即可 WXPUSER_UID要和cookie数量一致，WXPUSER_UID可以重复填

比如我2个微信阅读只想推送给一个微信 那就export WXPUSER_UID='UID_123456@UID_123456'
前者群发，后者单推个人，推荐后者
"""



import asyncio
import aiohttp
from typing import Optional, Dict 
import requests
from urllib.parse import urlparse,parse_qs,quote
import time,json,re,random
import os

"""
人人帮
待完善


"""


class Rrbyd:
    def __init__(self) -> None:

        self.sessions = aiohttp.ClientSession()
        self.base_url = 'http://ebb.vinse.cn/api/'
        

    
    async def close(self):
        await self.sessions.close()

    async def request(self,url,method='get',data=None, dtype='json', add_headers: Optional[Dict[str,str]]=None, headers=None):
        host = urlparse(url).netloc
        _default_headers = {
            'Host': host,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8391 Flue',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
            'Proxy-Connection': 'keep-alive',
            'mid': 'null',
            'platform': '0',
            'Origin': 'http://ebb101.twopinkone.cloud',
            'Referer': 'http://ebb101.twopinkone.cloud/',
            'Accept-Language': 'zh-CN,zh',
            }
        try:
            request_headers = headers or _default_headers
            if add_headers:
                request_headers.update(add_headers)
            async with getattr(self.sessions, method)(url,headers = request_headers, data=data) as response:
                    if response.status == 200:
                        if dtype == 'json':
                            return await response.json()     #返回text或json 看情况如json就response.json()
                        if dtype == 'text':
                            return await response.text()
                    else:
                        print(f"请求失败状态码：{response.status}")
                        if dtype == 'json':
                            return await response.json()     #返回text或json 看情况如json就response.json()
                        if dtype == 'text':
                            return await response.text()
        except Exception as e:
            print(e)
            return None    
    
    async def user_info(self):
        url = self.base_url+'user/info'
        add_headers = {'un':self.un,'uid':self.uid,'token':self.cookie}
        data_json = {"pageSize": 10}
        res = await self.request(url,'post',data=json.dumps(data_json),add_headers=add_headers)
        if res:
            if res['code'] == 0:
                print(f"【用户】:{res['result']['nickName']}  当前{res['result']['integralCurrent']}")
                if res['result']['integralCurrent'] >=5000:
                    await self.with_draw(5000)

            else:
                print(f"【用户】:error infomation:{res}")
        else:
            print("【用户】:返回为空,肯定出问题了")

    async def sign_status(self):
        url = self.base_url+'user/getUserSignDays'
        add_headers = {'un':self.un,'uid':self.uid,'token':self.cookie}
        data_json = {"pageSize": 10}
        res = await self.request(url,'post',data=json.dumps(data_json),add_headers=add_headers)
        if res:
            if res['code'] == 0:
                if res['result']['signStatus'] == 0:
                    print(f"【用户】:今天尚未签到,试着签到")
                    await self.signIn()
                else:
                    print(f"【用户】:今天已经签到")
            else:
                print(f"error infomation:{res}")
        else:
            print("【用户】:返回为空,肯定出问题了")

    async def signIn(self):
        url = self.base_url+'user/sign'
        add_headers = {'un':self.un,'uid':self.uid,'token':self.cookie}
        data_json = {"pageSize": 10}
        res = await self.request(url,'post',data=json.dumps(data_json),add_headers=add_headers)
        if res:
            if res['code'] == 0:
                print(f"【用户】:签到获得{res['result']['point']}豆")
            else:
                print(f"【用户】:签到失败{res}")
        else:
            print("【用户】:返回为空,肯定出问题了")
    
    async def start(self):
        url = f'https://u.cocozx.cn/ipa/read/getEntryUrl?fr=ebb0726&uid={self.uid}'
        res = await self.request(url=url)
        if res:
            if res['code'] == 0 and res['result']['status'] !=2:
                print(f'【用户】:获取到阅读url {res["result"]["url"]}')
                if res["result"]["url"]:
                    await self.read(res["result"]["url"])
            else:
                print("【用户】:当前不能阅读")
        else:
            print("【用户】:请求出现差错了,有问题")
    
    async def read(self,start_url):
        res = await self.request(start_url,dtype='text')
        if res:
            print("【用户】:模拟打开页面成功")
            extracted_value = re.search(r'mr(\d+)', start_url).group(1) if re.search(r'mr(\d+)', start_url) else None
            if extracted_value:
                host = urlparse(start_url).netloc
                value = await self.get_group(extracted_value,host=host)
                await self.read_info(host=host,value=value)
        else:
            print("【用户】:请求出现差错了,有问题")

    async def read_info(self,host,value):
        url = 'http://u.cocozx.cn/ipa/read/info'
        data_json = {
            "fr": "ebb0726",
            "uid": self.uid,
            "group": value,
            "un": None,
            "token": None,
            "pageSize": 20
            }
        add_headers = {'Origin': f'http://{host}'}
        res = await self.request(url,'post',data=json.dumps(data_json),add_headers=add_headers)
        if res:
            if res['code'] == 0:
                print(f"【用户】:当前任务最大数量{res['result']['dayMax']},当前次数{res['result']['dayCount']}")
                num = res['result']['dayMax'] - res['result']['dayCount']
                for i in range(num):
                    print(f"【用户】:第{i+1}次阅读")
                    result = await self.complete(host=host,value=value)
                    if result is False:
                        break
                    else:
                        await asyncio.sleep(random.randint(2,3))
            else:
                print("【用户】:当前不能阅读")
        else:
            print("【用户】:请求出现差错了,有问题")
    
    async def complete(self,host,value):
        url = 'http://u.cocozx.cn/ipa/read/read'
        data_json = {
            "fr": "ebb0726",
            "uid": self.uid,
            "group": value,
            "un": None,
            "token": None,
            "pageSize": 20
            }
        add_headers = {'Origin': f'http://{host}'}
        res = await self.request(url,'post', data=json.dumps(data_json),add_headers=add_headers)
        if res:
            if res['code'] == 0:
                if res['result']['url']:
                    if await self.varification(res['result']['url']):
                        ts = random.randint(7,15)
                        print(f"【用户】:等待{ts}秒")
                        await asyncio.sleep(ts)
                        submit_url = 'http://u.cocozx.cn/ipa/read/submit'
                        res = await self.request(submit_url,'post', data=json.dumps(data_json),add_headers=add_headers)
                        if res:
                            if res['code'] == 0:
                               print(f"【用户】:完成阅读{res['result']['dayCount']}次")
                            else:
                                 print(f"【用户】:阅读失败{res}")
                        else:
                            print("【用户】:请求出现差错了,有问题")
                        return True
                    else:
                        return False
                else:
                    print("【用户】:没有url了")
                    return False
            else:
                print("【用户】:发生什么事情了")
        else:
            print("【用户】:请求出现差错了,有问题")

    async def with_draw(self,money):
        url = f"http://ebb.vinse.cn/apiuser/aliWd"
        data_json = {"val": money, "pageSize": 10}
        add_headers = {'un':self.un,'uid':self.uid,'token':self.cookie}
        res = await self.request(url,'post',data=json.dumps(data_json),add_headers=add_headers)
        if res:
            if res['code'] == 0:
                print(f"【用户】:提现{money/10000}元成功！")
            else:
                print(f"【用户】:提现{money/10000}元失败！原因{res}")
        else:
            print("【用户】:请求出现差错了,有问题")


    async def varification(self,url):
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        if '__biz' in query_parameters:
            biz_value = query_parameters['__biz'][0]
            if biz_value in self.check_data:
                print(f"【用户】【检测】: {self.check_data[biz_value][0]}公众号")
                encoded_url = quote(url)
                await self.wxpuser("人人帮检测,请1分钟内点击阅读",encoded_url)
                print(f"【用户】【等待】:请手动前往wxpuser点击阅读")
                for i in range(1,61):
                    if await self.get_read_state():
                        print(f"【用户】【阅读】:已手动阅读,稍微延迟5秒钟")
                        await asyncio.sleep(5)
                        return True
                    if i == 60:
                        print(f"【用户】【警告】:超时未阅读，终止本次阅读")
                        return False
                    time.sleep(1)
            else:
                print(f"【用户】:没有检测")
                return True
        else:
            print("__biz parameter not found in the URL")
            return True

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
                <div class="title">人人帮阅读检测，务必在一分钟内点击阅读</div>
                <div class='button'><a href="self.aol/redirect?user=abc&value=0&timestamp=1900&wxurl=link">点击阅读检测文章</a></div>
                <div class="tips">
                    <p>如果错过时间未能阅读, 会导致当天收益下降或者没有收益</p>
                    <p>请留意消息推送时间点(9, 11, 13, 15, 17, 19, 21)</p>
                </div><br>
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
        json_data = json.dumps(data)
        wxpuser_url = 'http://wxpusher.zjiecode.com/api/send/message'
        res = await self.request(wxpuser_url,'post',data=json_data, headers={"Content-Type":"application/json"})
        if res['success'] == True:
            print(f"【用户】【通知】:检测发送成功！")
        else:
            print(f"【用户】【通知】:发送失败！！！！！") 

    async def get_group(self,num,host):
        add_headers = {'Origin': f'http://{host}',
                   'X-Requested-With': 'com.tencent.mm',
                   'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
        data_json = {"un": None, "token": None, "pageSize": 20}
        url = f'http://u.cocozx.cn/api/common/ustr?t={num}'
        res = await self.request(url,'post', add_headers=add_headers, data=json.dumps(data_json))
        if res:
            if res['code'] == 0:
                if res['result']['str']:
                    parsed_url = urlparse(res['result']['str'])
                    # 提取参数
                    query_parameters = parse_qs(parsed_url.query)
                    # 获取 "group" 参数的值
                    group_value = query_parameters.get('group', [None])[0]
                    if group_value is not None:
                        return group_value
                    else:
                        return None
            else:
                print("【用户】:发生什么事情")
                return None
        else:
            print("【用户】:我有罪,请求错了")
    
    async def souhu(self):
        url = self.base_url + 'task/v2/getTask'
        data_json = {
        "imgUrl": "http://juyouimg.oss-cn-zhangjiakou.aliyuncs.com/15/task/QoExACdjJc.png",
        "businessType": 5,
        "taskType": "14",
        "pageSize": 10
        }
        add_headers = {'un':self.un,'uid':self.uid,'token':self.cookie}
        res = await self.request(url,'post',data=json.dumps(data_json),add_headers=add_headers)
        if res:
            # print(res)
            if res['code'] == 0:
                print(f"【用户】:当前提交的搜狐任务助力数量为{res['result']['commitNum']},当前任务数量限制为{res['result']['taskLimitNum']}")
                chances = res['result']['taskLimitNum']-res['result']['commitNum']
                if chances>0:
                    ts = random.randint(70,80)
                    print(f"【用户】:开始搜狐视频助力,等待{ts}秒")
                    await asyncio.sleep(ts)
                    await self.commit_souhu()
                    await asyncio.sleep(random.randint(2,3))
                    await self.souhu()
            else:
                print(f"【用户】:发生了什么事情,原来是{res['msg']}")
        else:
            print("【用户】:我有罪,请求出错了")

    async def commit_souhu(self):
        url = self.base_url +'task/v2/commitTask'
        data_json = {
                "imgUrl": "http://juyouimg.oss-cn-zhangjiakou.aliyuncs.com/15/task/QoExACdjJc.png",
                "businessType": 5,
                "taskType": "14", 
                "pageSize": 10
            }
        add_headers = {'un':self.un,'uid':self.uid,'token':self.cookie}
        res = await self.request(url,'post',data=json.dumps(data_json),add_headers=add_headers)
        if res:
            if res['code'] == 0:
                print(f"【用户】:搜狐视频助力成功")
            else:
                print(f"【用户】:搜狐视频助力失败!!!!!!!!!!!!!!!!!!{res}")
        else:
            print("【用户】:我有罪,请求出错了")

    async def get_read_state(self,max_retry=3):
        url = self.aol + f'/read/state?user={self.cookie}&value=2'
        res = requests.get(url)
        if res.status_code == 200:
            res = res.json()
            if res['status'] == True:
                return True
            else:
                if res['status'] == '-1' and max_retry>0:
                    time.sleep(5)
                    self.get_read_state(max_retry-1)
                return False
        else:
            return False
        
    async def check_read(self,maxretry=2):
        url = self.aol + f'/check_dict?user={self.cookie}&value=2'
        res = requests.get(url)
        if res.status_code == 200:
            res = res.json()
            self.check_data = res['check_dict']
        else:
            if maxretry >0:
                b_line = 'http://api.doudoudou.fun'
                print(f"【用户】：索取字典出现错误:{res.status_code},试着重新获取！")
                self.check_read(b_line,maxretry-1)
            else:
                exit()

    async def run(self, ck,wxpuser_uid,topicid,wxpuser_token,a_url):
        self.un,self.uid,self.cookie = ck.split('&')
        self.aol = a_url
        self.wxpuser_token = wxpuser_token
        self.topicid=topicid
        self.wxpuser_uid = wxpuser_uid
        await self.check_read()
        # await self.user_info()
        # await self.sign_status()
        # await self.start()
        await self.souhu()
        await self.close()

async def check_env():
    wxpuser_token = os.getenv("WXPUSER_TOKEN")
    topicid = os.getenv("WXPUSER_TOPICID")
    wxpuser_uid = os.getenv("WXPUSER_UID")
    cks = os.getenv('rrbcks')
    if cks is None:
        print("人人帮ck为空，请去抓包格式:'手机号&uid&token' 多账户请用@分割")
        exit()
    if wxpuser_token is None:
        print("wxpuser的apptoken为空，前往官网注册创建一个app")
        exit()
    if topicid is None and wxpuser_uid is None:
        print("wxpuser的topicid和WXPUSER_UID都为空，请至少填写其中一个")
        exit()
    return cks.split("@") , wxpuser_uid.split('@'), topicid, wxpuser_token


async def main():
    cks,wx_uid,topicidid,wxpuser_token =  await check_env()
    for ck in cks:
        abc = Rrbyd()
        await abc.run(ck,wx_uid[cks.index(ck)],topicidid,wxpuser_token,'http://api.doudoudou.fun')  
        

if __name__ == '__main__':
    asyncio.run(main())
