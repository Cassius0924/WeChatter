# 消息解析器
# from command_invoker import CommandInvoker
from main import cr
from message import Message
from notifier import Notifier
from send_msg import SendTo
# from command.command_set import cmd_dict


class MessageParser:
    """消息解析器，用于解析用户发来的消息"""

    def __init__(self) -> None:
        pass

    def parse_message(self, message: Message) -> None:
        """解析消息"""
        # 消息内容格式: /<cmd> <msg>
        msg = message.msg  # 消息内容
        # cmd = message.cmd # 命令
        desc = message.cmd_desc  # 命令描述
        # cmd_value = message.cmd_value  # 命令值
        cmd_func = message.cmd_func  # 命令函数

        print(desc)
        # 非命令消息
        if not message.is_cmd:
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

        # 调用命令
        if cmd_func is not None:
            cmd_func(to, msg)
        else:
            print("该命令未实现")
