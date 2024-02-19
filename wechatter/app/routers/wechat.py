import json
from typing import Union

from fastapi import APIRouter, Form, UploadFile
from loguru import logger

import wechatter.config as config
from wechatter.bot.bot_info import BotInfo
from wechatter.commands import commands
from wechatter.database import (
    Group as DbGroup,
    Message as DbMessage,
    Person as DbPerson,
    make_db_session,
)
from wechatter.message import MessageHandler
from wechatter.message_forwarder import MessageForwarder
from wechatter.models.wechat import Message
from wechatter.models.wechat.group import Group
from wechatter.models.wechat.person import Person
from wechatter.sender import notifier

router = APIRouter()


@router.post(config.wx_webhook_recv_api_path)
async def recv_wechat_msg(
    type: str = Form(),
    content: Union[UploadFile, str] = Form(),
    source: str = Form(),
    is_mentioned: str = Form(alias="isMentioned"),
    is_system_event: str = Form(alias="isSystemEvent"),
):
    """
    接收Docker转发过来的消息的接口
    """

    # 更新机器人信息（id和name）
    BotInfo.update_from_source(source)

    # 判断是否是系统事件
    if is_system_event == "1":
        logger.info(f"收到系统事件：{content}")
        handle_system_event(content)
        return

    # 不是系统消息，则是用户发来的消息
    if type == "file":
        logger.info(f"收到文件：{content.filename}")
        return

    # 解析命令
    # 构造消息对象
    message = Message.from_api_msg(
        type=type,
        content=content,
        source=source,
        is_mentioned=is_mentioned,
    )
    # 向群组表中添加该群组
    add_group(message.group)
    # 向用户表中添加该用户
    add_person(message.person)
    # 向消息表中添加该消息
    message.id = add_message(message)
    # TODO: 添加自己发送的消息，等待 wechatbot-webhook 支持

    # DEBUG
    print(str(message))

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


def add_group(group: Group) -> None:
    """
    判断群组表中是否有该群组，若没有，则添加该群组
    """
    if group is None:
        return
    with make_db_session() as session:
        _group = session.query(DbGroup).filter(DbGroup.id == group.id).first()
        if _group is None:
            _group = DbGroup.from_model(group)
            session.add(_group)
            # 逐个添加群组成员，若存在则更新
            for member in group.member_list:
                _person = (
                    session.query(DbPerson).filter(DbPerson.id == member.id).first()
                )
                if _person is None:
                    _person = DbPerson.from_member_model(member)
                    session.add(_person)
                    session.commit()
                    logger.info(f"用户 {member.name} 已添加到数据库")
                else:
                    # 更新用户信息
                    _person.name = member.name
                    _person.alias = member.alias
                    session.commit()

            session.commit()
            logger.info(f"群组 {group.name} 已添加到数据库")
        else:
            # 更新群组信息
            _group.update(group)
            session.commit()


def add_person(person: Person) -> None:
    """
    判断用户表中是否有该用户，若没有，则添加该用户
    """
    with make_db_session() as session:
        _person = session.query(DbPerson).filter(DbPerson.id == person.id).first()
        if _person is None:
            _person = DbPerson.from_model(person)
            session.add(_person)
            session.commit()
            logger.info(f"用户 {person.name} 已添加到数据库")
        else:
            # 更新用户信息
            _person.update(person)
            session.commit()


def add_message(message: Message) -> int:
    """
    添加消息到消息表
    """
    with make_db_session() as session:
        _message = DbMessage.from_model(message)
        session.add(_message)
        session.commit()
        logger.info(f"消息 {_message.id} 已添加到数据库")
        return _message.id
