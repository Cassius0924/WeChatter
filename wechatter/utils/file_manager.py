# 文件夹管理类
import os
from typing import List

from loguru import logger

import wechatter.utils.path_manager as pm


def check_and_create_folder(*paths: str) -> None:
    """
    检查文件是否存在，如果不存在则创建
    :param *paths: 文件夹路径（可变参数）
    """
    path = pm.join_path(*paths)
    abs_path = pm.get_abs_path(path)
    if not os.path.exists(abs_path):
        try:
            os.makedirs(abs_path)
            logger.info(f"成功创建文件夹 '{abs_path}'。")
        except FileNotFoundError:
            logger.error(f"路径 '{abs_path}' 不存在。")
        except PermissionError:
            logger.error(f"没有在 '{abs_path}' 创建文件夹的权限。")
        except Exception as e:
            logger.error(f"在尝试创建文件夹 '{abs_path}' 时出现未知错误：{str(e)}")


def is_folder_exist(*paths: str) -> bool:
    """
    检查文件夹是否存在
    :param *paths: 文件夹路径（可变参数）
    """
    path = pm.join_path(*paths)
    abs_path = pm.get_abs_path(path)
    return os.path.exists(abs_path)


def create_folder(*paths: str) -> None:
    """
    创建文件夹
    :param *paths: 文件夹路径（可变参数）
    """
    path = pm.join_path(*paths)
    abs_path = pm.get_abs_path(path)
    try:
        os.makedirs(abs_path)
        logger.info(f"成功创建文件夹 '{abs_path}'。")
    except FileNotFoundError:
        logger.error(f"路径 '{abs_path}' 不存在。")
    except PermissionError:
        logger.error(f"没有在 '{abs_path}' 创建文件夹的权限。")
    except Exception as e:
        logger.error(f"在尝试创建文件夹 '{abs_path}' 时出现未知错误：{str(e)}")


def create_file(*paths: str) -> None:
    """
    创建文件
    :param *paths: 文件路径（可变参数）
    """
    path = pm.join_path(*paths)
    abs_path = pm.get_abs_path(path)
    try:
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write("")
        logger.info(f"文件 '{abs_path}' 已创建。")
    except FileNotFoundError:
        logger.error(f"路径 '{abs_path}' 不存在。")
    except PermissionError:
        logger.error(f"没有在 '{abs_path}' 创建文件的权限。")
    except Exception as e:
        logger.error(f"在尝试创建文件 '{abs_path}' 时出现未知错误：{str(e)}")


def is_file_exist(*paths: str) -> bool:
    """
    检查文件是否存在
    :param *paths: 文件路径（可变参数）
    """
    path = pm.join_path(*paths)
    abs_path = pm.get_abs_path(path)
    return os.path.exists(abs_path)


def check_and_create_file(*paths: str) -> None:
    """
    检查文件是否存在，如果不存在则创建
    :param *paths: 文件路径（可变参数）
    """
    path = pm.join_path(*paths)
    abs_path = pm.get_abs_path(path)
    if not os.path.exists(abs_path):
        try:
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write("")
            logger.info(f"成功创建文件 '{abs_path}'。")
        except FileNotFoundError:
            logger.error(f"路径 '{abs_path}' 不存在。")
        except PermissionError:
            logger.error(f"没有在 '{abs_path}' 创建文件的权限。")
        except Exception as e:
            logger.error(f"在尝试写入文件 '{abs_path}' 时出现未知错误：{str(e)}")


def list_files(*paths: str, suffixs: List[str] = []) -> List[str]:
    """
    列出路径下所有文件（不包括文件夹）
    :param *paths: 路径（可变参数）
    :param suffix: 文件后缀
    """
    path = pm.join_path(*paths)
    abs_path = pm.get_abs_path(path)
    if not os.path.exists(abs_path):
        logger.error(f"路径 '{abs_path}' 不存在。")
        return []
    files = os.listdir(abs_path)
    if len(suffixs) == 0:
        return [file for file in files if os.path.isfile(os.path.join(abs_path, file))]
    else:
        return [
            file
            for file in files
            if os.path.isfile(os.path.join(abs_path, file))
            and os.path.splitext(file)[1] in suffixs
        ]


def list_folder(*paths: str) -> List[str]:
    """
    列出路径下所有文件夹
    :param *paths: 路径（可变参数）
    """
    path = pm.join_path(*paths)
    abs_path = pm.get_abs_path(path)
    if not os.path.exists(abs_path):
        logger.error(f"路径 '{abs_path}' 不存在。")
        return []
    try:
        files = os.listdir(abs_path)
    except NotADirectoryError:
        logger.error(f"路径 '{abs_path}' 不是文件夹。")
        return []
    return [file for file in files if os.path.isdir(os.path.join(abs_path, file))]


def delete_file(*paths: str) -> None:
    """
    删除文件
    :param *paths: 文件路径（可变参数）
    """
    path = pm.join_path(*paths)
    abs_path = pm.get_abs_path(path)
    if not os.path.exists(abs_path):
        logger.error(f"文件 '{abs_path}' 不存在。")
        return
    try:
        os.remove(abs_path)
        logger.info(f"文件 '{abs_path}' 已删除。")
    except PermissionError:
        logger.error(f"没有在 '{abs_path}' 删除文件的权限。")
    except Exception as e:
        logger.error(f"在尝试删除文件 '{abs_path}' 时出现未知错误：{str(e)}")


def delete_folder(*paths: str) -> None:
    """
    删除文件夹
    :param *paths: 文件夹路径（可变参数）
    """
    path = pm.join_path(*paths)
    abs_path = pm.get_abs_path(path)
    if not os.path.exists(abs_path):
        logger.error(f"文件夹 '{abs_path}' 不存在。")
        return
    try:
        os.rmdir(abs_path)
        logger.info(f"文件夹 '{abs_path}' 已删除。")
    except PermissionError:
        logger.error(f"没有在 '{abs_path}' 删除文件夹的权限。")
    except Exception as e:
        logger.error(f"在尝试删除文件夹 '{abs_path}' 时出现未知错误：{str(e)}")


def rename_file(file_path: str, new_name: str) -> None:
    """
    重命名文件
    :param file_path: 文件路径
    :param new_name: 新文件名
    """
    abs_path = pm.get_abs_path(file_path)
    if not os.path.exists(abs_path):
        logger.error(f"文件 '{abs_path}' 不存在。")
        return
    file_dir = os.path.dirname(abs_path)
    new_path = os.path.join(file_dir, new_name)
    try:
        os.rename(abs_path, new_path)
        logger.info(f"文件 '{abs_path}' 已重命名为 '{new_path}'。")
    except PermissionError:
        logger.error(f"没有在 '{abs_path}' 重命名文件的权限。")
    except Exception as e:
        logger.error(f"在尝试重命名文件 '{abs_path}' 时出现未知错误：{str(e)}")
