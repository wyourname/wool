# wechatloader 使用指南

> [!WARNING]
> **请认真阅读以下使用说明与条款，否则对于使用过程中出现的任何问题，概不答复。**

## ⚠️ 重要声明与使用条款

1.  **仅供学习研究**：本仓库仅供个人学习与研究，请勿用于任何非法用途。
2.  **技术门槛**：本项目需要使用者具备基础的Linux知识，包括但不限于 `docker`、`docker-compose` 的安装与使用，以及Linux依赖管理。操作时建议使用超级用户权限。**不熟悉Linux环境（如Windows、群晖）或无相关经验的用户请谨慎使用。**
3.  **协议状态**：协议已失效，不再提供，请勿联系。
4.  **服务说明 (付费)**：
    *   **风险提示**：当前协议版本（855）存在封号风险，强烈建议使用小号进行测试。
    *   **购买流程**：请先到机器人 `@Mark_oool_bot` 发送命令 `/register`，然后再进行支付。
    *   **支付方式**：发送命令 `/pay passtoken 你的支付宝口令`。
    *   **价格**：35元。
    *   **退款政策**：5天内随时退款，看到消息后会立即处理。
    *   **环境要求**：请确保您的Linux服务器与您位于**同城的本地网络环境**。
    *   **更新**：安装完后请务必使用部署命令更新。
5.  **技术支持**：对于使用过程中出现的任何Bug，本人不保证能够修复，请慎重联系。对于一般使用疑问，概不回复。
6.  **中途退款**：若已使用多日但决定停止使用，请携带您的Token联系我，我将全额退款。请注意，退款后您将无法使用本仓库的任何代码，并请自觉从您的计算机上删除本仓库的所有相关代码，否则后果自负。
7.  **脚本状态**：目前可用的阅读脚本不多，且无法保证及时更新。若已购买，可联系退款。
8.  **使用者素质要求**：
    > 使用者本身要具备勇于尝试、勤奋坚韧、细心谨慎、不怕吃苦的精神。贪图安逸只会阻碍自身成长，依赖他人只会让人丧失斗志。如你不具备以上品行，请绕道而行。
    >
    > Users themselves must possess the spirit of courage to try new things, diligence and perseverance, attentiveness and prudence, and willingness to endure hardships. Seeking comfort will only hinder personal growth, while relying on others will sap one's fighting spirit. If you lack these qualities, please look elsewhere.

---

## 🚀 部署步骤

### 环境准备
- 一台支持 `Debian` 的 Linux 服务器。
- 已安装 `curl`, `wget`, `docker`。

### 安装命令

1.  dockeramd64的命令：
    ```bash
    docker run -d --name wechatloader -v $PWD/wechatloader:/root -p 8011:8011 --restart unless-stopped wyourname/wechatloader:amd64-latest
    
    ```

---

## 🛠️ 使用说明

> [!IMPORTANT]
> **这不是免费服务。** 协议有风险，登录需谨慎，**请勿使用主力微信号登录**，否则出现问题本人概不承担任何责任。如不同意，请立刻放弃部署。

1.  **服务器环境**：请确保您的Linux服务器已安装 `docker`，并且服务器**没有**挂代理，也**不位于**国外或云端。

2.  **配置密钥**：在 `ip:8011` 的网页界面中填写您的 `passtoken` (密钥)，保存后方可正常使用。

3.  **登录状态**：
    *   首次登录后约4小时会掉线。
    *   点击“唤醒登录”后，可维持约3天在线。
    *   心跳日志中出现 `missing port in address` 警告是正常的，通过“唤醒登录”即可消除（也可忽略，不影响使用）。

4.  **青龙面板配置**：
    在青龙的配置文件 (`config.sh` 或 `extra.sh`) 中添加以下环境变量：
    ```bash
    export WECHAT_SERVER='http://你部署的ip:8011'
    ```

5.  **当前可用脚本**：
    *   `wxkele` (可乐阅读，已黑号)
    *   `wxyidian` (壹点联盟, 未维护)
    *   `search_reward` (搜搜小奖, 已黑号停止维护，尚能用)
    *   `ddz` (点点赚)
    *   `ddlm` (叮叮联盟, 未维护)
    *   `sillydog` (傻狗阅读)

---

## 📜 运行脚本

1.  **更新容器**：部署成功后，用浏览器打开 `http://你部署的ip:8011` 登录微信。**首次打开网页请立即点击“更新容器”**。如有更新，请按提示操作，等待20秒后手动重启容器以完成更新。

2.  **获取 `wxid`**：登录后，在网页后台的日志中找到类似 `wxid_xxxxxxx` 的字符串，这就是您的微信ID。

3.  **配置青龙环境变量**：确保已在青龙配置文件中添加 `WECHAT_SERVER` 变量（见上一节）。

4.  **准备通用脚本模板**：
    *   在青龙的脚本目录中新建一个文件夹（例如 `wechat_scripts`）。
    *   下载 `common.py` 文件到该文件夹中，作为脚本模板。
    *   前往 定时任务 - 添加任务 名称随便
    *   填写命令
        ```bash
        task wechat_scripts/common.py --script 脚本名      
        ```

6.  **邀请码**：对于需要邀请码的脚本，请自行寻找。

7.  **定时任务**：阅读类任务建议定时为 `2小时一次`，即一天8次。

8.  **网络代理**：如果在下载 `common.so` 时遇到问题，可以在脚本中设置代理。找到 `PROXY_URL = ''` 这一行，修改为：
    ```python
    PROXY_URL = 'https://git.3675676.xyz.com/' # 或者其他可用的GitHub代理
    ```

---

## 👨‍💻 开发

-   **API文档**: `http://你部署的ip:8011/api/document/page`
