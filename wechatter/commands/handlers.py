import inspect
from typing import List

from loguru import logger

from wechatter.config import config

commands = {}
"""
存储所有命令的信息及其处理函数的字典
"""
quoted_handlers = {}
"""
存储所有可引用的命令消息的处理函数的字典
"""


# 改为类装饰器
class command:
    def __init__(self, command: str, keys: List[str], desc: str):
        """
        注册命令
        :param command: 命令
        :param keys: 命令关键词列表
        :param desc: 命令描述
        """
        # TODO: 检测command是否重复
        self.command = command
        self.keys = keys
        self.desc = desc

    def __call__(self, func):
        sig = inspect.signature(func)
        params = sig.parameters
        if len(params) < 2:
            error_message = f"缺少命令处理函数参数，命令处理函数至少需要 to 和 message 参数：{func.__name__}"
            logger.error(error_message)
            raise ValueError(error_message)
        if "to" not in params:
            error_message = (
                f"参数名错误，命令处理函数的第1个参数必须为 to：{func.__name__}"
            )
            logger.error(error_message)
            raise ValueError(error_message)
        if "message" not in params:
            error_message = (
                f"参数名错误，命令处理函数的第2个参数必须为 message：{func.__name__}"
            )
            logger.error(error_message)
            raise ValueError(error_message)
        if len(params) == 3 and "message_obj" not in params:
            error_message = (
                f"参数名错误，命令处理函数的第3个参数必须为 message_obj{func.__name__}"
            )
            logger.error(error_message)
            raise ValueError(error_message)
        if len(params) > 3:
            error_message = f"参数数量错误，命令处理函数参数数量不能超过3个（to, message, message_obj）{func.__name__}"
            logger.error(error_message)
            raise ValueError(error_message)

        commands[self.command] = {}
        # 自定义命令关键词
        if config["custom_command_key_dict"].get(self.command, None):
            self.keys.extend(config["custom_command_key_dict"][self.command])

        commands[self.command]["keys"] = self.keys
        commands[self.command]["desc"] = self.desc
        commands[self.command]["handler"] = func
        commands[self.command]["param_count"] = len(params)
        commands[self.command]["is_quotable"] = False

        return self

    def quoted_handler(self, func):
        """
        设置命令的引用消息处理函数
        :param func: 命令的引用消息处理函数
        """
        # TODO: 判断参数是否合理
        commands[self.command]["is_quotable"] = True
        quoted_handlers[self.command] = func
        return func

    def mainfunc(self, func):
        """
        设置命令的主函数，这个函数一般是返回命令的结果和命令的引用消息
        :param func: 命令的主函数
        """
        commands[self.command]["mainfunc"] = func
        return func
