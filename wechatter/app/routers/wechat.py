from typing import Union

from fastapi import APIRouter, Form, UploadFile
from loguru import logger

# from wechatter.bot import BotInfo
from wechatter.commands import commands, quoted_handlers
from wechatter.config import config
from wechatter.database import (
    Group as DbGroup,
    Message as DbMessage,
    Person as DbPerson,
    make_db_session,
)
from wechatter.games import games
from wechatter.message import MessageHandler
from wechatter.models.wechat import Message
from wechatter.models.wechat.group import Group
from wechatter.models.wechat.person import Person
from wechatter.sender import notifier

router = APIRouter()

# 传入命令字典，构造消息处理器
message_handler = MessageHandler(
    commands=commands, quoted_handlers=quoted_handlers, games=games
)


@router.post(config["wx_webhook_recv_api_path"])
async def recv_wechat_msg(
    type: str = Form(),
    content: Union[UploadFile, str] = Form(),
    source: str = Form(),
    is_mentioned: str = Form(alias="isMentioned"),
    is_from_self: str = Form(alias="isMsgFromSelf"),
):
    """
    用于接收 wxBotWebhook 转发过来的消息的接口
    """
    # 更新机器人信息（id和name）
    # BotInfo.update_from_source(source)

    # if type == "unknown":
    #     logger.info(f"收到未知消息：{content}")
    #     return

    # 判断是否是系统事件
    if type in ["system_event_login", "system_event_logout", "system_event_error"]:
        logger.info(f"收到系统事件：{type}")
        handle_system_event(type)
        return

    # 不是系统消息，则是用户发来的消息
    if type == "file":
        logger.info(f"收到文件：{content.filename}")
        return

    # 解析命令
    # 构造消息对象
    message_obj = Message.from_api_msg(
        type=type,
        content=content,
        source=source,
        is_mentioned=is_mentioned,
        is_from_self=is_from_self,
    )
    # 向群组表中添加该群组
    add_group(message_obj.group)
    # 向用户表中添加该用户
    add_person(message_obj.person)
    # 向消息表中添加该消息
    message_obj.id = add_message(message_obj)

    # DEBUG
    print(str(message_obj))

    # 用户发来的消息均送给消息解析器处理
    message_handler.handle_message(message_obj)

    # 快捷回复
    # return {"success": True, "data": {"type": "text", "content": "hello world！"}}


def handle_system_event(event: str) -> None:
    """
    判断系统事件类型，并调用相应的函数
    """
    # 判断是否为机器人登录消息
    if event == "system_event_login":
        notifier.notify_logged_in()
    elif event == "system_event_logout":
        notifier.notify_logged_out()
    elif event == "system_event_error":
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
                    logger.debug(f"用户 {member.name} 已添加到数据库")
                else:
                    # 更新用户信息
                    _person.name = member.name
                    _person.alias = member.alias
                    session.commit()

            session.commit()
            logger.debug(f"群组 {group.name} 已添加到数据库")
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
            logger.debug(f"用户 {person.name} 已添加到数据库")
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
        logger.debug(f"消息 {_message.id} 已添加到数据库")
        return _message.id
