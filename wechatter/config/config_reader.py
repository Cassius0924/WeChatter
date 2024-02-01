# 配置文件读取
import json
import os
from configparser import ConfigParser
from typing import List

from loguru import logger

import wechatter.utils.path_manager as pm


class ConfigReader:
    """配置文件读取类"""

    def __init__(self, config_file: str):
        self.config_file = pm.get_abs_path(config_file)
        if not os.path.exists(self.config_file):
            logger.critical(
                "config.ini 配置文件不存在，请先复制 config.ini.example 配置文件模板！"
            )
            exit(1)
        self.__cp = ConfigParser()
        self.__cp.read(self.config_file, encoding="utf-8")
        self.config_list = self.__cp.sections()

    def getstr(self, section: str, option: str) -> str:
        """
        以字符串的形式获取配置文件中的值
        :param section: 配置文件中的section
        :param option: 配置文件中的配置项
        :return: 配置文件中的值（字符串）
        """
        return self.__cp.get(section, option)

    def getbool(self, section: str, option: str) -> bool:
        """
        以 bool 的形式获取配置文件中的值
        :param section: 配置文件中的section
        :param option: 配置文件中的配置项
        :return: 配置文件中的值（bool）
        """
        return self.__cp.getboolean(section, option)

    def getint(self, section: str, option: str) -> int:
        """
        以 int 的形式获取配置文件中的值
        :param section: 配置文件中的section
        :param option: 配置文件中的配置项
        :return: 配置文件中的值（int）
        """
        return self.__cp.getint(section, option)

    def getlist(self, section: str, option: str) -> List:
        """
        以 List 的形式获取配置文件中的值
        :param section: 配置文件中的section
        :param option: 配置文件中的配置项
        :return: 配置文件中的值（List）
        """
        return json.loads(self.__cp.get(section, option))

    @property
    def config_dict(self) -> dict:
        """
        获取配置文件中的所有配置项
        :return: 配置文件中的所有配置项
        """
        return self.__cp._sections

    # TODO: 封装get方法，判断不为空
