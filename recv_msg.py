# 接收Docker转发过来的消息的接口
import json

from fastapi import FastAPI, Form
from BotInfo import BotInfo
from message import Message
from message_parser import MessageParser
from notifier import Notifier

app = FastAPI()
message_parser = MessageParser()


@app.post("/receive_msg")
async def recv_msg(
    type: str = Form(),
    content: str = Form(),
    source: str = Form(),
    isMentioned: str = Form(),
    isSystemEvent: str = Form(),
):
    # DEBUG
    # print("==" * 20)
    # print(type)
    # print(content)
    # print(source)
    # print(isMentioned)
    # print(isSystemEvent)
    # print("==" * 20)

    # 更新机器人信息（id和name）
    # FIXME: 启动服务器后，只有个人消息才能成功更新机器人信息，群消息无法确定机器人的id和name
    BotInfo.update(source)

    # 判断是否是系统事件
    if isSystemEvent == "1":
        handle_system_event(content)
        return

    # 不是系统消息，则是用户发来的消息
    # 获取发送者的名字
    to_user_name = get_user_name(source)

    # 构造消息对象
    message = Message(
        type=type,
        content=content,
        source=source,
        is_mentioned=isMentioned,
    )

    # DEBUG
    print(str(message))
    print("==" * 20)

    # 用户发来的消息均送给消息解析器处理
    message_parser.parse_message(message, to_user_name)


def get_user_name(source_str: str) -> str:
    source_dict = json.loads(source_str)
    if source_dict["from"] == "":
        return ""
    # return source_dict["from"]["payload"]["name"]
    return source_dict.get("from", {}).get("payload", {}).get("name", "")


# 判断系统事件类型，并调用相应的函数
def handle_system_event(content: str) -> None:
    content_dict: dict = json.loads(content)
    # 判断是否为机器人登录消息
    if content_dict["event"] == "login":
        print("机器人登录成功")
        Notifier.notify_logged_in()
    elif content_dict["event"] == "logout":
        print("机器人已退出登录")
        Notifier.notify_logged_out()
    elif content_dict["event"] == "error":
        pass
    else:
        pass


# type
"""
    "text" | "file" | "urlLink"
"""

# content
"""
    若isSystemEvent为0，则content的格式为：
    "Hello
    若isSystemEvent为1，则content的格式为：
    {
      "event": "login", // login | logout | error
      "user": { // 当前的用户信息，没有则为null
        "_events": {},
        "_eventsCount": 0,
        "id": "@xxxasdfsf",
        "payload": {
          "alias": "",
          "avatar": "",
          "friend": false,
          "gender": 1,
          "id": "@xxx",
          "name": "somebody",
          "phone": [],
          "star": false,
          "type": 1
        }
        "error": ''// js 报错的错误栈信息
      }
    }
    若type为"urlLink"，则content的格式为：
    {
      description: "描述例子",
      thumbnailUrl: "",
      title: "标题例子",
      url: "http://example.url",
    }
"""

# source
"""
    {
        // 消息来自群，会有以下对象，否则为空字符串
        "room": {
          "id": "@@xxx",
          "topic": "abc" // 群名
          "payload": {
            "id": "@@xxxx",
            "adminIdList": [],
            "avatar": "xxxx", // 相对路径，应该要配合解密
            "memberList": [
              {id: '@xxxx', name:'昵称', alias: '备注名' }
            ]
          },
          //以下暂不清楚什么用途，如有兴趣，请查阅 wechaty 官网文档
          "_events": {},
          "_eventsCount": 0,
        },

        // 消息来自个人，会有以下对象，否则为空字符串
        "to": {
            "id": "@xxx",
            "payload": {
                "alias": "", //备注名
                "avatar": "xxx",
                "friend": false,
                "gender": 1,
                "id": "@xxx",
                "name": "xxx",
                "phone": [],
                "signature": "hard mode",
                "star": false,
                "type": 1
            },
            "_events": {},
            "_eventsCount": 0,
          },

        // 消息发送方
        "from": {
          "id": "@xxx",

          "payload": {
            "alias": "",
            "avatar": "xxx",
            "city": "北京",
            "friend": true,
            "gender": 1,
            "id": "@xxxx",
            "name": "abc", //昵称
            "phone": [],
            "province": "北京",
            "star": false,
            "type": 1
          },

          "_events": {},
          "_eventsCount": 0,
        }
    }
"""

# isMentioned
"""
    0 | 1
"""

# isSystemEvent
"""
    0 | 1
"""
