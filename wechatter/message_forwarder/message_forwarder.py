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

        name = f"{from_name}"

        print(from_name)
        # TODO: 转发文件
        # 判断消息是否符合转发规则
        for rule in self.rule_list:
            print(rule)
            # 如果发送列表里有*，就代表发送者为所有人，如果发送者名字没有在列表，就加上
            if "*" in rule["froms"] and name not in rule["froms"]:
                rule["froms"] += [name]
            print(rule)
            # # 除去在接收者列表中发送的消息
            # if from_name in rule["to_persons"]:
            #     continue
            # # 除去在群里接收者发送的消息
            # if message.is_group and message.source.p_info.name in rule["to_persons"]:
            #     continue
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
