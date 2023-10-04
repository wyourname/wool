"""
代码请勿用于非法盈利，一切与本人无关，该代码仅用于学习交流，请阅览下载24小时内删除代码
new Env("57box")
57box
export 57boxcks='手机号#密码@手机号#密码'
# 顺序不要颠倒
我的本大部分的并发格式 脚本名_multi='true'

"""



import asyncio
from typing import Optional, Dict
from urllib.parse import urlparse
import aiohttp
import time
import os


class Box:
    def __init__(self) -> None:
        self.sessions = aiohttp.ClientSession()
        # self.token = ''

    async def close(self):
        await self.sessions.close()

    async def request(self, url, method='get', add_headers: Optional[Dict[str, str]] = None, data=None, headers=None):
        host = urlparse(url).netloc
        _default_headers = {
            'Host': host,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Linux; Android 13; Mi 10 Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.128 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/32.727272)',
        }
        try:
            request_headers = headers or _default_headers
            if add_headers:
                request_headers.update(add_headers)

            async with getattr(self.sessions, method)(url, headers=request_headers, data=data) as response:
                if response.status == 200:
                    return await response.json()  # 返回text或json 看情况
                else:
                    print(f"请求失败状态码：{response.status}")
                    return await response.json()
        except Exception as e:
            print(e)
            return None

    async def user_info(self):
        url = f'https://www.57box.cn/app/index.php?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=getuserinfo&m=greatriver_lottery_operation&token={self.token}&source=app'
        try:
            res = await self.request(url=url)
            if res['errno'] == 0:
                print(f"[信息][用户{self.index}]: {res['data']['nickname']} 积分: {res['data']['integral']}")
                if int(float(res['data']['integral'])) >= 120:
                    await self.open_the_box()
            else:
                print(f"[错误][用户{self.index}]:获取用户信息失败")
        except Exception as e:
            print(e)
            print("[异常] 获取用户信息时发生异常")

    async def get_task(self):
        url = f'https://www.57box.cn/app/index.php?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=getstarparameter&m=greatriver_lottery_operation&token={self.token}'
        task_list = []
        try:
            res = await self.request(url=url)
            if res['errno'] == 0:
                task_list = res['data']['tasklist']
                print(f"[信息][用户{self.index}]:获取任务列表成功")
                filtered_tasks = [task for task in task_list if 'state' in task and task['state'] == 0 and task['task_type'] in ['5', '6', '7']]
                # print(filtered_tasks)
                # for i in task_list:
                    # print(i)
                for task in filtered_tasks:
                    # print(task)
                    await self.complete_task(task)
                    await asyncio.sleep(2)
            else:
                print(f"[错误][用户{self.index}]:获取任务列表失败")
        except Exception as e:
            print(e)
            print(f"[异常][用户{self.index}]: 获取任务列表时发生异常")

    async def complete_task(self, task):
        for _ in range(int(task['valid_day_times'])):
            print(f"[信息][用户{self.index}] 开始任务: {task['task_title']}")
            url = f'https://www.57box.cn/app/index.php?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=uptaskinfo&token={self.token}'
            if task['id'] in ["35","39"]:
                data = {
                'm': 'greatriver_lottery_operation',
                'id': task['id'],
                'answer': ''
                }
            if task['id'] == "26":
                data = {
                'm': 'greatriver_lottery_operation',
                'id': task['id'],
                'answer': '228899'
                }
            if task['id'] == "30":
                data = {
                'm': 'greatriver_lottery_operation',
                'id': task['id'],
                'answer': '普通物品不可分解'
                }
            # print(data)
            try:
                res = await self.request(url=url, method='post', data=data)
                # print(res)
                if res['errno'] == 0:
                    print(f"[通知][用户{self.index}]:{task['task_title']}: {res['message']}")
                    time.sleep(3)
                else:
                    # print(res)
                    print(f"[错误][用户{self.index}]:做任务{task['task_title']}时失败")
                    time.sleep(3)
                    break
            except Exception as e:
                print(e)
                print(f"[异常][用户{self.index}]:做任务{task['task_title']}时发生异常")
            # break
    
    async def open_the_box(self):
        url = f'https://www.57box.cn/app/index.php?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=openthebox&m=greatriver_lottery_operation&box_id=303&paytype=1&zhonglvtool_id=&zhonglvtool_choiceprize=&num=1&token={self.token}&source=app'
        res = await self.request(url)
        if not res:
            print(f"[盲盒][用户{self.index}]:请求出错")
        if res['errno'] == 0:
            print(f"[盲盒][用户{self.index}]:抽到{res}")
        else:
            print(f"[盲盒][用户{self.index}]:开盒失败{res['message']}")



    async def get_token(self, phone, passwd):
        data = f'mobile={phone}&password={passwd}&password2=&code=&invite_uid=0&source=app'    
            
        url = 'https://www.57box.cn/app/index.php?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=login&m=greatriver_lottery_operation'
        add_headers = {'Content-Length':str(len(data)),'Accept-Encoding':'gzip'}
        # print(add_headers)
        res = await self.request(url,'post',data=data,)
        if not res:
            print(f"[用户{self.index}]登录获取token失败")
            return None
        if res['errno'] == 0:
            print(f"[登录][用户{self.index}]:{res['message']}")
            self.token=res['data']['token']
        else:
            print(f"[登录][用户{self.index}]:失败{res}")
        


    async def run(self,index, ck):
        self.index = index
        phone,passwd = ck.split('#')
        await self.get_token(phone,passwd)
        await self.user_info()
        await self.get_task()
        await self.user_info()
        await self.close()


async def get_msg():
    url = 'http://api.doudoudou.fun/other/message?name=57box'
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
    cks = os.getenv('57boxcks')
    if cks is None:
        print("你没有填写57boxcks")
        exit()
    correct_data = []
    for index ,ck in enumerate(cks.split("@")):
        # 也许这里可以添加你的变量检测是否合规
        # Here you can write some code.
        if len(ck.split('#')) != 2:
            print(f"账号{index+1}的格式填写错误应为:手机号#密码")
        else:
            correct_data.append(ck)
    return correct_data,

async def main():
    await get_msg()
    cks_list = await check_env()
    # 检查是否存在环境变量 multi
    use_concurrency = os.environ.get('57box_multi', 'false').lower() == 'true'
    tasks = []
    for index, ck in enumerate(cks_list):
        abc = Box()
        task = abc.run(index+1, ck[index])
        tasks.append(task)
    if use_concurrency:  # 如果是true 那么就执行并发
        await asyncio.gather(*tasks)  # 并发执行任务
    else:  # 如果是false 那么就串行执行
        for task in tasks:
            await task  


if __name__ == '__main__':
    asyncio.run(main())
