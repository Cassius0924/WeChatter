# 消息解析器
import re
from typing import Dict

from loguru import logger

from wechatter.bot import BotInfo
from wechatter.config import config
from wechatter.database import QuotedResponse, make_db_session
from wechatter.models.wechat import Message, SendTo


class MessageHandler:
    """
    消息处理器，用于处理用户发来的消息
    """

    def __init__(self, commands: Dict, quoted_handlers: Dict):
        """
        :param commands: 命令处理函数字典
        :param quoted_handlers: 可引用的命令消息处理函数字典
        """
        self.commands = commands
        self.quoted_handlers = quoted_handlers

    def handle_message(self, message_obj: Message):
        """
        处理消息
        :param message_obj: 消息对象
        """
        to = SendTo(person=message_obj.person, group=message_obj.group)
        # 解析命令
        content = message_obj.content
        cmd_dict = self.__parse_command(
            content, message_obj.is_mentioned, message_obj.is_group
        )
        logger.info(cmd_dict["desc"])

        # 如果是，处理可引用的命令消息
        if message_obj.quotable_id:
            with make_db_session() as session:
                _quoted_response = (
                    session.query(QuotedResponse)
                    .filter_by(quotable_id=message_obj.quotable_id)
                    .order_by(QuotedResponse.id.desc())
                    .first()
                )
                quoted_response = _quoted_response.to_model()
            quoted_handler = self.quoted_handlers.get(quoted_response.command, None)
            if quoted_handler:
                quoted_handler(
                    to=to,
                    message=message_obj.pure_content,
                    q_response=quoted_response.response,
                )
            else:
                logger.warning(
                    f"未找到可引用的命令消息处理函数: {quoted_response.command}"
                )
            return

        # 非命令消息
        if cmd_dict["command"] == "None":
            logger.info("该消息不是命令类型")
            return

        # TODO: 可以为不同的群设置是否need_mentioned
        if (
            config["need_mentioned"]
            and message_obj.is_group
            and not message_obj.is_mentioned
        ):
            logger.debug("该消息为群消息，但未@机器人，不处理")
            return

        # 是命令消息
        # 开始处理命令
        cmd_handler = cmd_dict["handler"]
        if cmd_handler is not None:
            if cmd_dict["param_count"] == 2:
                cmd_handler(
                    to=to,
                    message=cmd_dict["arg"],
                )
            elif cmd_dict["param_count"] == 3:
                cmd_handler(
                    to=to,
                    message=cmd_dict["arg"],
                    message_obj=message_obj,
                )
        else:
            logger.error("该命令未实现")
        return

    def __parse_command(self, content: str, is_mentioned: bool, is_group: bool) -> Dict:
        """
        解析命令
        :param content: 消息内容
        :param is_mentioned: 是否@机器人
        :param is_group: 是否群消息
        """
        cmd_dict = {
            "command": "None",
            "desc": "",
            "arg": "",
            "handler": None,
            "param_count": 0,
        }
        # 不带命令前缀和@前缀的消息内容
        if is_mentioned and is_group:
            # 去掉"@机器人名"的前缀
            content = content.replace(f"@{BotInfo.name} ", "")
        for command, info in self.commands.items():
            # 第一个空格或回车前的内容即为指令
            cont_list = re.split(r"\s|\n", content, 1)
            if not cont_list[0].startswith(config["command_prefix"]):
                continue
            # 去掉命令前缀
            no_prefix = cont_list[0][len(config["command_prefix"]) :]
            if no_prefix.lower() in info["keys"]:
                cmd_dict["command"] = command
                cmd_dict["desc"] = info["desc"]
                cmd_dict["handler"] = info["handler"]
                cmd_dict["param_count"] = info["param_count"]
                if len(cont_list) == 2:
                    cmd_dict["arg"] = cont_list[1]  # 消息内容
                return cmd_dict
        return cmd_dict