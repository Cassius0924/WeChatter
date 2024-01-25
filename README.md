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
- `<内网IP>`：填入服务器的**内网IP**。如果是在自己电脑，则填入 `127.0.0.1`。
- `<接收消息端口>`：设置一个接收消息的端口，此项目中默认为 `4000`。

3. 登录微信

使用下面命令查看 Docker 日志中的微信二维码，扫码登录微信。

```bash
docker logs -f wxBotWebhook
```

### 启动服务器

1. 下载源代码

```bash
git clone https://github.com/Cassius0924/WeChatter
cd WeChatter
```

2. 复制并编辑配置文件

```bash
cp config.ini.example config.ini
vim config.ini
```

3. 启动服务器

```bash
python3 main.py
```

4. 测试机器人

使用另一个微信给机器人发送 `/help` 指令。

## 配置文件

项目根目录中的 `config.ini.example` 为配置文件模版，首次启动项目前需要复制一份配置文件，并命名为 `config.ini`。 编辑 `config.ini`。

下表为配置项解释：

### ⚙️ WeChatter 配置

| 配置项 | 解释 | 备注 |
| --- | --- |  --- |
| `wechatter_port` | WeChattter服务器的端口，接受消息的端口 | 默认为 `4000`，需和 `wxbotwebhook` Docker 的 `RECV_MSG_API` 参数的端口一致 |

### ⚙️ WxBotWebhook 配置

| 配置项 | 解释 | 备注 |
| --- | --- |  --- |
| `wx_webhook_port` | 发送消息的端口 | 默认为 `3001`，需和 `wxBotWebhook` 的 Docker 端口一致 |
| `wx_webhook_recv_api_path` | 接收消息的接口路径 | 默认为 `/receive_msg`，此路径为 `RECV_MSG_API` 的路径 |

### ⚙️ Admin 配置

| 配置项 | 解释 | 备注 |
| --- | --- |  --- |
| `admin_list` | 设置管理员,用于接收机器人状态变化通知 | 填入管理员微信名（不是备注） |
| `admin_group_list` | 与 `admin_list` 同理，接收机器人状态变化通知 | 填入群名称（不是群备注） |

### ⚙️ Bot 配置

| 配置项 | 解释 | 备注 |
| --- | --- |  --- |
| `bot_name` | 微信机器人的名字 | 微信名称，非微信号 |

### ⚙️ Chat 配置

| 配置项 | 解释 | 备注 |
| --- | --- |  --- |
| `command_prefix` | 机器人命令前缀 | 默认为 `/` ，可以设置为`>>`、`!` 等 |
| `need_mentioned` | 群聊中的命令是否需要@机器人 | 默认为 `True` |

### ⚙️ Copilot GPT4 配置

| 配置项 | 解释 |  备注 |
| --- | --- |  --- |
| `cp_gpt4_api_host` | CopilotGPT4 服务的API地址 | 默认为 `http://localhost` |
| `cp_gpt4_port` | CopilotGPT4 服务的端口 | 默认为 `8080` |
| `cp_token` | Copilot 的 Token | 以 `ghu_` 开头的字符串 |

### ⚙️ GitHub Webhook 配置

| 配置项 | 解释 | 备注 |
| --- | --- |  --- |
| `github_webhook_enabled` | 功能开关，是否接收 GitHub Webhook | 默认为 `False` |
| `github_webhook_api_path` | 接收 GitHub Webhook 的接口路径 | 默认为 `/webhook/github` |
| `github_webhook_receiver_list` | 接收 GitHub Webhook 的微信用户 |  |
| `github_webhook_receive_group_list` | 接收 GitHub Webhook 的微信群 | |

### ⚙️ Message Forwarding 配置

| 配置项 | 子项 | 解释 | 备注 |
| --- | --- |  --- | --- |
| `message_forwarding_enabled` | | 功能开关，是否开启消息转发 | 默认为 `False` |
| `message_forwarding_rules` | | 消息规则列表，每个规则包含三个字段：`froms`, `to_persons` 和 `to_groups` | 一个由字典组成的JSON列表，最后的 `]` 不能单独一行 |
| ➤➤➤ | `froms` | 消息转发来源列表，即消息发送者 | 可以填多个用户名称或群名称 |
| ➤➤➤ | `to_persons` | 消息转发目标用户列表，即消息接收用户 | 可以填多个用户名称或为空列表 |
| ➤➤➤ | `to_groups` | 消息转发目标群列表，即消息接收群 | 可以填多个群名称或为空列表 |

## 支持的命令

- [x] GPT问答，基于 [Copilot-GPT4-Server](https://github.com/aaamoon/copilot-gpt4-service)
- [x] 获取B站热搜
- [x] 获取知乎热搜
- [x] 获取微博热搜
- [x] 获取抖音热搜
- [x] 获取GitHub趋势
- [x] 单词/词语翻译
- [x] 获取少数派早报
- [x] 获取历史上的今天
- [x] 二维码生成器
- [x] 待办清单（TODO）
- [x] 获取人民日报PDF

> [!TIP]
> 更多命令使用 `/help` 命令查看。

## 支持的功能

- [x] 消息转发，需[配置](# ⚙️ GitHub Forwarding 配置)

## 支持的 Webhook

- [x] GitHub 仓库 Webhook，需[配置](# ⚙️ GitHub Webhook 配置)

> [!NOTE]
> 需要在 GitHub 仓库 Settings 中添加 Webhook
