import json
from typing import Dict

from loguru import logger


def save_json(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file)
    except FileNotFoundError:
        logger.error(f"未找到文件 {file_path}。")
        raise FileNotFoundError(f"未找到文件 {file_path}。")
    except PermissionError:
        logger.error(f"写入文件 {file_path} 时权限被拒绝。")
        raise PermissionError(f"写入文件 {file_path} 时权限被拒绝。")
    except Exception as e:
        logger.error(f"保存 JSON 数据时发生未知错误: {e}")
        raise Exception(f"保存 JSON 数据时发生未知错误: {e}")


def load_json(file_path) -> Dict:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"未找到文件 {file_path}。")
        raise FileNotFoundError(f"未找到文件 {file_path}。")
    except PermissionError:
        logger.error(f"从文件 {file_path} 读取时权限被拒绝。")
        raise PermissionError(f"从文件 {file_path} 读取时权限被拒绝。")
    except json.JSONDecodeError:
        logger.error(f"文件 {file_path} 中的 JSON 数据无效。")
        raise json.JSONDecodeError(f"文件 {file_path} 中的 JSON 数据无效。")
    except Exception as e:
        logger.error(f"加载 JSON 数据时发生未知错误: {e}")
        raise Exception(f"加载 JSON 数据时发生未知错误: {e}")
