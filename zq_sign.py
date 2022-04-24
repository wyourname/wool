import requests
import json


def get_data():
    ac_list = []
    with open('./data.json', 'r') as f:
        data = json.load(f)
        for i in range(len(data['users'])):
            ac_list.append(data['users'][i]['zq_read'])
    return ac_list


def sign(ac_list):
    url = 'https://user.youth.cn/FastApi/Task/sign.json?{}'.format(ac_list)
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.9/xiaomi "
                      "com.miui.hybrid/1.9.0.5 com.youth.kandianquickapp/2.5.7 ({\"packageName\":\"com.miui.home\","
                      "\"type\":\"shortcut\",\"extra\":{\"original\":{\"packageName\":\"com.miui.quickappCenter\","
                      "\"type\":\"url\",\"extra\":{\"scene\":\"\"}},\"scene\":\"api\"}})",
        "Accept-Language": "zh-CN,zh;q\u003d0.9,en;q\u003d0.8",
        "Host": "user.youth.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"}
    r = requests.get(url, headers=headers).json()
    if r['success'] == True:
        print('签到成功')
    else:
        if r['error_code'] == "403":
            print('今日已签到')
        else:
            print('签到失败')


def run():
    print("======开始签到======")
    ac_list = get_data()
    for i in range(len(ac_list)):
        print("帐号{}".format(i + 1))
        sign(ac_list[i])
    print("======签到结束======")


if __name__ == '__main__':
    run()
