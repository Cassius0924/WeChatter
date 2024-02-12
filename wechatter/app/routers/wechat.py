import json
from typing import Union

from fastapi import APIRouter, Form, UploadFile
from loguru import logger

import wechatter.config as config
from wechatter.bot.bot_info import BotInfo
from wechatter.commands import commands
from wechatter.database import WechatGroup, WechatMessage, WechatUser, make_db_session
from wechatter.message import MessageHandler
from wechatter.message_forwarder import MessageForwarder
from wechatter.models.message import Message
from wechatter.models.message.group_info import GroupInfo
from wechatter.models.message.person_info import PersonInfo
from wechatter.sender import notifier

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
    # 向群组表中添加该群组
    add_group(message.source.g_info)
    # 向用户表中添加该用户
    add_user(message.source.p_info)
    # 向消息表中添加该消息
    add_message(message)
    # TODO: 添加自己发送的消息，等待 wechatbot-webhook 支持

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
    """
    判断系统事件类型，并调用相应的函数
    """
    content_dict: dict = json.loads(content)
    # 判断是否为机器人登录消息
    if content_dict["event"] == "login":
        logger.info("机器人登录成功")
        notifier.notify_logged_in()
    elif content_dict["event"] == "logout":
        logger.info("机器人已退出登录")
        notifier.notify_logged_out()
    elif content_dict["event"] == "error":
        pass
    else:
        pass


def add_group(group_info: GroupInfo) -> None:
    """
    判断群组表中是否有该群组，若没有，则添加该群组
    """
    if group_info is None:
        return
    with make_db_session() as session:
        g = session.query(WechatGroup).filter(WechatGroup.id == group_info.id).first()
        if g is None:
            g = WechatGroup.from_group_info(group_info)
            session.add(g)
            # 逐个添加群组成员，若存在则更新
            for member in group_info.member_list:
                u = session.query(WechatUser).filter(WechatUser.id == member.id).first()
                if u is None:
                    u = WechatUser.from_member_info(member)
                    session.add(u)
                    session.commit()
                    logger.info(f"用户 {member.name} 已添加到数据库")
                else:
                    # 更新用户信息
                    u.name = member.name
                    u.alias = member.alias
                    session.commit()

            session.commit()
            logger.info(f"群组 {group_info.name} 已添加到数据库")
        else:
            # 更新群组信息
            g.name = group_info.name
            session.commit()


def add_user(user_info: PersonInfo) -> None:
    """
    判断用户表中是否有该用户，若没有，则添加该用户
    """
    with make_db_session() as session:
        u = session.query(WechatUser).filter(WechatUser.id == user_info.id).first()
        if u is None:
            u = WechatUser.from_person_info(user_info)
            session.add(u)
            session.commit()
            logger.info(f"用户 {user_info.name} 已添加到数据库")
        else:
            # 更新用户信息
            u.name = user_info.name
            u.alias = user_info.alias
            u.gender = user_info.gender.value
            u.province = user_info.province
            u.city = user_info.city
            u.is_star = user_info.is_star
            u.is_friend = user_info.is_friend
            session.commit()


def add_message(message: Message) -> None:
    """
    添加消息到消息表
    """
    with make_db_session() as session:
        m = WechatMessage.from_message(message)
        session.add(m)
        session.commit()
        logger.info(f"消息 {m.id} 已添加到数据库")
