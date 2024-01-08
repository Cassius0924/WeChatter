# 文件夹管理类
import os
from utils.path import get_abs_path


class FolderManager:
    """文件夹管理类"""

    @staticmethod
    def check_and_create(path: str) -> None:
        """
        检查文件夹是否存在，如果不存在则创建
        :param folder_path: 文件夹路径
        """
        abs_path = get_abs_path(path)
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
            print(f"未找到文件夹 '{abs_path}' ，已创建。")
        else:
            print(f"文件夹 '{abs_path}' 已存在。")
