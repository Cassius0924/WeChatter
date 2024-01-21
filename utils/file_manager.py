# 文件夹管理类
import os
from typing import List
from utils.path import PathManager as pm


class FileManager:
    """文件管理类"""

    @staticmethod
    def check_and_create_folder(*paths: str) -> None:
        """
        检查文件是否存在，如果不存在则创建
        :param *paths: 文件夹路径（可变参数）
        """
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
    def create_folder(*paths: str) -> None:
        """
        创建文件夹
        :param *paths: 文件夹路径（可变参数）
        """
        path = pm.join_path(*paths)
        abs_path = pm.get_abs_path(path)
        os.makedirs(abs_path)
        print(f"文件夹 '{abs_path}' 已创建。")

    @staticmethod
    def create_file(*paths: str) -> None:
        """
        创建文件
        :param *paths: 文件路径（可变参数）
        """
        path = pm.join_path(*paths)
        abs_path = pm.get_abs_path(path)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write("")
        print(f"文件 '{abs_path}' 已创建。")

    @staticmethod
    def is_file_exist(*paths: str) -> bool:
        """
        检查文件是否存在
        :param *paths: 文件路径（可变参数）
        """
        path = pm.join_path(*paths)
        abs_path = pm.get_abs_path(path)
        return os.path.exists(abs_path)

    @staticmethod
    def check_and_create_file(*paths: str) -> None:
        """
        检查文件是否存在，如果不存在则创建
        :param *paths: 文件路径（可变参数）
        """
        path = pm.join_path(*paths)
        abs_path = pm.get_abs_path(path)
        if not os.path.exists(abs_path):
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write("")
            print(f"未找到文件 '{abs_path}' ，已创建。")
        else:
            print(f"文件 '{abs_path}' 已存在。")

    @staticmethod
    def list_files(*paths: str, suffixs: List[str] = []) -> List[str]:
        """
        列出路径下所有文件（不包括文件夹）
        :param *paths: 路径（可变参数）
        :param suffix: 文件后缀
        """
        path = pm.join_path(*paths)
        abs_path = pm.get_abs_path(path)
        if not os.path.exists(abs_path):
            print(f"路径 '{abs_path}' 不存在。")
            return []
        files = os.listdir(abs_path)
        if len(suffixs) == 0:
            return [
                file for file in files if os.path.isfile(os.path.join(abs_path, file))
            ]
        else:
            return [
                file
                for file in files
                if os.path.isfile(os.path.join(abs_path, file))
                and os.path.splitext(file)[1] in suffixs
            ]

    @staticmethod
    def list_folder(*paths: str) -> List[str]:
        """
        列出路径下所有文件夹
        :param *paths: 路径（可变参数）
        """
        path = pm.join_path(*paths)
        abs_path = pm.get_abs_path(path)
        if not os.path.exists(abs_path):
            print(f"路径 '{abs_path}' 不存在。")
            return []
        files = os.listdir(abs_path)
        return [file for file in files if os.path.isdir(os.path.join(abs_path, file))]

    @staticmethod
    def delete_file(*paths: str) -> None:
        """
        删除文件
        :param *paths: 文件路径（可变参数）
        """
        path = pm.join_path(*paths)
        abs_path = pm.get_abs_path(path)
        if not os.path.exists(abs_path):
            print(f"文件 '{abs_path}' 不存在。")
            return
        os.remove(abs_path)
        print(f"文件 '{abs_path}' 已删除。")

    @staticmethod
    def delete_folder(*paths: str) -> None:
        """
        删除文件夹
        :param *paths: 文件夹路径（可变参数）
        """
        path = pm.join_path(*paths)
        abs_path = pm.get_abs_path(path)
        if not os.path.exists(abs_path):
            print(f"文件夹 '{abs_path}' 不存在。")
            return
        os.rmdir(abs_path)
        print(f"文件夹 '{abs_path}' 已删除。")

    @staticmethod
    def rename_file(file_path: str, new_name: str) -> None:
        """
        重命名文件
        :param file_path: 文件路径
        :param new_name: 新文件名
        """
        abs_path = pm.get_abs_path(file_path)
        if not os.path.exists(abs_path):
            print(f"文件 '{abs_path}' 不存在。")
            return
        file_dir = os.path.dirname(abs_path)
        new_path = os.path.join(file_dir, new_name)
        os.rename(abs_path, new_path)
