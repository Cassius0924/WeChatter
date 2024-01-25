# 消息解析器
import re

from main import cr
from wechatter.models.message import Message, SendTo
from wechatter.notifier import Notifier
from wechatter.bot.bot_info import BotInfo


class MessageHandler:
    """消息处理器，用于处理用户发来的消息"""

    def __init__(self, commands: dict):
        self.__commands = commands

    def handle_message(self, message: Message) -> None:
        """处理消息"""
        # 解析命令
        content = message.content  # 消息内容
        # 消息内容格式: /<cmd> <arg>
        cmd_dict = self.parse_command(content, message.is_mentioned, message.is_group)
        cmd_desc = cmd_dict["desc"]

        print(cmd_desc)

        # 非命令消息
        if cmd_dict["command"] == "None":
            print("该消息不是命令类型")
            return

        # TODO: 判断是否引用消息，接着判断引用是否为“可引用的命令回复”消息
        # if message.is_quote:
        #     pass

        # TODO: 可以为不同的群设置是否need_mentioned
        if cr.need_mentioned and message.is_group and not message.is_mentioned:
            print("该消息为群消息，但未@机器人，不处理")
            return

        to = SendTo(message.source)

        # 是命令消息
        # 回复消息已收到
        Notifier.notify_received(to)

        # 开始处理命令
        cmd_handler = cmd_dict["handler"]
        if cmd_handler is not None:
            cmd_handler(to, cmd_dict["arg"])
        else:
            print("该命令未实现")
        return

    def parse_command(self, content: str, is_mentioned: bool, is_group: bool) -> dict:
        """解析命令"""
        cmd_dict = {
            "command": "None",
            "desc": "",
            "value": 0,
            "arg": "",
            "handler": None,
        }
        # 不带命令前缀和@前缀的消息内容
        if is_mentioned and is_group:
            # 去掉"@机器人名"的前缀
            content = content.replace(f"@{BotInfo.name} ", "")
        for command, info in self.__commands.items():
            # 第一个空格或回车前的内容即为指令
            cont_list = re.split(r"\s|\n", content, 1)
            # 去掉命令前缀
            no_prefix = cont_list[0].replace(
                cr.command_prefix, "", len(cr.command_prefix)
            )
            if no_prefix.lower() in info["keys"]:
                cmd_dict["command"] = command
                cmd_dict["desc"] = info["desc"]
                cmd_dict["value"] = info["value"]
                cmd_dict["handler"] = info["handler"]
                if len(cont_list) == 2:
                    cmd_dict["arg"] = cont_list[1]  # 消息内容
                return cmd_dict
        return cmd_dict
