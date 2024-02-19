QUOTABLE_FORMAT = "（可引用：%s）\n"


# 将消息可引用化
def make_quotable(message: str) -> str:
    """
    将消息可引用化
    :param message: 消息内容
    :return: 可引用的消息内容
    """
    # 获取可引用消息的ID（可引用标识符）
    quotable_id = _get_random_quotable_id()
    return QUOTABLE_FORMAT % quotable_id + message


def _get_random_quotable_id() -> str:
    """
    获取可引用消息的ID
    :return: 可引用消息的ID
    """
