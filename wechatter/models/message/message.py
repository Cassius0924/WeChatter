# 消息类
import enum
import json
import re
from typing import Union

from loguru import logger

import wechatter.config as config
from wechatter.models.message.group_info import GroupInfo
from wechatter.models.message.person_info import PersonInfo


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


class MessageSource:
    """
    消息来源类
    """

    def __init__(
        self,
        p_info: PersonInfo,
        g_info: Union[GroupInfo, None] = None,
    ):
        self.p_info = p_info
        self.g_info = g_info

    def __str__(self) -> str:
        result = ""
        if self.g_info is not None:
            result += str(self.g_info)
        result += str(self.p_info)
        return result


class Message:
    """
    消息类
    :property content: 消息内容
    :property source: 消息来源
    :property is_mentioned: 是否@机器人
    :property is_quoted: 是否引用机器人消息
    :property is_group: 是否是群消息
    """

    def __init__(
        self,
        type: str,
        content: str,
        source: str,
        is_mentioned: str = "0",
        command: dict = {},
    ):
        self.type = type
        self.content = content
        self.source: MessageSource = source
        self.is_mentioned = is_mentioned
        self.is_group = bool(self.source.g_info)
        self.is_quoted = content
        self.command = command

    # 获取消息类型
    @property
    def type(self) -> MessageType:
        return self.__type

    @type.setter
    def type(self, type: str):
        if type == "text":
            self.__type = MessageType.text
        elif type == "file":
            self.__type = MessageType.file
        elif type == "urlLink":
            self.__type = MessageType.urlLink
        else:
            raise ValueError("消息类型错误")

    @property
    def content(self) -> str:
        return self.__content

    @content.setter
    def content(self, content: str):
        # 对于 iPad、手机端的微信，@名称后面会跟着一个未解码的空格的Unicode编码："@Cassius\u2005/help"
        self.__content = content.replace("\u2005", " ", 1)

    @property
    def msg(self) -> str:
        return self.__msg

    @property
    def source(self) -> MessageSource:
        return self.__source

    @source.setter
    def source(self, source_json_str: str):
        if source_json_str == "":
            self.__source = MessageSource()
            return
        # 解析json
        source_json = dict()
        try:
            source_json = json.loads(source_json_str)
        except json.JSONDecodeError as e:
            logger.error("消息来源解析失败")
            raise e

        # from为发送者信息，无论是个人消息还是群消息，都有from
        payload = source_json.get("from").get("payload", {})
        if payload == {}:
            self.__source = MessageSource()
            return
        id = payload.get("id", "")
        name = payload.get("name", "")
        alias = payload.get("alias", "")
        gender = int(payload.get("gender", -1))
        signature = payload.get("signature", "")
        province = payload.get("province", "")
        city = payload.get("city", "")
        phone_list = payload.get("phone", [])
        is_star = payload.get("star", "")
        is_friend = payload.get("friend", "")

        if gender == 1:
            g = "male"
        elif gender == 0:
            g = "female"
        else:
            g = "unknown"
        message_source = MessageSource(
            p_info=PersonInfo(
                id=id,
                name=name,
                alias=alias,
                gender=g,
                signature=signature,
                province=province,
                city=city,
                phone_list=phone_list,
                is_star=is_star,
                is_friend=is_friend,
            )
        )

        # room为群信息，只有群消息才有room
        if source_json["room"] != "":
            g_data = source_json["room"]
            id = g_data["id"]
            payload = g_data.get("payload", {})
            name = payload.get("topic", "")
            admin_id_list = payload.get("adminIdList", [])
            member_list = payload.get("memberList", [])
            message_source.g_info = GroupInfo(
                id=id,
                name=name,
                admin_id_list=admin_id_list,
                member_list=member_list,
            )
        self.__source = message_source

    @property
    def is_mentioned(self) -> bool:
        """是否@机器人"""
        return self.__is_mentioned

    @is_mentioned.setter
    def is_mentioned(self, is_mentioned: str):
        if is_mentioned == "1":
            self.__is_mentioned = True
        else:
            self.__is_mentioned = False

    @property
    def is_group(self) -> bool:
        """是否是群消息"""
        return self.__is_group

    @is_group.setter
    def is_group(self, is_group: bool):
        self.__is_group = is_group

    @property
    def is_quoted(self) -> bool:
        """是否引用机器人消息"""
        return self.__is_quoted

    @is_quoted.setter
    def is_quoted(self, content: str):
        self.__is_quoted = False
        # 判断是否为引用消息
        quote_pattern = (
            r"(?s)「(.*?)」\n- - - - - - - - - - - - - - -"  # 引用消息的正则
        )
        match_result = re.match(quote_pattern, content)
        # 判断是否为引用机器人消息
        if bool(match_result) and content.startswith(f"「{config.bot_name}"):
            self.__is_quoted = True

    def __str__(self) -> str:
        return f"消息内容：{self.content}\n消息来源：\n{self.source}\n是否@：{self.is_mentioned}\n是否引用：{self.is_quoted}"
