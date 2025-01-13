第一步：mkdir -p wechat && cd wechat

第二步：wget https://git.kfc50.us.kg/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/install_wechatloader.sh && chmod +x install_wechatloader.sh && sudo ./install_wechatloader.sh


(openwrt 安装wechatloader 则用 wget https://git.kfc50.us.kg/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/openwrt_install.sh && chmod +x openwrt_install.sh && sudo ./openwrt_install.sh)


linux执行,支持Debian ，使用前安装curl wget docker 再运行命令

使用须知：
 ## 注意：这是付费  50（这个价格是暂时不卖了）

0.协议有风险，登录需谨慎，请勿使用主力微信号登录，否则出现问题本人概不承担任何责任，如不同意，请立刻放弃部署

1.请确保你的linux有安装了docker，请确保你的服务器不是挂着代理或者你的服务器位于国外、云服务器

2.填写passtoken: 也就是密钥，填写保存方可正常使用 

3.第一次登录4小时掉线 点头像重新登录三天后才掉的，介意勿用 

4.本地部署后在青龙配置文件添加 export WECHAT_SERVER='http://你部署的ip:8011' 

5.当前可用脚本:wxkele (可乐已黑号)、wxyidian(壹点联盟)、search_reward(搜搜小奖，已黑号停止维护，尚能用)、ddz(点点赚)  ddlm(叮叮联盟)脚本说明运行起来就能看到了

6. 试用3天,第三天才打钱,没打钱我就删token就行了, 出现问题删除容器就行了，你们不配合，我也懒得卖你们了

使用步骤:

1. 部署后成功后浏览器打开 ip:8011登录微信, 打开网页第一时间就得点更新容器，如有更新请立即更新，等待提示20s后需要您手动重启容器完成程序替换

2. wxid是什么? 打开网页你会看到后台日志显示 wxid_xxxxxxx 就是你的微信id。

3. 在青龙配置文件添加 export WECHAT_SERVER='http://你部署的ip:8011'

4. 复制脚本https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/script/common.py 到青龙脚本目录，新建一个文件夹，名字随意，然后把common.py文件复制进去保存即可。

5. 将common.py文件的内容复制创建一个新文件，名字随意，比如我要跑可乐阅读 则命名为kele.py 将 kele.py 脚本内的SCRIPT_NAME='test'修改为SCRIPT_NAME='wxkele',依次类推【wxkele (可乐已黑号)、wxyidian(壹点联盟)、search_reward(搜搜小奖，已黑号停止维护，尚能用)、ddz(点点赚)  ddlm(叮叮联盟)、sillydog(傻狗阅读)】

6. 阅读类任务定时 一天8次即可 2小时一次。

7. 下载common.so的时候遇到问题在脚本处 PROXY_URL = '' 添加github代理 自行寻找 格式：PROXY_URL = 'https://ghproxy.com/'
