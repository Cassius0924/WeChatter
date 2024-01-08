# 配置文件读取
import os
import json
from configparser import ConfigParser
from typing import List
from utils.path import get_abs_path


class ConfigReader:
    """配置文件读取类"""

    def __init__(self, config_file="config.ini"):
        print("读取配置文件中...")
        self.config_file = get_abs_path(config_file)
        if not self.is_config_exist:
            print("配置文件不存在，请先复制配置文件")
            exit(1)
        self.__cp = ConfigParser()
        self.__read_config()
        print("配置文件读取完成")

    @property
    def is_config_exist(self):
        """检查配置文件是否存在"""
        return os.path.exists(self.config_file)

    def __read_config(self):
        """读取配置文件"""
        self.__cp.read(self.config_file, encoding="utf-8")

        # admin信息
        self.admin_list: List = json.loads(self.__cp.get("admin", "admin_list"))
        self.admin_group_list: List = json.loads(
            self.__cp.get("admin", "admin_group_list")
        )

        # bot信息
        self.bot_name: str = self.__cp.get("bot", "bot_name")

        # chat信息
        self.command_prefix: str = self.__cp.get("chat", "command_prefix")
        self.need_mentioned: bool = self.__cp.getboolean("chat", "need_mentioned")

        # server信息
        self.send_port: int = self.__cp.getint("server", "send_port")
        self.recv_port: int = self.__cp.getint("server", "recv_port")
        self.recv_api_path: str = self.__cp.get("server", "recv_api_path")

    # TODO;封装get方法，判断不为空
