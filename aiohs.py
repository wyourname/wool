# cython: language_level=3
# author@ wangquanfugui233
# aiohs.py

import asyncio
import aiohttp
from typing import Optional, Dict 
from urllib.parse import urlparse,parse_qs,urlencode
import time, re, random,os,datetime 


class hs:
    def __init__(self) -> None:
        self.sessions = aiohttp.ClientSession()
    
    async def close(self):
        await self.sessions.close()

    async def request(self,url,method='get',data=None, add_headers: Optional[Dict[str,str]]=None, headers=None):
        host = urlparse(url).netloc
        _default_headers={
            'Host': host,
            'User-Agent': 'com.ss.android.ugc.live/260301 (Linux; U; Android 13; zh_CN; M2012K11AC; Build/TKQ1.220829.002; Cronet/TTNetVersion:f2f67850 2023-07-04 QuicVersion:4d847ea3 2023-05-09)',
            'Connection': 'close',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'sdk-version': '2',
            'passport-sdk-version': '203107',
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
            print(f"请求出现错误：{e}")
            return None
        
    async def update_url(self,before_url, url_tail,refresh=True):
        old_url = before_url+url_tail
        # host = urlparse(old_url).netloc
        if refresh:
            ts= time.time()
            url = re.sub(r'(_rticket=[^&]+)', f'_rticket={str(int(ts*1000))}', old_url)
            url = re.sub(r'(ts=[^&]+)', f'ts={str(int(ts))}', url)
            return url
        else:
            return old_url
    
    # 执行任务的核心
    async def complete_task(self,complete_url,task_name,token): 
        n_url = await self.update_url(complete_url,self.url,refresh=False)
        payload = f'task_name={task_name}&auto_finish=false&token={token}'
        add_headers = {
            "Content-Length": str(len(payload)),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie":self.cookie,
            "x-argus":self.argus,
            "x-ladon":self.ladon
        }
        res = await self.request(n_url,'post',data=payload, add_headers=add_headers)
        if res['status_code'] == 0:
            print(f"任务：{task_name}--> +{res['data']['task_done_award']['flame_amount']}火苗")
            if task_name == 'treasure_chest_check_in':
                return res
        else:
            print(f"任务{task_name}失败：{res}")

    async def task_center(self,n):
        p_url = 'https://hotsoon.snssdk.com/hotsoon/janus/flame/management/panel/?'
        n_url = await self.update_url(p_url,self.url)
        add_headers = {"cookie": self.cookie}
        res = await self.request(n_url,add_headers=add_headers)
        if res['status_code'] == 0:
            user = res['data']['user_flame_info']
            print(f"用户{n}:可提现余额{user['data']['can_with_draw_money']}, 今天火苗：{user['data']['td_flame_count']}")
            self.money = user['data']['can_with_draw_money']
            task = res['data']['task_info']['data']
            if "new_user_task_part" in task:
                for task_a in task['new_user_task_part']['task_list']:
                    if task_a['task_name'] == 'check_in_v2' :  # 每日签到
                        await self.daily_sign(task_a)
                    elif task_a['task_name'] == 'ad':   # n分钟/次 广告
                        await self.watch_ad(task_a)               
                    elif task_a['task_name'] == 'watch_video_bonus_guide':
                        pass
                    else:
                        print(f"存在未知任务:{task_a['task_name']}")
            # 不在新用户列表中的任务
            if 'task_list' in task:
                for task_b in task['task_list']:
                    if task_b['task_name'] == 'ad':
                        await self.watch_ad(task_b)
                        await asyncio.sleep(3)   
                        break

            await asyncio.sleep(3)
            # 开宝箱任务
            if "treasure_chest_info" in res['data']:
                treasure = res['data']["treasure_chest_info"]['data']
                await self.open_treasure(treasure=treasure)
        else:
            print(res['status_message'])  

    async def daily_sign(self,task_a):
        print("========检查今日签到状态========")
        print(f"签到状态：{task_a['check_in_v2_task']['check_in_today']}")
        if task_a['check_in_v2_task']['check_in_today'] is False:
            print("尚未签到，开始签到")
            c_url = 'https://hotsoon.snssdk.com/hotsoon/flame/task_system/task_done/?'
            await self.complete_task(complete_url=c_url,task_name=task_a['task_name'], token=task_a['check_in_v2_task']['token'])
            await asyncio.sleep(random.randint(10,20))
        else:
            print("今天已签到")

    # ^^^^对应task_center
    async def watch_ad(self, task_a):
        ad_task = task_a.get('ad_task')
        if ad_task:
            await self.handle_ad_task(ad_task, task_a['task_name'])
        else:
            print("今天的广告任务看完了")

    # ^^^^^
    async def handle_ad_task(self, ad_task, main_task_name):
        print(f"{ad_task['sub_title']}")
        task_time = ad_task['last_award_timestamp']
        next_time = ad_task['cooling_time']
        before_time = datetime.datetime.fromtimestamp(task_time)
        ts1 = time.time()
        print(f"上次执行时间{before_time}")
        if (task_time + next_time) < ts1:
            ad_token = ad_task.get('token')
            if ad_token:
                await self.handle_advertisement(ad_token, main_task_name)
            else:
                print("当前广告已看完")
        else:
            print(f"每{next_time/60}分钟看广告时间未到")

    # ^^^^
    async def handle_advertisement(self, ad_token, main_task_name):
        ts = random.randint(20, 25)
        print(f"看广告休息 {ts} 秒")
        await asyncio.sleep(ts)
        c_url = 'https://hotsoon.snssdk.com/hotsoon/flame/task_system/task_done/?'
        await self.complete_task(complete_url=c_url, task_name=main_task_name, token=ad_token)
        await asyncio.sleep(3)

    # 开箱 对于task_center
    async def open_treasure(self, treasure):
        if 'token' in treasure and 'last_award_timestamp' in treasure:
            await self.handle_treasure_with_timestamp(treasure)
        elif 'token' in treasure and 'last_award_timestamp' not in treasure:
            print("上次开箱时间在昨天")
            await self.handle_opening_treasure(treasure)
        else:
            print(f"【开宝箱】： {treasure['finished_toast']}")

    # ^^^^^
    async def handle_treasure_with_timestamp(self, treasure):
        ts = time.time()
        timestamp = treasure['last_award_timestamp']
        cooldown = treasure['cooling_time']
        if (timestamp + cooldown) < ts:
            await self.handle_opening_treasure(treasure)
        else:
            next_time = datetime.datetime.fromtimestamp(timestamp + cooldown)
            print(f"下次宝箱时间: {next_time}")


    # ^^^^^^
    async def handle_opening_treasure(self, treasure):
        c_url = 'https://hotsoon.snssdk.com/hotsoon/flame/task_system/task_done/?'
        res = await self.complete_task(complete_url=c_url, task_name=treasure['task_name'], token=treasure['token'])
        if "treasure_chest_ad_info" in res['data']:
            treasure_chest_ad_info = res['data']['treasure_chest_ad_info']
            if 'ad_token' in treasure_chest_ad_info:
                ts = random.randint(15, 20)
                print(f"等待{ts} 秒，加广告激励金币")
                await asyncio.sleep(ts)
                await self.complete_task(complete_url=c_url, task_name=treasure_chest_ad_info['ad_task_name'], token=treasure_chest_ad_info['ad_token'])
            else:
                print("当前宝箱没有看广告看了")
    
    # 看视频赚火苗
    async def get_flame_task_info(self):
        print("【任务】：=====>刷视频")
        c_url = 'https://api5-normal-c-hl.amemv.com/hotsoon/flame/task_info/?'
        n_url = await self.update_url(c_url,self.url,refresh=True)
        add_header = {
            'cookie': self.cookie
        }
        res = await self.request(n_url,add_headers=add_header)
        if res['status_code'] == 0:
            if res['data']['has_next'] ==1:
                flame_token = res['data']['next_token']
                await self.cycle_flame_videos(flame_token,1)
            else:
                print("今天没有可看的视频了,明天再来")
        else:
            print(f"获取视频token失败{res}")

    async def cycle_flame_videos(self,token, i):
        try:
            if i != 11:
                c_url = 'https://api5-normal-c-lf.amemv.com/hotsoon/flame/task_done/?'
                n_url = await self.update_url(c_url, self.url, refresh=False)
                payload = f'token={token}'
                add_header = {'Content-Length': str(len(payload)),
                              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
                              "Cookie": self.cookie,
                              "x-argus": self.argus, 
                              "x-ladon": self.ladon
                              }
                res = await self.request(n_url,'post',data=payload,add_headers=add_header)
                if res['status_code'] == 0:
                    print(f"第{i}个【视频】： +{res['data']['flame_amount']}火苗")
                    if res['data']['has_next'] == 1 and res['data']['flame_amount'] >10:
                        st = random.randint(25,30)
                        print(f"休息{st}秒,再执行第{i+1}次看视频")
                        await asyncio.sleep(st)
                        await self.cycle_flame_videos(res['data']['next_token'],i+1)
                    else:
                        print("可能没有视频了，或者收益过低就不浪费时间了")
                        # print(f"{res['data']['strong_show']['text']},{res['data']['strong_show']['tips']}")
                else:
                    print(f"看视频出错{res}")
            else:
                print("本次运行看视频到达设定次数了")
        except Exception as e:
            print(e)
            exit(0)

    async def extract_params(self,base_url, target_url, tag):
        # 解析目标 URL
        target_parsed = urlparse(target_url)
        target_params = parse_qs(target_parsed.query) 
        # 解析基础 URL
        base_parsed = urlparse(base_url)
        # 筛选出与目标 URL 参数相同的参数
        filtered_params = {param: target_params[param][0] for param in target_params if param in base_parsed.query}
        filtered_params['request_tag_from'] = tag
        params = urlencode(filtered_params)
        return params

    async def with_draw_info(self):
        base_url = 'https://hotsoon.snssdk.com/hotsoon/janus/flame/withdraw/panel/?request_tag_from=h5&iid=222&device_id=aaa&ac=wifi&channel=xiaomi_8663_store_64&aid=8663&app_name=aweme_hotsoon&version_code=260300&version_name=26.3.0&device_platform=android&os=android&ssmix=a&device_type=M2012K11AC&device_brand=Redmi&language=zh&os_api=33&os_version=13&manifest_version_code=260301&resolution=1080*2320&dpi=440&update_version_code=26309900&_rticket=1691718432501&package=com.ss.android.ugc.live&mcc_mnc=46001&cpu_support64=true&host_abi=arm64-v8a&is_guest_mode=0&app_type=normal&minor_status=0&appTheme=light&need_personal_recommend=1&is_android_pad=0&ts=1691718431&md=0'
        target_url = 'https://example.com/page?'+self.url
        params = await self.extract_params(base_url,target_url,'h5')
        panel = 'https://hotsoon.snssdk.com/hotsoon/janus/flame/withdraw/panel/?'
        n_url = await self.update_url(panel, params,refresh=True)
        add_headers = {"cookie":self.cookie,"x-argus":self.argus,"x-ladon":self.ladon}
        res = await self.request(n_url,add_headers=add_headers)
        if res['status_code'] ==0:
            for money in res['data']['direct_withdraw_package']['data']['alipay'][::-1]:
                if (money['amount']/100) <= self.money:
                    print(f"试着提现{(money['amount']/100)}元")
                    await self.with_draw(money['amount'],money['token'])
                    break
                else:
                    print(f"{(money['amount']/100)}> {self.money} 钱不够") 
        else:
            print(f"获取提现token出错{res}")

    async def with_draw(self,money,token):
        base_url = 'https://hotsoon.snssdk.com/hotsoon/janus/flame/withdraw/panel/?request_tag_from=h5&iid=222&device_id=aaa&ac=wifi&channel=xiaomi_8663_store_64&aid=8663&app_name=aweme_hotsoon&version_code=260300&version_name=26.3.0&device_platform=android&os=android&ssmix=a&device_type=M2012K11AC&device_brand=Redmi&language=zh&os_api=33&os_version=13&manifest_version_code=260301&resolution=1080*2320&dpi=440&update_version_code=26309900&_rticket=1691718432501&package=com.ss.android.ugc.live&mcc_mnc=46001&cpu_support64=true&host_abi=arm64-v8a&is_guest_mode=0&app_type=normal&minor_status=0&appTheme=light&need_personal_recommend=1&is_android_pad=0&ts=1691718431&md=0'
        target_url = 'https://example.com/page?'+self.url
        params = await self.extract_params(base_url,target_url,'lynx')
        payload = f'package={money}&input_type=1&payment_platform=0&__hideErrorToast=true&token={token}'
        draw = 'https://api5-normal-c-lf.amemv.com/hotsoon/flame/direct_withdraw/handle/?'
        n_url = await self.update_url(draw, params,refresh=True)
        add_headers = {'Content-Length': str(len(payload)),'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',"Cookie":self.cookie,"x-argus":self.argus,"x-ladon":self.ladon}
        res = await self.request(n_url,'post',data=payload,add_headers=add_headers)
        if res['status_code'] == 0:
            print(f"提现{(money/100)}元成功，请留意支付宝到账")
        else:
            print(f"提现失败 {res}")



    async def run(self):
        cks = os.getenv('hscks')
        cks_list = cks.split('@')
        for ck in cks_list:   # 碰到#需要变数组同理也可得
            print(f"==========开始用户{cks_list.index(ck)+1}==========")
            url,cookie,argus,ladon = ck.split('#')
            self.url = url
            self.cookie = cookie
            self.argus = argus
            self.ladon = ladon
            await self.task_center(cks_list.index(ck)+1)
            await asyncio.sleep(3)
            await self.get_flame_task_info()
            await asyncio.sleep(3)
            await self.with_draw_info()
            print(f"==========结束用户{cks_list.index(ck)+1}==========")
        await self.close()

async def main():
    abc = hs()
    await abc.run()  
        

if __name__ == '__main__':
    asyncio.run(main())
