"""
这是我的WXPUSER_TOKEN,你可以直接拿来用
export WXPUSER_TOKEN="AT_aYF2532tqjrD4dX90OrJsuiflscRureX"
微信打开链接:https://wxpusher.zjiecode.com/wxuser/?type=1&id=50341#/follow
关注wxpuser app 订阅公众号就能获取你的uid
export WXPUSER_UID="UID_xxxxx"
||||||
微信阅读:小阅阅
邀请链接:https://ot43562.tvtg.top:10259/yunonline/v1/auth/31cf5cf7e3f49fd7ce1738ac295dcc4f?codeurl=ot43562.tvtg.top:10259&codeuserid=2&time=1696733275
走不走我邀请都无所谓的,写代码只是爱好,你能用我写的本我就很开心了
抓  wi29252.masx.top下的 cookie: ysmuid=xxxxx;
只要xxxxxx
export xyycks='xxxxxxxx@xxxxxxxx'
export multi_xyy='true'  # 并发开关，可以不填
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

new Env('小阅阅阅读')
"""

import requests
import time
import random
import os,threading,re
from typing import Optional, Dict 
from urllib.parse import urlparse, parse_qs,quote


class Xyy:
    def __init__(self) -> None:
        """
        """
        self.url = 'http://1695469567.snak.top/yunonline/'     
             
        
    def request(self, url, method='get', data=None, add_headers: Optional[Dict[str, str]] = None, headers=None,dtype='json'):
        host = urlparse(url).netloc
        _default_headers = {
            'Host': host,
            "Connection": "keep-alive",
            # "Upgrade-Insecure-Requests":"1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090719) XWEB/8391 Flue",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "cookie":f"{self.cookie}"
        }
        try:
            request_headers = headers or _default_headers
            if add_headers:
                request_headers.update(add_headers)
            # print(request_headers)
            with requests.request(method, url, headers=request_headers, data=data) as response:
                if response.status_code == 200:
                    if dtype == 'json':
                        return response.json()  # 返回JSON数据
                        
                    else:
                        return response.text
                else:
                    print(f"请求失败状态码:{response.status_code}")
                    return None
        except Exception as e:
            print(e)
            return None
        
    def init_read(self):
        url = 'http://1695471164.snak.top?cate=0'
        res = self.request(url,dtype='text')
        if not res:
            print(f"【用户{self.index}】:初始化请求获取失败")
            return
        # print(res)
        pattern = r'href="(http://[^"]+)"'
        match = re.search(pattern, res)
        pattern = r'href="([^"]+)"[^>]*>提现</a>'
        matches = re.findall(pattern, res)
        if matches:
            self.exchange_url = matches[0]
        if match:
            ex_url = match.group(1)
            parsed_url = urlparse(ex_url)
            query_params = parse_qs(parsed_url.query)
            self.unionid = query_params.get('unionid', [])[0] if 'unionid' in query_params else None
            self.request_id = query_params.get('request_id', [])[0] if 'request_id' in query_params else None
        else:
            print("No URL found")


    def account(self):
        add_header = {'Accept':'application/json, text/javascript, */*; q=0.01','cookie':self.cookie}
        ts = int(time.time()*1000)
        url = self.url + f'v1/gold?time={ts}&unionid={self.unionid}'
        # print(url)
        res = self.request(url,add_headers=add_header)
        if res and res['errcode'] == 0:
            print(f"【用户{self.index}】:金币 {res['data']['day_gold']}, 剩余文章{res['data']['remain_read']}")
            if res['data']['remain_read'] >0:
                print(f"【用户{self.index}】:获取开篇文章url")
                time.sleep(3)
                urla = self.start()
                self.request(urla,dtype='text')
                host = urlparse(urla).netloc
                query_parameters = parse_qs(urlparse(urla).query)
                uk = query_parameters.get('uk', [])[0] if query_parameters.get('uk') else None
                if uk:
                    for i in range(1,res['data']['remain_read']+1):
                        print(f"【用户{self.index}】【阅读】:第{i}篇文章")
                        self.do_read_task(host,uk=uk)
                        if self.cont == False:
                            break
                        time.sleep(random.randint(1,3))
                else:
                    print("没有发现uk")
            else:
                print(f"没有可阅读的文章了")
        else:
            print(f"出错了:{res}")
    
    def start(self):
        url = self.url+'v1/wtmpdomain'
        data = f'unionid={self.unionid}'
        add_headers = {"Content-Lenght": str(len(data)),"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","Origin":"http://1695469567.snak.top","Referer":"http://1695469567.snak.top/"}
        res = self.request(url,'post',data=data, add_headers=add_headers)
        if res['errcode'] == 0:
            print(f"【用户{self.index}】【文章】: url加载成功")
            return res['data']['domain']
        else:
            return None

    
    def do_read_task(self,origin,uk):
        url = f'https://nsr.zsf2023e458.cloud/yunonline/v1/do_read?uk={uk}'
        add_header= {'origin': f'https://{origin}','accept':'application/json, text/javascript, */*; q=0.01','sec-fetch-site':'cross-site'}
        res = self.request(url,add_headers=add_header)
        if res:
            if res['errcode'] == 0:
                link_url = res['data']['link']
                time.sleep(random.randint(2,4))
                self.jump(url=link_url,uk=uk,origin=origin)
            else:
                print(f"【用户{self.index}】【阅读】:{res['msg']}")
                if res['errcode'] == 407:
                    self.cont = False
        else:
            print("发生了点意外,休息3秒")
            time.sleep(3)
            self.do_read_task(origin,uk)


    def jump(self,url, uk,origin):
        url = url+'?/'
        host = urlparse(url).netloc
        headers = {
            "Host":host,
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166 Mobile Safari/537.36 MMWEBID/2651 MicroMessenger/8.0.40.2420(0x28002851) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding":"gzip, deflate",
            "X-Requested-With":"com.tencent.mm",
            "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding":"gzip, deflate",
            'Cookie': self.cookie
        }
        res = requests.get(url,headers=headers,allow_redirects=False)
        location= res.headers.get('Location')
        if self.varification(location):
            ts = random.randint(8,16)
            print(f"【用户{self.index}】【等待】:休息{ts}秒")
            time.sleep(ts)
            self.complete_task(uk,ts,origin)

    def complete_task(self,uk,ts, origin):
        tsp = int(time.time())
        add_header= {'origin': f'https://{origin}','accept':'application/json, text/javascript, */*; q=0.01','sec-fetch-site':'cross-site'}
        url = f'https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={uk}&time={ts}&timestamp={tsp}000'
        res = self.request(url,add_headers=add_header)
        if res and res['errcode'] == 0:
            print(f"【用户{self.index}】【奖励】:{res['msg']}, +{res['data']['gold']}币,今天阅读数:{res['data']['day_read']},剩余{res['data']['remain_read']}")
            if res['data']['gold'] == 0:
                self.cont = False
        else:
            # print(res)
            print(f"【用户{self.index}】:领取阅读币失败{res['msg']}")
            if res['errcode'] == 407:
                self.cont = False
    
    def varification(self,url):
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        if '__biz' in query_parameters:
            biz_value = query_parameters['__biz'][0]
            if biz_value in self.check_data:
                print(f"【用户{self.index}】【检测】: {self.check_data[biz_value][0]}公众号")
                encoded_url = quote(url)
                self.wxpuser(f"小阅阅【用户{self.index}】检测,请90秒内点击阅读",encoded_url)
                print(f"【用户{self.index}】【等待】:请手动前往wxpuser点击阅读")
                start_time = int(time.time())
                while True:
                    if self.get_read_state():
                        print(f"【用户{self.index}】【阅读】:已手动阅读,休息3秒")
                        time.sleep(3)
                        return True
                    if int(time.time()) - start_time > 90:
                        print(f"【用户{self.index}】【阅读】:超时未阅读，终止本次阅读")
                        self.cont = False
                        return False
                    time.sleep(1)
            else:
                print(f"【用户{self.index}】【文章】:没有检测")
                return True
        else:
            print(f"【用户{self.index}】【文章】:__biz parameter not found in the URL")
            return True

    def init_chekc_dict(self):
        print(f"【用户{self.index}】:初始化阅读后台检测状态")
        url = self.aol + f'/check_dict?user={self.cookie}&value=0'
        res = self.request(url)
        if res and res['status'] == 200:
            self.check_data = dict(res['check_dict'])
            print(f"【用户{self.index}】:初始化状态成功")
        else:
            print(f"【用户{self.index}】:索取字典出现错误{res},休息5秒")
            time.sleep(5)
            self.init_chekc_dict()
    
    def get_read_state(self, max_retry=3):
        url = self.aol + f'/read/state?user={self.cookie}&value=0'
        try:
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
        except Exception as e:
            print(f"捕获到请求状态异常：{e}")
            if max_retry == 0:
                return False
            time.sleep(3)
            self.get_read_state(max_retry-1)

    def wxpuser(self,title,url):
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
                <div class="title">用户a小阅阅,务必在一分半钟内点击阅读</div>
                <div class='button'><a href="self.aol/redirect?user=uuu&value=0&timestamp=tsone&wxurl=link">点击阅读检测文章</a></div>
                <div class="tips">
                    <p>如果错过时间未能阅读, 会导致当天收益下降或者没有收益</p>
                    <p>请留意消息推送时间点依照你的定时计划</p>
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
        # print(content)
        wxpuser_url = 'http://wxpusher.zjiecode.com/api/send/message'
        res = requests.post(wxpuser_url, json=data).json()
        if res['success'] == True:
            print(f"【用户{self.index}】【通知】:检测发送成功！")
        else:
            print(f"【用户{self.index}】【通知】:发送失败！！！！！")

    def user_gold(self):
        add_header = {'Accept':'application/json, text/javascript, */*; q=0.01','cookie':self.cookie,'Referer':'http://1695469567.snak.top/?cate=0'}
        ts = int(time.time()*1000)
        url = self.url + f'v1/gold?unionid={self.unionid}&time={ts}'
        res = self.request(url,add_headers=add_header)
        if res['errcode'] == 0:
            current_gold = res['data']['last_gold']
            print(f"【用户{self.index}】【余额】:{current_gold}金币")
            tag = 8000
            if int(current_gold) >= tag:
                gold = int(int(current_gold)/1000)*1000
                unionid,request_id = self.exchange()
                if unionid and request_id:
                    # print(unionid,request_id)
                    self.with_draw(unionid=unionid,request_id=request_id,gold=gold)
                else:
                    print(f"【用户{self.index}】:没有获取到提现的参数，待修复")
            else:
                print(f"【用户{self.index}】【余额】:{current_gold} < {tag} ,不满足条件")
        else:
            print("出现一些问题")
        
    def exchange(self):
        host = urlparse(self.exchange_url).netloc
        add_headers = {"Referer":f'http://{host}/?cate=0'}
        res = self.request(self.exchange_url,add_headers=add_headers,dtype='text')
        if not res:
            print(f"【用户{self.index}】【用户】:获取unionid, snid出错")
            return None,None
        pattern_unionid = r'var unionid = \'(.*?)\';'
        pattern_request_id = r'var request_id = "(.*?)";'
        match_unionid = re.search(pattern_unionid, res, re.DOTALL)
        match_request_id = re.search(pattern_request_id, res, re.DOTALL)
        # print(match_request_id,match_unionid)
        
        if match_unionid:
            unionid_value = match_unionid.group(1)
        else:
            unionid_value = None
        if match_request_id:
            request_id_value = match_request_id.group(1)
        else:
            request_id_value = None
        if unionid_value and request_id_value:
            return unionid_value,request_id_value
        else:
            return None,None


    def with_draw(self, unionid,request_id,gold):
        host = urlparse(self.exchange_url).netloc
        url1 = f"http://{host}/yunonline/v1/user_gold"
        host = urlparse(self.exchange_url).netloc
        data1 = f"unionid={unionid}&request_id={request_id}&gold={gold}"
        add_headers = {"Content-Lenght": str(len(data1)),"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","Origin":f"http://{host}","Referer":self.exchange_url,'X-Requested-With': 'XMLHttpRequest'}
        res = self.request(url1,'post',data=data1,add_headers=add_headers)
        if res['errcode'] == 0:
            print(f"【用户{self.index}】【提现】:{res['data']['money']}元")
            url2 = self.url+'v1/withdraw'
            data2 = f"unionid={unionid}&signid={request_id}&ua=2&ptype=0&paccount=&pname="
            {"Content-Lenght": str(len(data2)),"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","Origin":f"http://{host}","Referer":self.exchange_url}
            res = self.request(url2,'post', data=data2,add_headers=add_headers)
            if res['errcode'] == 0:
                print(f"【用户{self.index}】【提现】:{res['msg']}")
            else:
                print(f"提现失败 原因:{res['msg']}")
        else:
            print(res)
    
    def run(self, index, ck, app_token, wx_uid, topicid, check_url, sleep_time=None):
        self.aol = check_url
        self.index = index
        if sleep_time:
            print(f"【用户{self.index}】:随机休息{sleep_time}秒，我怕你点不了那么多")
            time.sleep(sleep_time)
        print(f"【用户{self.index}】【开始任务】: 第{index}个的账号")
        self.cont = True
        self.topicid = topicid
        self.wxpuser_token = app_token
        self.wxpuser_uid = wx_uid
        self.cookie = f'ysmuid={ck}'
        self.init_chekc_dict()
        self.init_read()
        self.account()
        self.user_gold()
        print(f"【用户{self.index}】【结束任务】: 第{index}个 账号")


def check_env():
    wxpuser_token = os.getenv("WXPUSER_TOKEN")
    topicid = os.getenv("WXPUSER_TOPICID")
    wxpuser_uid = os.getenv("WXPUSER_UID")
    cks = os.getenv('xyycks')
    if cks is None:
        print("小悦悦ck为空,请去抓包格式:cookie:'ysmuid=xxxxx.....'只要xxxxx 多账户请用@分割")
        print("cookie填写,export xyycks='xxxxxx'")
        exit()
    correct_data = []
    for index ,ck in enumerate(cks.split("@")):
        # 也许这里可以添加你的变量检测是否合规
        # Here you can write some code.
        if 'ysmuid=' in ck:
            print(f"账号[{index+1}]:请手动去除cookie里面的ysmuid=")
        else:
            correct_data.append(ck)
    if wxpuser_token is None:
        print("wxpuser的apptoken为空,前往官网注册创建一个app,复制应用token和微信关注wxpuser公众号获取uid")
        print("获取完请在配置文件填写:export WXPUSER_TOKEN=AT_aYF2.....\nexport WXPUSER_UID=UID_....")
        exit()
    if topicid is None and wxpuser_uid is None:
        print("wxpuser的topicid和WXPUSER_UID都为空,请至少填写其中一个")
        exit()
    return wxpuser_token, topicid, wxpuser_uid.split('@'), correct_data


def test_api(url):
    print("开始测试检测服务可用性")
    api_url = url + '/read/announcement'
    res = requests.get(api_url)
    if res.status_code == 200:
        result = res.json()
        print(f"【公告】:{result['messages']}")
        return True
    else:
        return False


def main():
    apptoken, topicid, wx_uids, cks_list = check_env()  # 这里顺序不能搞乱了
    aol = []
    for url in ['http://api.doudoudou.fun']:
        if test_api(url):
            print(f"{url} 联通性测试通过")
            aol.append(url)
    if len(aol) == 0:
        print("当前检测服务不可用,请稍后再试")
        exit()
    random_sleep_list = [i * random.randint(50, 65) for i in range(len(cks_list))]
    from random import choice
    # 检查是否启用并发
    multi = os.environ.get("multi_xyy")
    if multi and multi.lower() == "true":
        threads = []
        for index, ck in enumerate(cks_list):
            xyy = Xyy()
            thread = threading.Thread(target=xyy.run, args=(index + 1, ck, apptoken, wx_uids[index], topicid, choice(aol), random_sleep_list[index]))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    else:
        for index, ck in enumerate(cks_list):
            xyy = Xyy()
            xyy.run(index + 1, ck, apptoken, wx_uids[index], topicid, choice(aol))



if __name__ == '__main__':
    main()
