import hashlib
import json
import random
import time
from retry import retry
import requests


class zq:
    def __init__(self):
        self.headers = {"Host": "user.youth.cn",
                        "Connection": "keep-alive",
                        "Accept": "application/json",
                        "Sec-Fetch-Dest": "empty",
                        "X-Requested-With": "XMLHttpRequest",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) "
                                      "AppleWebKit/537.36 (KHTML, "
                                      "like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.9/xiaomi "
                                      "com.miui.hybrid/1.9.0.5 com.youth.kandianquickapp/2.5.7",
                        "Connection": "close"}

    @staticmethod
    def get_data():
        ac_list = []
        with open("./data.json", 'r') as file:
            data = json.load(file)
            for i in range(len(data["users"])):
                ac_list.append(data["users"][i]["zq_read"])
        return ac_list

    @retry(tries=3, delay=3)
    def get_url(self, ac_list):
        url = "https://user.youth.cn/FastApi/article/lists.json?{}&app_version=2.5.7".format(ac_list)
        s_list = []
        n_list = []
        try:
            response = requests.get(url, headers=self.headers, timeout=2)
            time.sleep(1)  # 控制爬取速度
            if response.status_code == 200:
                data = response.json()
                for i in range(len(data["items"])):
                    s_list.append(data["items"][i]["signature"])
                    n_list.append(data["items"][i]["title"])
                return s_list, n_list
            else:
                print("网络错误")
        except Exception as e:
            print(e)
            print("重新尝试自动连接3次，不行我也没辙了")

    @staticmethod
    def cre_sign(s_list):
        sign_list = []
        sign_md5 = []
        key = 'UHLHlqcHLHLH9dPhlhhLHLHGF2DgAbsmBCCGUapF1YChc'
        sign_pre = 'app_version=2.5.7f=1signature='
        for i in range(len(s_list)):
            sign_list.append(sign_pre + s_list[i] + key)
        for i in range(len(sign_list)):
            sign_md5.append(hashlib.md5(sign_list[i].encode('utf-8')).hexdigest())
        return sign_md5

    @retry(tries=3, delay=3)
    def read_article(self, s_list, n_list, sign_md5):
        for i in range(len(s_list)):
            url = "https://user.youth.cn/FastApi/article/complete.json?signature={}&app_version=2.5.7&f=1&sign=".format(
                s_list[i]) + sign_md5[i]
            try:
                response = requests.get(url, headers=self.headers, timeout=2)
                time.sleep(1)  # 控制爬取速度
                if response.status_code == 200:
                    data = response.json()
                    if data["error_code"] == "0":
                        print("阅读" + n_list[i] + "成功" + "获得" + str(data["items"]["read_score"]) + "青豆")
                        print("随机等待" + str(random.randint(30, 35)) + "秒")
                        time.sleep(random.randint(30, 35))
                    else:
                        print("阅读" + n_list[i] + "失败,应该是太频繁了")
                else:
                    print("网络错误")
            except Exception as e:
                print(e)
                print("不知道哪里错了重新尝试自动连接，不行我也没辙了")

    def get_userinfo(self, ac_list):
        url = "https://user.youth.cn/v1/Task/getSign.json?{}&app_version=2.5.7".format(ac_list)
        try:
            response = requests.get(url, headers=self.headers, timeout=2)
            time.sleep(1)  # 控制爬取速度
            if response.status_code == 200:
                data = json.loads(response.text)
                print(data["items"]["user"]["nickname"] + "当前余额：" + data['items']['user']['money'])
            else:
                print("网络错误")
        except Exception as e:
            print(e)
            print("不知道哪里错了重新尝试自动连接，不行我也没辙了")

    def run(self):
        print("============开始运行=============")
        ac_list = self.get_data()
        for i in range(len(ac_list)):
            self.get_userinfo(ac_list[i])
            s_list, n_list = self.get_url(ac_list[i])
            print("第{}个帐号获取到的文章数量为{}".format((i + 1), len(s_list)))
            sign_md5 = self.cre_sign(s_list)
            self.read_article(s_list, n_list, sign_md5)
            self.get_userinfo(ac_list[i])
            print("结束第{}个帐号".format(i + 1))
        print("============结束运行=============")


if __name__ == '__main__':
    start = zq()
    start.run()
