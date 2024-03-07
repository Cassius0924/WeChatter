import enum
import json
import re
from functools import cached_property
from typing import Optional, Tuple

from loguru import logger
from pydantic import BaseModel, computed_field

from wechatter.bot import BotInfo
from wechatter.models.wechat.group import Group
from wechatter.models.wechat.person import Person
from wechatter.models.wechat.quoted_response import QUOTABLE_FORMAT
from wechatter.models.wechat.url_link import UrlLink

PERSON_FORWARDING_MESSAGE_FORMAT = "⤴️ [%s] 说：\n" "-------------------------\n"
GROUP_FORWARDING_MESSAGE_FORMAT = "⤴️ [%s] 在 [%s] 说：\n" "-------------------------\n"


class MessageType(enum.Enum):
    """
    消息类型枚举类
    """

    text = "text"
    file = "file"
    urlLink = "urlLink"
    friendship = "friendship"
    system_event_login = "system_event_login"
    system_event_logout = "system_event_logout"
    system_event_error = "system_event_error"
    system_event_push_notify = "system_event_push_notify"
    unknown = "unknown"


class MessageSenderType(enum.Enum):
    """
    消息来源枚举
    """

    PERSON = 0
    GROUP = 1


class Message(BaseModel):
    """
    微信消息类（消息接收）
    """

    type: MessageType
    person: Person
    group: Optional[Group] = None
    receiver: Optional[Person] = None
    content: str
    is_mentioned: bool = False
    is_from_self: bool = False
    id: Optional[int] = None

    @classmethod
    def from_api_msg(
        cls,
        type: MessageType,
        content: str,
        source: str,
        is_mentioned: str,
        is_from_self: str = 0,
    ):
        """
        从API接口创建消息对象
        :param type: 消息类型
        :param content: 消息内容
        :param source: 消息来源
        :param is_mentioned: 是否@机器人
        :param is_from_self: 是否是自己发送的消息
        :return: 消息对象
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
        # 判断 id 长度：个人用户为65位，公众号为33位（包括@符号）
        name = payload.get("name", "")
        # 暂时通过名字判断是否为央视新闻公众号
        is_official_account = len(payload.get("id", "")) == 33
        if name == "央视新闻":
            is_official_account = True
        _person = Person(
            id=payload.get("id", ""),
            name=name,
            alias=payload.get("alias", ""),
            gender=g,
            signature=payload.get("signature", ""),
            province=payload.get("province", ""),
            city=payload.get("city", ""),
            # phone_list=payload.get("phone", []),
            is_star=payload.get("star", False),
            is_friend=payload.get("friend", False),
            is_official_account=is_official_account,
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

        _receiver = None
        if source_json.get("to"):
            to_payload = source_json.get("to").get("payload", {})
            _receiver = Person(
                id=to_payload.get("id", ""),
                name=to_payload.get("name", ""),
                alias=to_payload.get("alias", ""),
                gender="unknown",
                is_star=to_payload.get("star", False),
                is_friend=to_payload.get("friend", False),
            )

        _content = content.replace("\u2005", " ", 1)
        _is_mentioned = False
        if is_mentioned == "1":
            _is_mentioned = True
        _is_from_self = False
        if is_from_self == "1":
            _is_from_self = True
        return cls(
            type=type,
            person=_person,
            group=_group,
            receiver=_receiver,
            content=_content,
            is_mentioned=_is_mentioned,
            is_from_self=_is_from_self,
        )

    @computed_field
    @property
    def is_group(self) -> bool:
        """
        是否是群消息
        :return: 是否是群消息
        """
        return self.group is not None

    @computed_field
    @cached_property
    def is_quoted(self) -> bool:
        """
        是否引用机器人消息
        :return: 是否引用机器人消息
        """
        # 引用消息的正则
        quote_pattern = r"(?s)「(.*?)」\n- - - - - - - - - - - - - - -"
        match_result = re.match(quote_pattern, self.content)
        # 判断是否为引用机器人消息
        if match_result and self.content.startswith(f"「{BotInfo.name}"):
            return True
        return False

    # TODO: 判断所有的引用消息，不仅仅是机器人消息
    #  待解决：在群中如果有人设置了自己的群中名称，那么引用内容的名字会变化，导致无法匹配到用户

    @computed_field
    @property
    def sender_name(self) -> str:
        """
        返回消息发送对象名，如果是群则返回群名，如果不是则返回人名
        :return: 消息发送对象名
        """
        return self.group.name if self.is_group else self.person.name

    @computed_field
    @cached_property
    def quotable_id(self) -> Optional[str]:
        """
        获取引用消息的id
        :return: 引用消息的id
        """
        if self.is_quoted:
            pattern = f'^「[^「]+{QUOTABLE_FORMAT % "(.{3})"}'
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
        :return: 不带引用的消息内容
        """
        if self.is_quoted:
            pattern = "「[\s\S]+」\n- - - - - - - - - - - - - - -\n([\s\S]*)"
            return re.search(pattern, self.content).group(1)
        else:
            return self.content

    @computed_field
    @cached_property
    def forwarded_source_name(self) -> Optional[Tuple[str, bool]]:
        """
        获取转发消息的来源的名字
        :return: 消息来源的名字和是否为群的元组(source_name, is_group)
        """
        if self.is_quoted:
            # 先尝试匹配群消息
            group_format = GROUP_FORWARDING_MESSAGE_FORMAT.replace("[", "\[").replace(
                "]", "\]"
            )
            pattern = re.compile(f'{group_format % ("(.*)", "(.+)")}')
            try:
                # 将名字和该名字是否为群都返回，便于在回复时判断
                return re.search(pattern, self.content).group(2), True
            except AttributeError:
                pass
            # 再尝试匹配个人消息
            person_format = PERSON_FORWARDING_MESSAGE_FORMAT.replace("[", "\[").replace(
                "]", "\]"
            )
            pattern = re.compile(f'{person_format % "(.+)"}')
            try:
                return re.search(pattern, self.content).group(1), False
            except AttributeError:
                return None
        else:
            return None

    @computed_field
    @cached_property
    def is_official_account(self) -> bool:
        """
        是否是公众号消息
        :return: 是否是公众号消息
        """
        return self.person.is_official_account

    @computed_field
    @cached_property
    def urllink(self) -> Optional[UrlLink]:
        """
        当消息类型为urlLink时，返回url link的解析结果
        """
        if self.type == MessageType.urlLink:
            url_link_json = json.loads(self.content)
            return UrlLink(
                title=url_link_json.get("title"),
                desc=url_link_json.get("description"),
                url=url_link_json.get("url"),
                cover_url=url_link_json.get("thumbnailUrl"),
            )
        return None

    @computed_field
    @cached_property
    def is_tickled(self) -> bool:
        """
        是否为拍一拍消息
        """
        # 消息类型为 unknown 且 content 为 "某人" 拍了拍我
        return self.type == MessageType.unknown and "拍了拍我" in self.content

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
