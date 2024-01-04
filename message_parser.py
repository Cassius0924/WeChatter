# 消息解析器
from typing import Tuple
from command_invoker import CommandInvoker
from notifier import Notifier
from command.command_set import cmd_dict
from message import Message


# 消息解析器，用于解析用户发来的消息
class MessageParser:
    def __init__(self) -> None:
        pass

    def parse_message(self, message: Message, to_user_name: str) -> None:
        content = message.content
        cont, desc_and_cmd = self.__parse_command(content)
        desc, cmd = desc_and_cmd["desc"], desc_and_cmd["value"]
        print(desc)

        # 非命令消息（消息不是以/开头）
        if cmd == 0:
            print("该消息不是命令类型")
            return

        # TODO: 判断是否引用消息，接着判断引用是否为“可引用的命令回复”消息

        # TODO: 判断是否为群消息，群消息需要@机器人，此限制可以在config里修改

        # 是命令消息
        # 回复消息已收到
        Notifier.notify_received(to_user_name)
        # 开始处理命令
        if cmd == self.__get_cmd_value("help"):
            CommandInvoker.cmd_help(to_user_name)

        elif cmd == self.__get_cmd_value("gpt4"):
            CommandInvoker.cmd_gpt4(cont, to_user_name)

        elif cmd == self.__get_cmd_value("gpt"):
            CommandInvoker.cmd_gpt35(cont, to_user_name)

        elif cmd == self.__get_cmd_value("bili-hot"):
            CommandInvoker.cmd_bili_hot(to_user_name)

        elif cmd == self.__get_cmd_value("zhihu-hot"):
            CommandInvoker.cmd_zhihu_hot(to_user_name)

        elif cmd == self.__get_cmd_value("weibo-hot"):
            CommandInvoker.cmd_weibo_hot(to_user_name)

        elif cmd == self.__get_cmd_value("word"):
            CommandInvoker.cmd_word(cont, to_user_name)

    # 解析消息，判断是否为命令消息
    def __parse_command(self, content: str) -> Tuple[str, dict]:
        for value in cmd_dict.values():
            for key in value["keys"]:
                # 无参数指令：
                if content == "/" + key:
                    return "", {"desc": value["desc"], "value": value["value"]}
                # 带参数指令：
                # 命令以/开头，和消息之间用空格隔开
                if content.startswith("/" + key + " "):
                    cont = content[len(key) + 2 :]
                    return cont, {"desc": value["desc"], "value": value["value"]}
        return "", {
            "desc": cmd_dict["None"]["desc"],
            "value": cmd_dict["None"]["value"],
        }

    # 获取命令值
    def __get_cmd_value(self, cmd: str) -> int:
        return cmd_dict[cmd]["value"]

    # 判断是否为@消息
    def __is_mentioned(self, message: str) -> bool:
        return False

    # 判断是否为引用消息
