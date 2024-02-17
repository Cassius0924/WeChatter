# 消息类
import enum
import json
import re
from typing import Union

from loguru import logger
from pydantic import BaseModel, computed_field

import wechatter.config as config
from wechatter.models.wechat.group_info import GroupInfo
from wechatter.models.wechat.person_info import PersonInfo


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


class MessageSource(BaseModel):
    """
    消息来源类
    """

    p_info: PersonInfo
    g_info: Union[GroupInfo, None] = None

    def __str__(self) -> str:
        result = ""
        if self.g_info is not None:
            result += str(self.g_info)
        result += str(self.p_info)
        return result


class Message(BaseModel):
    """
    微信消息类（消息接收）
    :property content: 消息内容
    :property source: 消息来源
    :property is_mentioned: 是否@机器人
    :property is_quoted: 是否引用机器人消息
    :property is_group: 是否是群消息
    """

    type: MessageType
    content_: str
    source_: str
    is_mentioned_: str

    @computed_field
    @property
    def content(self) -> str:
        # 对于 iPad、手机端的微信，@名称后面会跟着一个未解码的空格的Unicode编码："@Cassius\u2005/help"
        return self.content_.replace("\u2005", " ", 1)

    @computed_field
    @property
    def source(self) -> MessageSource:
        try:
            source_json = json.loads(self.source_)
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
        p_info = PersonInfo(
            id=payload.get("id", ""),
            name=payload.get("name", ""),
            alias=payload.get("alias", ""),
            gender=g,
            signature=payload.get("signature", ""),
            province=payload.get("province", ""),
            city=payload.get("city", ""),
            phone_list=payload.get("phone", []),
            is_star=payload.get("star", ""),
            is_friend=payload.get("friend", ""),
        )
        message_source = MessageSource(p_info=p_info)

        # room为群信息，只有群消息才有room
        if source_json["room"] != "":
            g_data = source_json["room"]
            payload = g_data.get("payload", {})
            message_source.g_info = GroupInfo(
                id=g_data.get("id", ""),
                name=payload.get("topic", ""),
                admin_id_list=payload.get("adminIdList", []),
                member_list=payload.get("memberList", []),
            )
        return message_source

    @computed_field
    @property
    def is_mentioned(self) -> bool:
        """
        是否@机器人
        """

        if self.is_mentioned_ == "1":
            return True
        return False

    @computed_field
    @property
    def is_group(self) -> bool:
        """
        是否是群消息
        """
        return bool(self.source.g_info)

    @computed_field
    @property
    def is_quoted(self) -> bool:
        """
        是否引用机器人消息
        """
        # 判断是否为引用消息
        quote_pattern = (
            r"(?s)「(.*?)」\n- - - - - - - - - - - - - - -"  # 引用消息的正则
        )
        match_result = re.match(quote_pattern, self.content)
        # 判断是否为引用机器人消息
        if bool(match_result) and self.content.startswith(f"「{config.bot_name}"):
            return True
        return False

    def __str__(self) -> str:
        return f"消息内容：{self.content}\n消息来源：\n{self.source}\n是否@：{self.is_mentioned}\n是否引用：{self.is_quoted}"
