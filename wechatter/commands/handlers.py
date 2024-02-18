import inspect
from typing import List

from loguru import logger

import wechatter.config as config

commands = {}
"""
存储所有命令消息和其信息的及其处理函数的字典。
"""


def command(command: str, keys: List[str], desc: str):
    """
    注册命令
    :param command: 命令
    :param keys: 命令关键词列表
    :param desc: 命令描述
    :return: 装饰器
    """

    def decorator(func):
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

        commands[command] = {}
        # 自定义命令关键词
        if config.custom_command_key_dict.get(command, None):
            keys.extend(config.custom_command_key_dict[command])

        commands[command]["keys"] = keys
        commands[command]["desc"] = desc
        commands[command]["handler"] = func
        commands[command]["param_count"] = len(params)

        return func

    return decorator
