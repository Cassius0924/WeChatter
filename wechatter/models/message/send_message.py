from enum import Enum
from typing import List

from wechatter.models.message.message import MessageSource


class SendTo:
    """发送对象类"""

    def __init__(self, source: MessageSource):
        self.p_id = ""
        self.p_name = ""
        self.g_id = ""
        self.g_name = ""
        if source.p_info is not None:
            self.p_id = source.p_info.id
            self.p_name = source.p_info.name
        if source.g_info is not None:
            self.g_id = source.g_info.id
            self.g_name = source.g_info.name


class SendMessageType(Enum):
    """发送消息类型枚举"""

    TEXT = "text"
    FILE_URL = "fileUrl"


class SendMessage:
    """发送消息类"""

    def __init__(self, type: SendMessageType, content: str):
        self.type = type.value
        self.content = content


class SendMessageList:
    """发送消息列表类，用于给同一个对象发送多条消息"""

    def __init__(self):
        self.messages: List[SendMessage] = []

    def add(self, message: SendMessage):
        self.messages.append(message)
