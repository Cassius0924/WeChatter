from typing import Dict

import yaml
from loguru import logger

from wechatter.utils.path_manager import get_abs_path


def load_config(config_path="config.yaml") -> Dict:
    config_path = get_abs_path(config_path)
    logger.info(f"正在加载配置文件 {config_path} ...")

    try:
        with open(config_path, "r") as file:
            yaml_data = yaml.safe_load(file)
    except FileNotFoundError:
        logger.critical(
            f"未找到 {config_path} 配置文件！若首次使用，请先复制配置文件模板！"
        )
        exit(1)
    else:
        logger.info(f"配置文件加载成功：{yaml_data}")
        return yaml_data


def validate_config(config):
    """
    验证配置文件
    :param config: 配置文件
    """
    logger.info("正在验证配置文件...")
    # valid_types = ["text", "image"]
    # if config["official_account_reminder_type"] not in valid_types:
    #     error_msg = (
    #         f"配置参数错误：official_account_reminder_type 参数可选择为 {valid_types} "
    #     )
    #     logger.critical(error_msg)
    #     raise ValueError(error_msg)

    logger.info("配置文件验证通过！")
