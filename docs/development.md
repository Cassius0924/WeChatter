# 本地部署和 Docker 部署

本文档介绍了 WeChatter 的本地部署和 Docker 部署方法。Docker Compose 部署方法请参考[自述文件](../README.md#快速开始)。

## 目录

- [本地部署](#本地部署)
- [Docker 部署](#docker-部署)

## 本地部署

### 运行 wechatbot-webhook Docker

1. 拉取 wechatbot-webhook 镜像

```bash
docker pull dannicool/docker-wechatbot-webhook
```

2. 运行 wechatbot-webhook

```bash
docker run -d \
--name wxBotWebhook \
-p 3001:3001 \
-e LOGIN_API_TOKEN="<Token>" \
-e RECVD_MSG_API="http(s)://<宿主机IP>:<接收消息端口>/receive_msg" \
dannicool/docker-wechatbot-webhook
```

- `<Token>`：令牌
- `<宿主机IP>`：填入 Docker 的宿主机地址。
- `<接收消息端口>`：设置一个接收消息的端口，默认为 `4000`。

3. 登录微信

使用下面命令查看 wechatbot-webhook 日志中的微信登录二维码，扫码登录微信。

或访问 `http://localhost:3001/login?token=<Token>` 查看微信登录二维码。

```bash
docker logs -f wxBotWebhook
```

### 启动 WeChatter

1. 下载源代码

```bash
git clone https://github.com/Cassius0924/WeChatter
cd WeChatter
```

2. 安装依赖项

```bash
# 如果需要，可创建虚拟环境...

pip install -r requirements.txt
```

3. 复制并编辑配置文件

```bash
cp config.yaml.example config.yaml
vim config.yaml
```

4. 启动 WeChatter

```bash
python3 -m wechatter
```

5. 测试机器人

使用另一个微信给机器人发送 `/help` 指令。

### Docker 部署

### 运行 wechatbot-webhook Docker

Docker 部署同上述[本地部署](#本地部署)，需要运行 `wechatbot-webhook` Docker 容器。

### 运行 WeChatter Docker

1. 拉取 WeChatter 镜像

```bash
docker pull cassius0924/wechatter
```

2. 下载 WeChatter 配置文件

```bash
mkdir WeChatter && cd WeChatter
wget -O config.yaml https://cdn.jsdelivr.net/gh/cassius0924/wechatter@master/config.yaml.exmaple
```

3. 编辑配置文件

```bash
vim config.yaml
```

4. 运行 WeChatter

```bash
docker run -d \
--name WeChatter \
-p 4000:4000 \
-v ./config.yaml:/wechatter/config.yaml \
-e WECHATTER_LOG_LEVEL=INFO \
cassius0924/wechatter
```
