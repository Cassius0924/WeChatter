import json
from typing import Union

from fastapi import APIRouter, Form, UploadFile
from loguru import logger

import wechatter.config as config
from wechatter.bot.bot_info import BotInfo
from wechatter.commands import commands
from wechatter.message import MessageHandler
from wechatter.message_forwarder import MessageForwarder
from wechatter.models.message import Message
from wechatter.sender import notifier
from wechatter.sqlite.sqlite_manager import SqliteManager

router = APIRouter()


@router.post(config.wx_webhook_recv_api_path)
async def recv_wechat_msg(
    type: str = Form(),
    content: Union[UploadFile, str] = Form(),
    source: str = Form(),
    isMentioned: str = Form(),
    isSystemEvent: str = Form(),
):
    """接收Docker转发过来的消息的接口"""

    # 更新机器人信息（id和name）
    BotInfo.update_from_source(source)

    # 判断是否是系统事件
    if isSystemEvent == "1":
        logger.info(f"收到系统事件：{content}")
        handle_system_event(content)
        return

    # 不是系统消息，则是用户发来的消息
    if type == "file":
        logger.info(f"收到文件：{content.filename}")
        return

    # 解析命令
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

    if config.message_forwarding_enabled:
            MessageForwarder(config.message_forwarding_rule_list).forward_message(message)

    # 传入命令字典，构造消息处理器
    message_handler = MessageHandler(commands)
    # 用户发来的消息均送给消息解析器处理
    message_handler.handle_message(message)

    # 快捷回复
    # return {"success": True, "data": {"type": "text", "content": "hello world！"}}


def handle_system_event(content: str) -> None:
    """判断系统事件类型，并调用相应的函数"""
    content_dict: dict = json.loads(content)
    # 判断是否为机器人登录消息
    if content_dict["event"] == "login":
        print("机器人登录成功")
        notifier.notify_logged_in()
    elif content_dict["event"] == "logout":
        print("机器人已退出登录")
        notifier.notify_logged_out()
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
