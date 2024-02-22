from typing import Dict, List

from loguru import logger

from wechatter.models.wechat import (
    GROUP_FORWARDING_MESSAGE_FORMAT,
    PERSON_FORWARDING_MESSAGE_FORMAT,
    Message,
)
from wechatter.sender import sender


def _forwarding_by_rule(message_obj: Message, rule: Dict):
    """
    根据规则转发消息
    :param message_obj: 消息对象
    :param rule: 规则
    """
    to_person_list = rule.get("to_person_list")
    if to_person_list:
        msg = _construct_forwarding_message(message_obj)
        logger.info(f"转发消息：{message_obj.sender_name} -> {to_person_list}")
        sender.mass_send_msg(to_person_list, msg, is_group=False)
    to_group_list = rule.get("to_group_list")
    if to_group_list:
        msg = _construct_forwarding_message(message_obj)
        logger.info(f"转发消息：{message_obj.sender_name} -> {to_group_list}")
        sender.mass_send_msg(to_group_list, msg, is_group=True)


class MessageForwarder:
    """
    消息转发器类
    """

    def __init__(self, rule_list: List):
        """
        初始化
        :param rule_list: 转发规则列表
        """
        self.all_message_rules = []
        self.specific_message_rules = {}

        for rule in rule_list:
            if "%ALL" in rule["from_list"]:
                self.all_message_rules.append(rule)
            else:
                for from_name in rule["from_list"]:
                    if from_name not in self.specific_message_rules:
                        self.specific_message_rules[from_name] = []
                    self.specific_message_rules[from_name].append(rule)

    def forwarding(self, message_obj: Message):
        """
        消息转发
        :param message_obj: 消息对象
        """
        # TODO: 转发文件
        from_name = message_obj.sender_name

        # 判断消息来源是否符合转发规则
        if from_name in self.specific_message_rules:
            for rule in self.specific_message_rules[from_name]:
                _forwarding_by_rule(message_obj, rule)
        elif self.all_message_rules:
            for rule in self.all_message_rules:
                _forwarding_by_rule(message_obj, rule)

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
