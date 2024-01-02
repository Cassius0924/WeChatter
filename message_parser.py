from typing import Tuple
from admin import send_msg_to_all_admin
from command_invoker import CommandInvoker
from notifier import Notifier
from command.command_set import cmd_dict
from event_parser import EventParser


# 消息解析器，用于解析用户发来的消息
class MessageParser:
    def __init__(self) -> None:
        pass

    def parse_message(self, message: str, to_user_name: str) -> None:
        message, desc_and_cmd = self.__parse_command(message)
        desc, cmd = desc_and_cmd["desc"], desc_and_cmd["value"]
        print(desc)

        # 非命令消息（消息不是以/开头）
        if cmd == 0:
            print("该消息不是命令类型")
            return

        # 是命令消息
        # 回复消息已收到
        Notifier.notify_received(to_user_name)
        # 开始处理命令
        if cmd == self.__get_cmd_value("help"):
            CommandInvoker.cmd_help(to_user_name)

        elif cmd == self.__get_cmd_value("gpt4"):
            CommandInvoker.cmd_gpt4(message, to_user_name)

        elif cmd == self.__get_cmd_value("gpt"):
            CommandInvoker.cmd_gpt35(message, to_user_name)

        elif cmd == self.__get_cmd_value("bili-hot"):
            CommandInvoker.cmd_bili_hot(to_user_name)

        elif cmd == self.__get_cmd_value("zhihu-hot"):
            CommandInvoker.cmd_zhihu_hot(to_user_name)

        elif cmd == self.__get_cmd_value("weibo-hot"):
            CommandInvoker.cmd_weibo_hot(to_user_name)


    # 解析消息，判断是否为命令消息
    def __parse_command(self, message: str) -> Tuple[str, dict]:
        for value in cmd_dict.values():
            for key in value["keys"]:
                if message.startswith("/" + key):
                    message = message[len(key) + 1 :]
                    return message, {"desc": value["desc"], "value": value["value"]}
        return message, {
            "desc": cmd_dict["None"]["desc"],
            "value": cmd_dict["None"]["value"],
        }


    # 获取命令值
    def __get_cmd_value(self, cmd: str) -> int:
        return cmd_dict[cmd]["value"]






