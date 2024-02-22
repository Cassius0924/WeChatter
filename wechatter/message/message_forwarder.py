from typing import List

from loguru import logger

from wechatter.models.wechat import (
    GROUP_FORWARDING_MESSAGE_FORMAT,
    PERSON_FORWARDING_MESSAGE_FORMAT,
    Message,
)
from wechatter.sender import sender


class MessageForwarder:
    """
    消息转发器类
    """

    def __init__(self, rule_list: List):
        self.rule_list = rule_list

    def forward_message(self, message_obj: Message):
        """
        消息转发
        :param message_obj: 消息对象
        """
        # TODO: 转发文件
        from_name = message_obj.sender_name

        # TODO: from_list 支持通配符

        # 判断消息是否符合转发规则
        for rule in self.rule_list:
            # 判断消息来源是否符合转发规则
            if from_name in rule["from_list"]:
                # 构造转发消息
                msg = _construct_forwarding_message(message_obj)
                to_person_list = rule.get("to_person_list")
                if to_person_list:
                    logger.info(f"转发消息：{from_name} -> {to_person_list}")
                    sender.mass_send_msg(to_person_list, msg, is_group=False)
                to_group_list = rule.get("to_group_list")
                if to_group_list:
                    logger.info(f"转发消息：{from_name} -> {to_group_list}")
                    sender.mass_send_msg(to_group_list, msg, is_group=True)

    @staticmethod
    def reply_forwarded_message(message_obj: Message):
        """
        回复转发消息
        :param message_obj: 消息对象
        """
        assert message_obj.forwarded_source
        name, is_group = message_obj.forwarded_source
        sender.send_msg(
            name,
            message_obj.pure_content,
            is_group=is_group,
        )
        logger.info(f"回复 {message_obj.forwarded_source} 的转发消息")


def _construct_forwarding_message(message_obj: Message) -> str:
    """
    构造转发消息
    """

    content = message_obj.content
    if message_obj.is_group:
        content = (
            GROUP_FORWARDING_MESSAGE_FORMAT
            % (
                message_obj.person.name,
                message_obj.group.name,
            )
            + content
        )
    else:
        content = PERSON_FORWARDING_MESSAGE_FORMAT % message_obj.person.name + content
    return content
