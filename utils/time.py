# 获取时间工具类
import time


def get_current_timestamp() -> int:
    """获取当前时间戳
    返回当前时间戳
    """
    return int(time.time())


def get_current_datetime() -> str:
    """获取当前时间
    返回格式化后的时间字符串
    """
    return time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())


def get_current_date() -> str:
    """获取当前日期
    返回格式化后的日期字符串
    """
    return time.strftime("%y-%m-%d", time.localtime())


def get_current_time() -> str:
    """获取当前时间
    返回格式化后的时间字符串
    """
    return time.strftime("%H:%M:%S", time.localtime())
