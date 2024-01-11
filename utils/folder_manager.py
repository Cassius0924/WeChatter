# 文件夹管理类
import os
from typing import List
from utils.path import PathManager as pm


class FolderManager:
    """文件夹管理类"""

    @staticmethod
    def check_and_create(*paths: str) -> None:
        """
        检查文件夹是否存在，如果不存在则创建
        :param *paths: 文件夹路径（可变参数）
        """
        # q: 如何传多个参数
        # a: 用 *args，def check_and_create(*args)
        path = pm.join_path(*paths)
        abs_path = pm.get_abs_path(path)
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
            print(f"未找到文件夹 '{abs_path}' ，已创建。")
        else:
            print(f"文件夹 '{abs_path}' 已存在。")

    @staticmethod
    def is_folder_exist(*paths: str) -> bool:
        """
        检查文件夹是否存在
        :param *paths: 文件夹路径（可变参数）
        """
        path = pm.join_path(*paths)
        abs_path = pm.get_abs_path(path)
        return os.path.exists(abs_path)

    @staticmethod
    def create(*paths: str) -> None:
        """
        创建文件夹
        :param *paths: 文件夹路径（可变参数）
        """
        path = pm.join_path(*paths)
        abs_path = pm.get_abs_path(path)
        os.makedirs(abs_path)
        print(f"文件夹 '{abs_path}' 已创建。")

    @staticmethod
    def list_files(*paths: str) -> List[str]:
        """
        列出文件夹下所有文件（不包括文件夹）
        :param *paths: 文件夹路径（可变参数）
        """
        path = pm.join_path(*paths)
        abs_path = pm.get_abs_path(path)
        if not os.path.exists(abs_path):
            print(f"文件夹 '{abs_path}' 不存在。")
            return []
        files = os.listdir(abs_path)
        return [file for file in files if os.path.isfile(os.path.join(abs_path, file))]

    @staticmethod
    def list_dirs(*paths: str) -> List[str]:
        """
        列出文件夹下所有文件夹
        :param *paths: 文件夹路径（可变参数）
        """
        path = pm.join_path(*paths)
        abs_path = pm.get_abs_path(path)
        if not os.path.exists(abs_path):
            print(f"文件夹 '{abs_path}' 不存在。")
            return []
        files = os.listdir(abs_path)
        return [file for file in files if os.path.isdir(os.path.join(abs_path, file))]
