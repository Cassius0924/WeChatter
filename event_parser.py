from typing import Union


# 用于解析消息的事件：login、logout、error
class EventParser:
    def __init__(self) -> None:
        pass

    # 解析是否为登录消息
    @staticmethod
    def parse_login(content: Union[str, dict]) -> bool:
        # 如果是字符串，说明是普通消息
        if isinstance(content, str):
            return False
        if content["event"] == "login":
            return True
        return False

    # 解析是否为登出消息
    @staticmethod
    def parse_logout(content: Union[str, dict]) -> bool:
        if isinstance(content, str):
            return False
        if content["event"] == "logout":
            return True
        return False

    # 解析是否为错误消息
    @staticmethod
    def parse_error(content: Union[str, dict]) -> bool:
        if isinstance(content, str):
            return False
        if content["event"] == "error":
            return True
        return False
