from typing import List

from loguru import logger

from wechatter.models.message import Message
from wechatter.sender import sender


class MessageForwarder:
    """消息转发器类"""

    def __init__(self, rule_list: List):
        self.rule_list = rule_list

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
        for rule in self.rule_list:
            # 判断是否有["froms"]字段,即是否是接收所有消息转发给指定人或群
            if "froms" not in rule:
                # 构造转发消息
                msg = self.__construct_forwarding_message(message)
                logger.info(
                    f"转发消息：{from_name} -> {rule['to_persons']}\n"
                    f"转发消息：{from_name} -> {rule['to_groups']}"
                )
                sender.mass_send_msg(rule["to_persons"], msg)
                sender.mass_send_msg(rule["to_groups"], msg, is_group=True)
            # 自定义转发规则
            if from_name in rule["froms"]:
                # 构造转发消息
                msg = self.__construct_forwarding_message(message)
                logger.info(
                    f"转发消息：{from_name} -> {rule['to_persons']}\n"
                    f"转发消息：{from_name} -> {rule['to_groups']}"
                )
                sender.mass_send_msg(rule["to_persons"], msg)
                sender.mass_send_msg(rule["to_groups"], msg, is_group=True)

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
