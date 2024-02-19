import enum
import json
import re
from functools import cached_property
from typing import Optional

from loguru import logger
from pydantic import BaseModel, computed_field

import wechatter.config as config
from wechatter.models.wechat.group import Group
from wechatter.models.wechat.person import Person
from wechatter.models.wechat.quoted_response import QUOTABLE_FORMAT


class MessageType(enum.Enum):
    """
    消息类型枚举类
    """

    text = "text"
    file = "file"
    urlLink = "urlLink"
    friendship = "friendship"


class MessageSenderType(enum.Enum):
    """
    消息来源枚举
    """

    PERSON = 0
    GROUP = 1
    # TODO: 公众号文章
    # ARTICLE = 2


class Message(BaseModel):
    """
    微信消息类（消息接收）
    """

    type: MessageType
    person: Person
    group: Optional[Group] = None
    content: str
    is_mentioned: bool = False
    id: Optional[int] = None

    @classmethod
    def from_api_msg(
        cls,
        type: MessageType,
        content: str,
        source: str,
        is_mentioned: str,
    ):
        """
        从API接口创建消息对象
        """
        try:
            source_json = json.loads(source)
        except json.JSONDecodeError as e:
            logger.error("消息来源解析失败")
            raise e

        # from为发送者信息，无论是个人消息还是群消息，都有from
        payload = source_json.get("from").get("payload", {})
        gender = int(payload.get("gender", -1))
        g = "unknown"
        if gender == 1:
            g = "male"
        elif gender == 0:
            g = "female"
        _person = Person(
            id=payload.get("id", ""),
            name=payload.get("name", ""),
            alias=payload.get("alias", ""),
            gender=g,
            signature=payload.get("signature", ""),
            province=payload.get("province", ""),
            city=payload.get("city", ""),
            # phone_list=payload.get("phone", []),
            is_star=payload.get("star", ""),
            is_friend=payload.get("friend", ""),
        )

        _group = None
        # room为群信息，只有群消息才有room
        if source_json["room"] != "":
            g_data = source_json["room"]
            payload = g_data.get("payload", {})
            _group = Group(
                id=g_data.get("id", ""),
                name=payload.get("topic", ""),
                admin_id_list=payload.get("adminIdList", []),
                member_list=payload.get("memberList", []),
            )
        _content = content.replace("\u2005", " ", 1)
        _is_mentioned = False
        if is_mentioned == "1":
            _is_mentioned = True
        return cls(
            type=type,
            person=_person,
            group=_group,
            content=_content,
            is_mentioned=is_mentioned,
        )

    @computed_field
    @property
    def is_group(self) -> bool:
        """
        是否是群消息
        """
        return self.group is not None

    @computed_field
    @cached_property
    def is_quoted(self) -> bool:
        """
        是否引用机器人消息
        """
        # 引用消息的正则
        quote_pattern = r"(?s)「(.*?)」\n- - - - - - - - - - - - - - -"
        match_result = re.match(quote_pattern, self.content)
        # 判断是否为引用机器人消息
        if match_result and self.content.startswith(f"「{config.bot_name}"):
            return True
        return False

    # TODO: 判断所有的引用消息，不仅仅是机器人消息
    #  待解决：在群中如果有人设置了自己的群中名称，那么引用内容的名字会变化，导致无法匹配到用户

    @computed_field
    @property
    def sender_name(self) -> str:
        """
        返回消息发送对象名，如果是群则返回群名，如果不是则返回人名
        """
        return self.group.name if self.is_group else self.person.name

    @computed_field
    @cached_property
    def quotable_id(self) -> Optional[str]:
        """
        获取引用消息的id
        """
        if self.is_quoted:
            pattern = rf'「.+{QUOTABLE_FORMAT % "(.{3})"}'
            try:
                return re.search(pattern, self.content).group(1)
            except AttributeError:
                return None
        return None

    @computed_field
    @cached_property
    def pure_content(self) -> str:
        """
        获取不带引用的消息内容，即用户真实发送的消息
        """
        if self.is_quoted:
            pattern = "「[\s\S]+」\n- - - - - - - - - - - - - - -\n([\s\S]*)"
            return re.search(pattern, self.content).group(1)
        else:
            return self.content

    def __str__(self) -> str:
        source = self.person
        if self.is_group:
            source = self.group
        return (
            f"消息内容：{self.content}\n"
            f"消息来源：{source}\n"
            f"是否@：{self.is_mentioned}\n"
            f"是否引用：{self.is_quoted}"
        )
