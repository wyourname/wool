"""
用我脚本怕黑号的,大可不必用我的,请删除脚本,觉得自己目前的脚本还行的也请忽略,多有得罪请勿见怪

提现的openid,去提现页面,点一下提现至微信就能抓到的了nickname也一样
url?后面的xxxx即可只要xxxx
包含dfid=&appid=&token=&mid=&clientver=&from=client&clienttime=&userid&uuid...这几个参数即可不要求排序
export kgyycks='xxxx#openid#nickname#ture=2

ture=2 提2块
ture=5 5块
ture=10 10
ture=20 20
其他不提
在 async def submit(self,user,taskid,ap=None):
这个里面修改成你的用户数据,不用你的我怕黑号...,嗯爱用不用,我自己用就行,不改就默认数据了
data1 = {
    "taskid":taskid,
    "t2":"随便完成一个任务的body里就有了", # 只要替换t2和user label就行,其实有没有都不影响完成任务
    "clienttime_ms": str(ts1),
    "user_label": 同样也是复制粘贴就行
    }

"""


import asyncio
import aiohttp
import time
import sys
import datetime
import os
import random
import hashlib
from urllib.parse import parse_qs
import json



class kgyy:
    def __init__(self) -> None:
        """
        这里的请求头是全局的
        基础的内容可以填这里
        添加修改删除如
        self.headers = {"cookie":"xxxxx"}
        self.headers['cookie']='xxxxx'
        del self.header['cookie']

        """

        self.sessions = aiohttp.ClientSession()
        self.headers={
            "user-agent":"Android13-AndroidPhone-11689-130-0-MusicalNoteProtocol-wifi",
            "content-type":"application/json; charset=utf-8",
            "Host":"gateway.kugou.com",
            "accept-encoding":"gzip,deflate",
        }
    
    async def close(self):
        await self.sessions.close()

    async def request(self,url,method='get',data=None,headers=None):
        try:
            if headers:
                self.headers.update(headers)
            async with getattr(self.sessions, method)(url,headers = self.headers, json=data) as response:
                    if response.status == 200:
                        res = await response.text()
                        return json.loads(res)
                    else:
                        print(f"请求失败状态码：{response.status}")
                        res = await response.text()  
                        return json.loads(res)
        except Exception as e:
            print(e)
            return None    

    async def get_param(self,param,ts):
        parsed_params = parse_qs(param)
        dfid = parsed_params.get('dfid', [None])[0]
        appid = parsed_params.get('appid', [None])[0]
        token= parsed_params.get('token', [None])[0]
        mid = parsed_params.get('mid', [None])[0]
        userid = parsed_params.get('userid', [None])[0]
        clientver = parsed_params.get('clientver', [None])[0]
        uuid = parsed_params.get('uuid', [None])[0]
        # print(dfid,appid,mid,clientver,uuid,token)
        param = f'dfid={dfid}&appid={appid}&token={token}&mid={mid}&clientver={clientver}&from=client&clienttime={ts}&userid={userid}&uuid={uuid}'
        #appid=1005clienttime={ts}clientver=11689dfid=10y1NO21sgZ83dq0o31Gx4sAfrom=clientmid=143313187661739409749940452920351916391token=20DChF52So1KC0ay0BS2moJLE3rJUsR0ooIcW1jNKvv1pjjSI4SePM31MsWOkuserid=1963278492uuid=bfc3018cde5108a8b1e7cc1076e01cb6
        key = f'appid={appid}clienttime={ts}clientver={clientver}dfid={dfid}from=clientmid={mid}token={token}userid={userid}uuid={uuid}'
        return param,key


    async def create_sign(self,param,data=None):
            if data:
                key = f'OIlwieks28dk2k092lksi2UIkp{param}{data}OIlwieks28dk2k092lksi2UIkp'
            else:
                key = f'OIlwieks28dk2k092lksi2UIkp{param}OIlwieks28dk2k092lksi2UIkp'
            # print(key)
            new_md5 = hashlib.md5()
            new_md5.update(key.encode('utf-8'))
            secret = new_md5.hexdigest().lower()
            return secret
    
    async def signon(self,user):
        """
        """
        ts = int(time.time())
        param,key = await self.get_param(user,ts)
        # print(param,key)
        today = datetime.datetime.now().strftime("%Y%m%d")
        data1 = {"code":str(today)}
        data = json.dumps(data1)
        signature = await self.create_sign(key,data)
        print("-------执行签到-------")
        url = f'https://gateway.kugou.com/mstc/musicsymbol/v1/task/signon?{param}&signature={signature}'
        res = await self.request(url,'post',data1)
        if res['errcode'] == 0:
            for day in res['data']['list']:
                if day['today'] == 1:
                    print(f"签到获得：{day['award_coins']}币，试着加点金币")
                    await asyncio.sleep(3)
                    double_data = {"code":str(today),"double_code":res['data']['double_code'],"double_award_type":2}
                    ddata = json.dumps(double_data)
                    double_signature = await self.create_sign(key,ddata)
                    url = f'https://gateway.kugou.com/mstc/musicsymbol/v1/task/signon?{param}&signature={double_signature}'
                    res1 = await self.request(url,'post',double_data)
                    if res1['errcode'] == 0:
                        print(f"翻倍成功，获得：{res1['data']['awards']['coins']}币")
                    else:
                        print(res1)
        else:
            print(res['error'])


    async def sign_status(self,user):
        ts = int(time.time())
        param,key = await self.get_param(user,ts)
        signature = await self.create_sign(key)
        url = f'https://gateway.kugou.com/mstc/musicsymbol/v1/task/sign_state?{param}&signature={signature}'
        res = await self.request(url)
        if res['errcode'] == 0:
            for day in res['data']['list']:
                if day['today'] == 1:
                    if day['state'] == 0:
                        print("今日尚未签到，开始签到")
                        await self.signon(user)
                    else:
                        print("今日已签到")
    
    async def task_center(self,user):
        ts = int(time.time())
        param,key = await self.get_param(user,ts)
        signature = await self.create_sign(key)
        url = f'https://gateway.kugou.com/mstc/musicsymbol/v1/system/infos?{param}&signature={signature}'
        res = await self.request(url)
        if res['errcode'] == 0:
            for task in res['data']['tasks']:
                # print(task['state'])
                if task['state']['state'] == 0:
                    print(f"未完成的任务：{task['profile']['name']},可完成最大次数:{task['state']['max_done_count']} 当前：{task['state']['done_count']}")
                    if task['state']['taskid']==1107:
                        if task['state']['lottery']['chances']==1:
                            for lottery in range(task['state']['max_done_count']-task['state']['done_count']):
                                print(f"第{task['state']['done_count']+1+lottery}次抽奖")
                                await self.submit(user,task['state']['taskid'])
                                await asyncio.sleep(15)
                                await self.chances(user)
                        elif task['state']['lottery']['chances']==0:
                            await self.chances(user)
                            await asyncio.sleep(15)
                            await self.submit(user,task['state']['taskid'])
                        else:
                            print("应该没有抽奖了")
                    elif task['state']['taskid']==45:
                        print(f"第{task['state']['done_count']+1}次广告奖励")
                        await self.submit(user,task['state']['taskid'])
                    elif task['state']['taskid']==1108:
                        hour = datetime.datetime.now().hour
                        if hour==10 or hour ==12 or hour ==17 or hour ==21:
                            await self.submit(user,task['state']['taskid'])
                        else:
                            print(f"{task['state']['taskid']}:未到设定时间领取，不领取")
                    elif task['state']['taskid']==1111 or task['state']['taskid']==29 :
                        print(f"id:{task['state']['taskid']},skip")
                    else:
                        await self.submit(user,task['state']['taskid']) 
                    print("休息15-20秒") 
                    await asyncio.sleep(random.randint(15,20))       
                else:
                    print(f"已完成的任务有：{task['profile']['name']}")
                
        else:
            print(res['error'])

    async def chances(self,user):
        ts = int(time.time())
        param,key = await self.get_param(user,ts)
        data1 = {"way":'ad'}
        data = json.dumps(data1)
        signature = await self.create_sign(key,data)
        url = f"https://gateway.kugou.com/mstc/musicsymbol/v1/lottery/exchange?{param}&signature={signature}"
        res = await self.request(url,'post',data1)
        if res['errcode'] == 0:
            print(f"获得抽奖机会+{res['data']['lottery']['chances']}")
        else:
            print(res['error'])
    
    async def submit(self,user,taskid,ap=None):
        ts = int(time.time())
        ts1 = int(time.time()*1000)
        param,key = await self.get_param(user,ts)
        data1 ={"taskid":taskid,
                "t2":"a46276d24d1b73efc00b037f9418b5eb5c7e556efc531398393f29f0f7165491fb34d37faee7a583dd6ae62c7fed5065452b75c0f61058574a453d71e9a153e0af5c3d3eb72508cc3ccf9b50f78a990caa2371427171f55d64e80c3f1dd19b5b5013e520766f9a36e5d39de56dbf",
                "clienttime_ms": str(ts1),
                "user_label":{"val9":2431,"val8":0,"val7":1,"val6":0,"val5":1,"val4":0,"val3":3,"val2":0,"val1":0}
                }
        if ap:
            data1.update(ap)
        if taskid == 1107:
            data1.update({"lottery_pool":[{"id":"1","type":"coin","num":588},{"id":"2","type":"coin","num":228},{"id":"3","type":"coin","num":158},{"id":"4","type":"gift","num":559},{"id":"5","type":"gift","num":557},{"id":"6","type":"coin","num":88},{"id":"7","type":"coin","num":38},{"id":"8","type":"gift","num":459}]})
        elif taskid == 1108:
            hour = datetime.datetime.now().hour
            data1.update({"meal_id": 1 if hour == 10 else 2 if hour == 12 else 3 if hour == 17 else 4 if hour == 21 else data1.get("meal_id")})
        data = json.dumps(data1)
        signature = await self.create_sign(key,data)
        url = f'https://gateway.kugou.com/mstc/musicsymbol/v1/task/submit?{param}&signature={signature}'
        res = await self.request(url,'post',data1)
        if res['errcode'] == 0:
            if taskid == 1107:
                if res['data']['awards']['extra']['lottery_gift']['type'] == 'coin':
                    print(f"id:{taskid} + {res['data']['awards']['coins']}币")
                else:
                    print(f"抽到 res['data']['awards']")
            else:
                print(f"id:{taskid} +{res['data']['awards']['coins']} 币")
                if 'double_code' in res['data']:
                    print(f"id:{taskid} 可以加金币,试着加金币")
                    await asyncio.sleep(random.randint(10,15))
                    ap = {'double_code':res['data']['double_code'],'double_award_type':2}
                    await self.submit(user,taskid=taskid,ap=ap)
        else:
            print(f"id：{taskid}错误信息:{res['error']}")


    async def info(self,user):
        ts = int(time.time())
        param,key = await self.get_param(user,ts)
        signature = await self.create_sign(key)
        url = f'https://gateway.kugou.com/mstc/musicsymbol/v1/user/info?{param}&signature={signature}'
        res = await self.request(url)
        if res['errcode'] == 0:
            print(f"用户信息：{res['data']['base']['nickname']} 余额：{res['data']['account']['balance_coins']}")
            if 20000 <= res['data']['account']['balance_coins'] < 50000 and self.draw =='ture=2':
                await self.draw_money(user, 20000)
            elif 50000<= res['data']['account']['balance_coins'] < 100000 and self.draw =='ture=5':
                await self.draw_money(user, 50000)
            elif 100000<= res['data']['account']['balance_coins'] < 200000 and self.draw =='ture=10':
                await self.draw_money(user, 100000)
            elif res['data']['account']['balance_coins'] >= 200000 and self.draw =='ture=20':
                await self.draw_money(user, 200000)
            else:
                print(f"{res['data']['account']['balance_coins']} 狗狗币,不提现")
        else:
            print(res['error'])

    async def draw_money(self,user, money):
        ts = int(time.time())
        param,key = await self.get_param(user,ts)
        data1 = {"openid": self.openid,"nickname":self.nickname,"total_fee":int(money/100),"coins":money,"channel":3}
        data = json.dumps(data1)
        signature = await self.create_sign(key,data)
        url = f'https://gateway.kugou.com/mstc/musicsymbol/v1/withdraw/apply?{param}&signature={signature}'
        res = await self.request(url,'post',data1)
        if res['errcode'] == 0:
            print(f"提现{money/10000} 元成功！")
        else:
            print(f"提现{money/10000} 元失败！{res}")

    async def check_env(self):
        cks = os.getenv('kgyycks')
        if cks is None:
            print('你没有填写酷狗音乐ck环境变量，请填写：kgyycks 变量，格式：dfid&mid&uuid&token&....#openid#nickname#是否提现（是就填ture=2,不提就false）')
        else:
            cks_list = cks.split('@')
            correct_data = []
            for cka in cks_list:
                if len(cka.split('#')) == 4:
                    print(f"第{cks_list.index(cka)+1}个账号填写格式正确")
                    correct_data.append(cka)
                else:
                    print("第{cks_list.index(cka)}账号填写格式不正确，格式：dfid&mid&uuid&token&....#openid#nickname#是否提现（是就填ture,不提就false）")
            return correct_data

    async def run(self):
        cks_list = await self.check_env()
        for cks in cks_list:
            print(f"=========开始第{cks_list.index(cks)+1}个账号运行===========")
            ck,openid,nickname,draw = cks.split('#')
            self.openid = openid
            self.nickname = nickname
            self.draw = draw
            await self.info(ck)
            await self.sign_status(ck)
            await asyncio.sleep(random.randint(15,20))  
            await self.task_center(ck)
            print(f"=========结束第{cks_list.index(cks)+1}个账号运行===========")
        await self.close()

   


async def main():
    abc = kgyy()
    await abc.run()  
        

if __name__ == '__main__':
    asyncio.run(main())
