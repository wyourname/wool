import requests

class model:
    def __init__(self) -> None:
        """
        最开始的模板，但是很多时候我都用不上它了，因为这个代码有个局限性，日后就体会出来了，但个别的爬虫项目不支持aiohttp,那么就用的上它
        这里的请求头是全局的
        基础的内容可以填这里
        添加修改删除如
        self.headers = {"cookie":"xxxxx"}
        self.headers.update({"cookie":"zzzz","xxx":"aaa"})
        self.headers['cookie']='xxxxx'
        del self.header['cookie']
        """
        self.session = requests.Session()
        self.headers = {}

    def close(self):
        self.session.close()

    def request(self, url, method='get', data=None, headers=None):
        try:
            if headers:
                self.headers.update(headers)
            response = self.session.request(method, url, headers=self.headers, data=data)
            if response.status_code == 200:
                return response.json()  # 返回json数据
            else:
                print(f"请求失败状态码：{response.status_code}")
                return response.json()  # 同理由可得
        except Exception as e:
            print(e)
            return None

    def expamget(self):
        pass

    def post(self):
        pass

    def run(self):
        cks = ''
        # cks = os.getenv('cks')
        cks_list = cks.split('@')
        for ck in cks_list:   # 碰到#需要变数组同理也可得
            self.headers['cookie'] = 'ck'
            print(f"将cookie：{ck}添加到headers中")
            print(self.headers)
            self.headers['cookie'] = "abc"
            print(self.headers)
            pass
        self.close()

def main():
    abc = model()
    abc.run()

if __name__ == '__main__':
    main()
