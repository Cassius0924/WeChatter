# 文件路径管理
import os

def get_abs_path(relative_path: str) -> str:
    """获取绝对路径
    :param relative_path: 文件相对于项目目录的相对路径
    """
    # 由于这个文件在 utils 文件夹下，工作路径是在上一层 utils/..
    working_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(working_dir_path, relative_path)
