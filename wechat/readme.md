# 请认真阅读以下使用说明与条款,否则对于使用过程中出现的任何问题概不答复 

1. 本仓库为个人学习与研究，仅供学习参考，请勿用于非法用途。

### 2. 使用本仓库内任何代码均需要基础的linux知识,包括但不限于docker docker-compose 安装 linux依赖。切换到超级用户权限执行命令。小白请绕道而行！！！！！！！！！。windows 群晖请绕道而行。

### 3. 部署安装完成后请周末时间联系 获取token 其他时间拒绝受理。不接受请绕道而行。售出不退，购买前慎重考虑，且不接受使用咨询，请仔细阅读脚本相关公告。周末购买价格为35元其余时间50元。支付宝口令即可。

4. 对于使用过程中出现任何bug 本人不一定能修复，请慎重联系，对于使用有疑问我概不回复。

5. 对于使用了很多天但却中途不想用了，请带上你的token 联系我，我将全款退回给你，但需要注意的是本仓库内任何代码你将无法使用，也请你从你的计算机上删除本仓库任何有关代码，否则后果自负。

6. 对于阅读脚本目前并没有多少可用的，请小白绕道而行，我无法及时更新脚本。若已购买，请联系退款。

7. 使用者本身要具备勇于尝试、勤奋坚韧、细心谨慎、不怕吃苦的精神。贪图安逸只会阻碍自身成长，依赖他人只会让人丧失斗志。如你不具备以上品行，请绕道而行。
Users themselves must possess the spirit of courage to try new things, diligence and perseverance, attentiveness and prudence, and willingness to endure hardships. Seeking comfort will only hinder personal growth, while relying on others will sap one's fighting spirit. If you lack these qualities, please look elsewhere.

## 部署步骤：

1. mkdir -p wechat && cd wechat

2. wget https://git.365676.xyz/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/install_wechatloader.sh -O install_wechatloader.sh && chmod +x install_wechatloader.sh && sudo ./install_wechatloader.sh

(openwrt 安装wechatloader 则用 wget https://git.365676.xyz/https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/wechat/openwrt_install.sh -O openwrt_install.sh && chmod +x openwrt_install.sh && sudo ./openwrt_install.sh)

linux ssh 执行,支持Debian ，使用前安装curl wget docker 再运行命令，群晖、windows请离开

## 使用步骤：

### 注意：这是并非是免费服务

0. 协议有风险，登录需谨慎，请勿使用主力微信号登录，否则出现问题本人概不承担任何责任，如不同意，请立刻放弃部署

1. 请确保你的linux有安装了docker，请确保你的服务器不是挂着代理或者你的服务器位于国外、云服务器

2. 填写passtoken: 也就是密钥，填写保存方可正常使用 

3. 第一次登录4小时掉线 点唤醒登录后3天一掉，介意勿用 

4. 本地部署后在青龙配置文件添加 export WECHAT_SERVER='http://你部署的ip:8011' 

5. 当前可用脚本:wxkele (可乐已黑号)、wxyidian(壹点联盟,未维护)、search_reward(搜搜小奖，已黑号停止维护，尚能用)、ddz(点点赚)、  ddlm(叮叮联盟，未维护) sillydog（傻狗阅读）脚本说明运行起来就能看到了

## 运行脚本:

1. 部署后成功后浏览器打开 ip:8011登录微信, 打开网页第一时间就得点更新容器，如有更新请立即更新，等待提示20s后需要您手动重启容器完成程序替换

2. wxid是什么? 打开网页你会看到后台日志显示 wxid_xxxxxxx 就是你的微信id。

3. 在青龙容器的配置文件添加 export WECHAT_SERVER='http://你部署的ip:8011'

4. 复制脚本https://raw.githubusercontent.com/wyourname/wool/refs/heads/master/script/common.py 到青龙脚本目录，新建一个文件夹，名字随意，然后把common.py文件复制进去当作模板保存即可。

5. 在新建的文件夹创建一个新的py文件，名字随意，比如我要跑可乐阅读 则命名为kele.py 将 commom.py的内容复制到kele.py kele.py脚本内的SCRIPT_NAME='test'修改为SCRIPT_NAME='wxkele',依次类推，如果你不能理解请绕道而行。

6. 阅读脚本集合【wxkele (可乐已黑号)、wxyidian(壹点联盟)、search_reward(搜搜小奖，已黑号停止维护，尚能用)、 ddlm(叮叮联盟)、sillydog(傻狗阅读)】对于邀请，可以看公告，也可以自行寻找其他人的邀请码。我对你们的人头不感兴趣

7. 阅读类任务定时 一天8次即可 2小时一次。

8. 下载common.so的时候遇到问题在脚本处 PROXY_URL = '' 添加github代理 自行寻找 格式：PROXY_URL = 'https://ghproxy.com/'，如果你不能理解请绕道而行。


## Development:

1. 开发文档: http://ip:8011/api/document/page
