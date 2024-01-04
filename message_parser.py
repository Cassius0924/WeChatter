# 消息解析器
from command.command_set import cmd_dict
from command_invoker import CommandInvoker
from message import Message
from notifier import Notifier


# 消息解析器，用于解析用户发来的消息
class MessageParser:
    def __init__(self) -> None:
        pass

    def parse_message(self, message: Message, to_user_name: str) -> None:
        # 消息内容格式: /<cmd> <msg>
        msg = message.msg  # 消息内容
        # cmd = message.cmd # 命令
        desc = message.cmd_desc  # 命令描述
        cmd_value = message.cmd_value  # 命令值

        print(desc)
        # 非命令消息（消息不是以/开头）
        if cmd_value == 0:
            print("该消息不是命令类型")
            return

        # TODO: 判断是否引用消息，接着判断引用是否为“可引用的命令回复”消息

        # TODO: 判断是否为群消息，群消息需要@机器人，此限制可以在config里修改

        # 是命令消息
        # 回复消息已收到
        Notifier.notify_received(to_user_name)
        # 开始处理命令
        if cmd_value == self.__get_cmd_value("help"):
            CommandInvoker.cmd_help(to_user_name)

        elif cmd_value == self.__get_cmd_value("gpt4"):
            CommandInvoker.cmd_gpt4(msg, to_user_name)

        elif cmd_value == self.__get_cmd_value("gpt"):
            CommandInvoker.cmd_gpt35(msg, to_user_name)

        elif cmd_value == self.__get_cmd_value("bili-hot"):
            CommandInvoker.cmd_bili_hot(to_user_name)

        elif cmd_value == self.__get_cmd_value("zhihu-hot"):
            CommandInvoker.cmd_zhihu_hot(to_user_name)

        elif cmd_value == self.__get_cmd_value("weibo-hot"):
            CommandInvoker.cmd_weibo_hot(to_user_name)

        elif cmd_value == self.__get_cmd_value("word"):
            CommandInvoker.cmd_word(msg, to_user_name)

        elif cmd_value == self.__get_cmd_value("github-trending"):
            CommandInvoker.cmd_github_trending(to_user_name)

        elif cmd_value == self.__get_cmd_value("douyin-hot"):
            CommandInvoker.cmd_douyin_hot(to_user_name)

    # 获取命令值
    def __get_cmd_value(self, cmd: str) -> int:
        return cmd_dict[cmd]["value"]
