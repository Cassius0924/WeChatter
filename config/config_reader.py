# 配置文件读取
import json
from configparser import ConfigParser
from typing import List


# 配置文件读取类
class ConfigReader:
    def __init__(self, config_file="config.ini"):
        self.config_file = config_file
        self.__cp = ConfigParser()
        self.__read_config()

    # 读取配置文件
    def __read_config(self):
        self.__cp.read(self.config_file, encoding="utf-8")

        # admin信息
        self.admin_list: List = json.loads(self.__cp.get("admin", "admin_list"))

        # bot信息
        self.bot_name: str = self.__cp.get("bot", "bot_name")

        # chat信息
        self.command_prefix: str = self.__cp.get("chat", "command_prefix")
        self.need_mentioned: bool = self.__cp.getboolean("chat", "need_mentioned")

        # server信息
        self.send_port: int = self.__cp.getint("server", "send_port")
        self.recv_port: int = self.__cp.getint("server", "recv_port")

    # TODO;封装get方法，判断不为空

