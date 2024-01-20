# 接收Docker转发过来的消息的接口
import json

from fastapi import FastAPI, Form
from bot_info import BotInfo
from message import Message
from message_parser import MessageParser
from notifier import Notifier
from sqlite.sqlite_manager import SqliteManager
from main import cr

app = FastAPI()


@app.post(cr.recv_api_path)
async def recv_msg(
    type: str = Form(),
    content: str = Form(),
    source: str = Form(),
    isMentioned: str = Form(),
    isSystemEvent: str = Form(),
):
    """接收Docker转发过来的消息的接口"""
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
    BotInfo.update_from_source(source)

    # 判断是否是系统事件
    if isSystemEvent == "1":
        print("收到系统事件")
        handle_system_event(content)
        return

    # 不是系统消息，则是用户发来的消息

    # 构造消息对象
    message = Message(
        type=type,
        content=content,
        source=source,
        is_mentioned=isMentioned,
    )

    # 向用户表中添加该用户
    check_and_add_user(
        user_id=message.source.p_info.id,
        user_name=message.source.p_info.name,
        user_alias=message.source.p_info.alias,
        user_gender=message.source.p_info.gender,
    )

    # DEBUG
    print("==" * 20)
    print(str(message))
    print("==" * 20)

    # 用户发来的消息均送给消息解析器处理
    MessageParser.parse_message(message)

    # return {"success": True, "data": {"type": "text", "content": "hello world！"}}


def handle_system_event(content: str) -> None:
    """判断系统事件类型，并调用相应的函数"""
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


# TODO: 判断传入的参数和数据库中的数据是否一致，若不一致，则更新数据库中的数据
def check_and_add_user(
    user_id: str, user_name: str = "", user_alias: str = "", user_gender: int = -1
) -> None:
    """判断用户表中是否有该用户，若没有，则添加该用户"""
    sqlite_manager = SqliteManager()
    sql = "SELECT * FROM wx_users WHERE wx_id = ?"
    result = sqlite_manager.fetch_one(sql, (user_id,))
    if result is not None:
        return
    # 该用户不存在，添加该用户
    gender = "unknown"
    if user_gender == 1:
        gender = "male"
    elif user_gender == 0:
        gender = "female"
    sql = "INSERT INTO wx_users(wx_id, wx_name, wx_alias, wx_gender) VALUES(?, ?, ?, ?)"
    sqlite_manager.insert(
        "wx_users",
        {
            "wx_id": user_id,
            "wx_name": user_name,
            "wx_alias": user_alias,
            "wx_gender": gender,
        },
    )


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
