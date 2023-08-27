import asyncio
import aiohttp
from typing import Optional, Dict 
from urllib.parse import urlparse
import time
import sys
import os

"""
模板a 采用aiohttp: 作用是 存在不同url,不同host,能自主的选择host，且基础headers变量保持不变，其他headers参数可以自由选择
         
request(url,'get或者post','data可以为空','add_headers为往请求头追加元素必须为字典',headers为替换头)

headers为替换头,当headers 需要修改的参数太多还不如重新弄一个，可以选用这个替换默认头

host 不需要你设置，根据url自动筛选，或者add_headers添加host就会更新了

当 headers里有cookie怎么设置
run方法定义类变量 self.cookie = cookie
async def other_method(self):
    add_header= {"cookie":self.cookie}
    await requests(url,add_headers=add_header)

用async 实现并发可以如下
tasks1 = [self.request(url) for _ in range(并发数)]
responses1 = await asyncio.gather(*tasks1)
for response in responses1:
    print(response)

"""


class template:
    def __init__(self) -> None:
        """
        new model
         
        """
        self.sessions = aiohttp.ClientSession()
        # self._default_headers={   # 没有那么多参数就用这就行了把requst里的注释掉就好了
        #     # 'Host': host,
        #     'User-Agent': 'com.ss.android.ugc.live/260301 (Linux; U; Android 13; zh_CN; M2012K11AC; Build/TKQ1.220829.002; Cronet/TTNetVersion:f2f67850 2023-07-04 QuicVersion:4d847ea3 2023-05-09)',
        #     'Connection': 'close',
        #     'Accept': '*/*',
        #     'Accept-Encoding': 'gzip, deflate',
        #     'sdk-version': '2',
        #     'passport-sdk-version': '203107',
        #     'Cookie': ''
        # }

    
    async def close(self):
        await self.sessions.close()

    async def request(self,url,method='get',data=None, add_headers: Optional[Dict[str,str]]=None, headers=None):
        host = urlparse(url).netloc
        # self._default_headers['Host'] = host
        self._default_headers={
            'Host': host,
            'User-Agent': 'com.ss.android.ugc.live/260301 (Linux; U; Android 13; zh_CN; M2012K11AC; Build/TKQ1.220829.002; Cronet/TTNetVersion:f2f67850 2023-07-04 QuicVersion:4d847ea3 2023-05-09)',
            'Connection': 'close',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'sdk-version': '2',
            'passport-sdk-version': '203107',
        }
        try:
            request_headers = headers or self._default_headers
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

    async def expamget(self):
        pass

    async def post(self):
        pass

    async def run(self):
        cks = ''
        # cks = os.getenv('cks')
        cks_list = cks.split('@')
        for ck in cks_list:   # 碰到#需要变数组同理也可得
            pass
        await self.close()

async def main():
    abc = template()
    await abc.run()  
        

if __name__ == '__main__':
    asyncio.run(main())
