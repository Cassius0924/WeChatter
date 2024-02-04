from typing import List

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
        commands[command] = {}
        # 自定义命令关键词
        if config.custom_command_key_dict.get(command, None):
            keys.extend(config.custom_command_key_dict[command])

        commands[command]["keys"] = keys
        commands[command]["desc"] = desc
        commands[command]["handler"] = func

        return func

    return decorator
