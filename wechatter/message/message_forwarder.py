from typing import Dict, List

from loguru import logger

from wechatter.config.parsers import (
    parse_discord_message_forwarding_rule_list,
    parse_message_forwarding_rule_list,
    parse_official_account_reminder_rule_list,
)
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

    def __init__(self):
        self.all_message_rule = None
        self.specific_message_rules = None
        self.official_account_reminder_rule = None
        self.official_account_reminder_type = "text"
        self.discord_all_message_rule = None
        self.discord_message_forwarding_rule = None

    def set_wechat_forwarding_rule(self, message_forwarding_rule_list: List):
        """
        设置微信消息转发规则
        :param message_forwarding_rule_list: 消息转发规则列表
        """
        (
            self.all_message_rule,
            self.specific_message_rules,
        ) = parse_message_forwarding_rule_list(message_forwarding_rule_list)

    def set_official_account_reminder_rule(
        self, official_account_reminder_rule_list: List
    ):
        """
        设置公众号提醒规则
        :param official_account_reminder_rule_list: 公众号提醒规则列表
        """
        self.official_account_reminder_rule = parse_official_account_reminder_rule_list(
            official_account_reminder_rule_list
        )

    def set_discord_forwarding_rule(self, discord_message_forwarding_rule_list: List):
        """
        设置 Discord 消息转发规则
        :param discord_message_forwarding_rule_list: Discord 消息转发规则列表
        """
        (
            self.discord_all_message_rule,
            self.discord_specific_message_rules,
        ) = parse_discord_message_forwarding_rule_list(
            discord_message_forwarding_rule_list
        )

    def forwarding_to_wechat(self, message_obj: Message):
        """
        消息转发
        :param message_obj: 消息对象
        """
        # TODO: 转发文件

        # 判断是否设置了转发规则
        if not self.all_message_rule and not self.specific_message_rules:
            logger.warning(
                "消息转发器未设置转发规则，self.all_message_rule 和 self.specific_message_rules 均为空"
            )
            return

        # 判断消息来源是否符合转发规则
        if not self.all_message_rule["is_none"]:
            rule = self.all_message_rule
            _forwarding_by_rule(message_obj, rule)

        if message_obj.sender_name in self.specific_message_rules:
            rule = self.specific_message_rules[message_obj.sender_name]
            _forwarding_by_rule(message_obj, rule)

    @staticmethod
    def reply_wechat_forwarded_message(message_obj: Message):
        """
        回复转发消息
        :param message_obj: 消息对象
        """
        assert message_obj.forwarded_source_name
        name, is_group = message_obj.forwarded_source_name
        sender.send_msg(
            name,
            message_obj.pure_content,
            is_group=is_group,
        )
        logger.info(f"回复 {message_obj.forwarded_source_name} 的转发消息")

    def remind_official_account_article(self, message_obj: Message):
        """
        提醒公众号文章
        :param message_obj: 消息对象
        """
        if not message_obj.is_official_account:
            return
        # 判断是否设置了提醒规则
        if not self.official_account_reminder_rule:
            logger.warning(
                "消息转发器未设置公众号提醒规则，self.official_account_reminder_rule 为空"
            )
            return
        if message_obj.sender_name in self.official_account_reminder_rule:
            rule = self.official_account_reminder_rule[message_obj.sender_name]
            to_person_list = rule["to_person_list"]
            to_group_list = rule["to_group_list"]
            for recipient_list, is_group in [
                (to_person_list, False),
                (to_group_list, True),
            ]:
                if recipient_list:
                    if self.official_account_reminder_type == "text":
                        response = _construct_official_account_reminder_message(
                            message_obj
                        )
                        sender.mass_send_msg(
                            recipient_list, response, type="text", is_group=is_group
                        )
                    elif self.official_account_reminder_type == "image":
                        response = _construct_official_account_reminder_image(
                            message_obj
                        )
                        logger.info(
                            f"提醒公众号文章：{message_obj.sender_name} -> {recipient_list}"
                        )
                        sender.mass_send_msg(
                            recipient_list,
                            response,
                            type="localfile",
                            is_group=is_group,
                        )

    def forwarding_to_discord(self, message_obj: Message):
        """
        转发消息到 Discord
        :param message_obj: 消息对象
        """
        if (
            not self.discord_all_message_rule
            and not self.discord_specific_message_rules
        ):
            logger.warning(
                "消息转发器未设置 Discord 转发规则，self.discord_message_forwarding_rule 为空"
            )
            return

        if not self.discord_all_message_rule["is_none"]:
            rule = self.discord_all_message_rule
            webhook_url = rule["webhook_url"]
            sender.send_to_discord(
                webhook_url, message_obj.content, message_obj.person, message_obj.group
            )

        if message_obj.sender_name in self.discord_specific_message_rules:
            rule = self.discord_specific_message_rules[message_obj.sender_name]
            webhook_url = rule["webhook_url"]
            sender.send_to_discord(
                webhook_url, message_obj.content, message_obj.person, message_obj.group
            )


def _construct_official_account_reminder_message(message_obj: Message) -> str:
    """
    构造公众号文章提醒消息
    """
    result = (
        "✨===公众号文章提醒===✨\n"
        f"😃 公众号：{message_obj.sender_name}\n"
        f"📰 标题：{message_obj.urllink.title}\n"
    )
    return result


def _construct_official_account_reminder_image(message_obj: Message) -> str:
    """
    构造公众号文章提醒图片
    """
    # TODO: 构造公众号文章提醒图片
    # title = message_obj.urllink.title
    return "开发中..."
    pass


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
