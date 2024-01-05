# 基于WxBotWebhook的微信机器人

## 介绍

基于[wechatbot-webhook](https://github.com/danni-cool/wechatbot-webhook)

## 快速开始

### 运行 wxBotWebhook

1. 拉取 Docker 镜像

```bash
docker pull dannicool/docker-wechatbot-webhook
```

2. 运行 Docker

```bash
docker run -d \
--name wxBotWebhook \
-p 3001:3001 \
-e LOGIN_API_TOKEN="<Token>" \
-e RECVD_MSG_API="http://<内网IP>:<接收消息端口>/receive_msg" \
dannicool/docker-wechatbot-webhook
```

- `<Token>`：登录令牌（不是密码），自己设置一个好记的。
- `<内网IP>`：填入服务器的内网IP，如果是在自己电脑，则填入 `127.0.0.1`。
- `<接收消息端口>`：设置一个接收消息的端口，此项目中默认为 `4000`。

3. 登录微信

使用下面命令查看微信的登录二维码地址：

```bash
curl http://localhost:3001/loginCheck\?token\=<你的Token>
```

然后在浏览器访问输出的登录二维码地址，扫码登录微信。

### 启动服务器

1. 先将项目`git clone`下来：

```bash
git clone https://github.com/Cassius0924/WeChatBot
```

2. 进入项目文件夹

```bash
cd WeChatBot
```

3. 复制配置文件

```bash
cp config.ini.temp config.ini
```

4. 根据`config.ini`内的注释修改配置文件，详见[配置文件](#配置文件)

```bash
vim config.ini
```

5. 启动服务器

```bash
python3 main.py
```

## 配置文件

| 配置项| 解释 | 可选值 | 备注 |
| --- | --- | --- | --- |
| `admin_list` | 设置管理员,用于接收机器人状态变化通知 || 填入管理员名称（不是备注）|
| `is_need_mentioned` | 群命令是否需要`@`机器人 |`True` `Flase`| 默认为 `True` |
| `send_port` | 发送消息的端口 | | 此端口必须和 `wxBotWebhook` 的 Docker 端口相同，默认为 `3001` |
| `recv_port` | 接受消息的端口 | | 此端口必须和 Docker 中 `RECV_MSG_API` 的端口相同 |

6. 测试机器人

使用另一个微信给机器人发送 `/help` 指令。

## 支持功能

目前机器人支持如下指令：

- [x] GPT问答，基于[gpt4free](https://github.com/xtekky/gpt4free)
- [x] 获取B站热搜
- [x] 获取知乎热搜
- [x] 获取微博热搜
- [x] 获取抖音热搜
- [x] 获取GitHub趋势
- [x] 单词/词语翻译
- [x] 获取少数派早报
- [x] 获取历史上的今天
