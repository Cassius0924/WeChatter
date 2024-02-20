import string

from wechatter.database import QuotedResponse as DbQuotedResponse, make_db_session
from wechatter.models.wechat import QUOTABLE_FORMAT, QuotedResponse

# QUOTABLE_FORMAT = "（可引用：%s）\n"
CHARS = string.digits + string.ascii_letters


# 将消息可引用化
def make_quotable(message: str, quoted_response: QuotedResponse) -> str:
    """
    将消息可引用化
    :param message: 消息内容
    :param quoted_response: 可引用的消息内容
    :return: 可引用的消息内容
    """
    # 获取可引用消息的ID（可引用标识符）
    quotable_id = _get_quotable_id()
    quoted_response.quotable_id = quotable_id
    with make_db_session() as session:
        # 将可引用标识符和回复消息存入数据库
        q_message = DbQuotedResponse.from_model(quoted_response)
        session.add(q_message)
        session.commit()

    # 将消息内容和可引用消息的ID拼接
    return (QUOTABLE_FORMAT % quotable_id) + message


def _get_quotable_id() -> str:
    """
    获取可引用消息的ID
    :return: 可引用消息的ID
    """
    # 获取最后一个可引用消息的ID
    with make_db_session() as session:
        quotable_id = (
            session.query(DbQuotedResponse).order_by(DbQuotedResponse.id.desc()).first()
        )
        # quotable_id 是由52个大小写字母加10个数字组成的三位字符串，每一位都有可能是0-9、a-z、A-Z中的任意一个字符
        if quotable_id:
            # id加1
            quotable_id = _increase_id(quotable_id.quotable_id)
        else:
            quotable_id = "000"
        return quotable_id


def _increase_id(quotable_id: str) -> str:
    """
    将ID加1，如果ID超过 ZZZ，则从 000 开始
    """
    if quotable_id == "Z":
        return "0"

    if quotable_id[-1] == CHARS[-1]:
        return _increase_id(quotable_id[:-1]) + "0"
    else:
        return quotable_id[:-1] + CHARS[CHARS.find(quotable_id[-1]) + 1]
