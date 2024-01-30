# 配置文件读取
import json
import os
from configparser import ConfigParser
from typing import List

import wechatter.utils.path_manager as pm


class ConfigReader:
    """配置文件读取类"""

    def __init__(self, config_file: str):
        print("读取配置文件中...")
        self.config_file = pm.get_abs_path(config_file)
        if not self.is_config_exist:
            print("配置文件不存在，请先复制配置文件")
            exit(1)
        self.__cp = ConfigParser()
        self.__cp.read(self.config_file, encoding="utf-8")
        print("配置文件读取完成")

    def get(self, section: str, option: str) -> str:
        """获取配置文件中的值"""
        return self.__cp.get(section, option)

    def getboolean(self, section: str, option: str) -> bool:
        """获取配置文件中的值"""
        return self.__cp.getboolean(section, option)

    def getint(self, section: str, option: str) -> int:
        """获取配置文件中的值"""
        return self.__cp.getint(section, option)

    def getlist(self, section: str, option: str) -> List:
        """获取配置文件中的值"""
        return json.loads(self.__cp.get(section, option))

    # TODO;封装get方法，判断不为空

    @property
    def is_config_exist(self) -> bool:
        """检查配置文件是否存在"""
        return os.path.exists(self.config_file)
