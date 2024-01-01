from typing import Tuple
from command_invoker import CommandInvoker
from send_msg import acknowledge
from command.command_set import cmd_dict
from event_parser import EventParser


class MessageParser:
    def __init__(self) -> None:
        pass

    def parse_message(self, message: str, to_user_name: str) -> None:
        message, desc_and_cmd = self.__parse_command(message)
        desc, cmd = desc_and_cmd["desc"], desc_and_cmd["value"]
        print(desc)
        # 非命令消息
        if cmd == 0:
            print("该消息不是命令类型")
            return

        # 判断是否为登录消息
        if (EventParser.parse_login(message)):
            print("机器人登录成功")
            return

        # 是命令消息
        acknowledge(to_user_name)  # 回复消息已收到

        if cmd == self.__get_cmd_value("help"):
            CommandInvoker.cmd_help(to_user_name)

        elif cmd == self.__get_cmd_value("gpt4"):
            CommandInvoker.cmd_gpt4(message, to_user_name)

        elif cmd == self.__get_cmd_value("gpt"):
            CommandInvoker.cmd_gpt35(message, to_user_name)

        elif cmd == self.__get_cmd_value("bili-hot"):
            CommandInvoker.cmd_bili_hot(to_user_name)

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

    def __get_cmd_value(self, cmd: str) -> int:
        return cmd_dict[cmd]["value"]

