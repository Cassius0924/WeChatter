# 文件夹管理类
import os


class FolderManager:
    """文件夹管理类"""

    @staticmethod
    def check_and_create(folder_path):
        """
        检查文件夹是否存在，如果不存在则创建
        :param folder_path: 文件夹路径
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"未找到文件夹 '{folder_path}' ，已创建。")
        else:
            print(f"文件夹 '{folder_path}' 已存在。")
