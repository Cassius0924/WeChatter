from typing import List
from wechatter.models.message import Message, SendMessage, SendMessageType
from wechatter.sender import Sender


class MessageForwarder:
    """消息转发器类"""

    def __init__(self, rules: List):
        self.rules = rules

    def forward_message(self, message: Message):
        """消息转发"""

        # 判断消息来源
        from_name = ""
        if message.is_group:
            from_name = message.source.g_info.name
        else:
            from_name = message.source.p_info.name

        # TODO: 转发文件

        # 判断消息是否符合转发规则
        for rule in self.rules:
            # 判断消息来源是否符合转发规则
            if from_name in rule["froms"]:
                # 构造转发消息
                msg = self.__construct_forwarding_message(message)
                for p_name in rule["to_persons"]:
                    Sender.send_msg_p(p_name, SendMessage(SendMessageType.TEXT, msg))
                for g_name in rule["to_groups"]:
                    Sender.send_msg_g(g_name, SendMessage(SendMessageType.TEXT, msg))

    def __construct_forwarding_message(self, message: Message) -> str:
        """构造转发消息"""
        content = message.content
        if message.is_group:
            content = (
                f"⤴️ {message.source.p_info.name}在{message.source.g_info.name}中说：\n"
                f"-------------------------\n"
                f"{content}"
            )
        else:
            content = (
                f"⤴️ {message.source.p_info.name}说：\n"
                f"-------------------------\n"
                f"{content}"
            )
        return content
