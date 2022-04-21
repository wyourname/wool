import hashlib
import requests
import json
import time
import random


# @Author: 王权富贵233
# 新手上路嘀嘀嘀
# 大佬看不上小白又嫌弃，不爱请勿伤害 键下积德
# 使用方法：把uid=xxxx&token=xxxx&token_id=xxxxx
# 放在参数里面即可帐号用@隔开脚本暂时写到这有空再改进没有多的号没有测试多账户运行

def get_article_url(url1, header1):
    print('我要开始获取文章链接啦，请稍等···')
    signature_list = []
    signature_name = []
    response = requests.get(url1, headers=header1)
    response_json = eval("u" + "\'" + response.text + "\'")
    response_final = json.loads(response_json)
    for i in range(len(response_final['items'])):
        signature_list.append(response_final['items'][i]['signature'])
    for j in range(len(response_final['items'])):
        signature_name.append(response_final['items'][j]['title'])
    return signature_list, signature_name


def create_sign(signature_list):
    sign_list = []
    sign_key = []
    sign = []
    key = 'UHLHlqcHLHLH9dPhlhhLHLHGF2DgAbsmBCCGUapF1YChc'
    sign_url = 'app_version=2.5.7f=1signature='
    for i in range(len(signature_list)):
        sign_list.append(sign_url + signature_list[i])
        sign_key.append(sign_url + signature_list[i] + key)
    for j in range(len(sign_key)):
        sign.append(hashlib.md5(sign_key[j].encode('utf-8')).hexdigest())
    return sign


def request_article(signature_list, signature_name, sign):
    for i in range(len(signature_list)):
        url = 'https://user.youth.cn/FastApi/article/complete.json?signature={}&app_version=2.5.7&f=1&sign='.format(
            signature_list[i]) + sign[i]
        response = requests.get(url)
        response_final = response.json()
        if response_final['error_code'] == "0":
            print(
                '正在阅读第' + str(i + 1) + '文章：' + signature_name[i] + '获取成功增加了{}青豆'.format(
                    response_final['items']['read_score']))
            print("本次请求间隔时间随机等待时间{}秒".format(random.randint(30, 35)))
            time.sleep(random.randint(30, 35))
        elif response_final['error_code'] == "10015":
            print('阅读文章' + signature_name[i] + '操作失败，应该是时间间隔太短，请稍后再试')
            print("本次增加一次请求间隔时间随机等待{}秒".format(random.randint(5, 10)))
            time.sleep(random.randint(5, 10))
        else:
            print('签名不正确，等我修复···')


if __name__ == '__main__':
    account = ''
    list_count = account.split('@')
    url1 = 'https://user.youth.cn/FastApi/article/lists.json?{}&app_version=2.5.7'
    header1 = {"User-Agent": "Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 ("
                             "KHTML, "
                             "like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.9/xiaomi "
                             "com.miui.hybrid/1.9.0.5 com.youth.kandianquickapp/2.5.7"}
    print('==============' + "开始运行" + '==============')
    for i in range(len(list_count)):
        print('正在开始第{}个帐号的请求，每次12篇文章'.format(i))
        url = url1.format(list_count[i])
        signature_list, signature_name = get_article_url(url, header1)
        print('获取到的文章列表为：' + str(len(signature_list)))
        sign = create_sign(signature_list)
        request_article(signature_list, signature_name, sign)
    print('==============' + "结束运行" + '==============')
