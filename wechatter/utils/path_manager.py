# 文件路径管理
import os


def get_abs_path(relative_path: str) -> str:
    """
    获取绝对路径
    :param relative_path: 文件相对于项目目录的相对路径
    :return: 文件的绝对路径
    """
    # 由于这个文件在 utils 文件夹下，项目更根目录是在上上层 utils/../..
    working_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    return os.path.join(working_dir_path, relative_path)


def join_path(*args) -> str:
    """
    拼接路径
    :param *args: 路径（可变参数）
    :return: 拼接后的路径
    """
    if len(args) == 1:
        return args[0]
    if len(args) == 0:
        return ""
    return os.path.join(*args)


def is_file_exist(*args) -> bool:
    """
    检查文件是否存在
    :param *args: 文件路径（可变参数）
    :return: 文件是否存在
    """
    path = join_path(*args)
    return os.path.exists(path)
