from typing import Dict, List

from loguru import logger

from wechatter.config.parsers import parse_message_forwarding_rule_list
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
    # 应用 exclude 规则
    # 开始转发消息
    to_person_list = rule["to_person_list"]
    if message_obj.sender_name in rule.get("from_list_exclude", []):
        return
    if to_person_list:
        msg = _construct_forwarding_message(message_obj)
        sender.mass_send_msg(to_person_list, msg, is_group=False)
        logger.info(f"转发消息：{message_obj.sender_name} -> {to_person_list}")
    to_group_list = rule["to_group_list"]
    if to_group_list:
        msg = _construct_forwarding_message(message_obj)
        sender.mass_send_msg(to_group_list, msg, is_group=True)
        logger.info(f"转发消息：{message_obj.sender_name} -> {to_group_list}")


class MessageForwarder:
    """
    消息转发器类
    """

    def __init__(self, rule_list: List):
        """
        初始化
        :param rule_list: 转发规则列表
        """
        (
            self.all_message_rule,
            self.specific_message_rules,
        ) = parse_message_forwarding_rule_list(rule_list)

    def forwarding(self, message_obj: Message):
        """
        消息转发
        :param message_obj: 消息对象
        """
        # TODO: 转发文件

        # 判断消息来源是否符合转发规则
        if self.all_message_rule:
            rule = self.all_message_rule
            _forwarding_by_rule(message_obj, rule)

        if message_obj.sender_name in self.specific_message_rules.keys():
            rule = self.specific_message_rules[message_obj.sender_name]
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
