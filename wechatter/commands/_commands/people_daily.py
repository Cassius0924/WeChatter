from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender
from wechatter.utils.time import get_current_ymd


@command(
    command="people-daily",
    keys=["人民日报", "people", "people-daily"],
    desc="获取人民日报。",
)
def people_daily_command_handler(to: SendTo, message: str = "") -> None:
    """发送人民日报url"""
    # 发送当天01版本的人民日报PDF
    if message == "":
        try:
            url = get_today_people_daliy_url()
        except Exception as e:
            error_message = f"获取今日人民日报失败，错误信息：{e}"
            logger.error(error_message)
            _send_text_msg(to, error_message)
        else:
            _send_file_url_msg(to, url)
    else:
        try:
            url = get_people_daily_url(message)
        except Exception as e:
            error_message = f"输入的日期版本号不符合要求，请重新输入，错误信息：{e}\n若要获取2021年1月2日03版的人民日报的PDF，请输入：\n/people 2021010203"
            logger.error(error_message)
            _send_text_msg(to, error_message)
        else:
            _send_file_url_msg(to, url)


@command(
    command="people-daily-url",
    keys=["人民日报链接", "people-url", "people-daily-url"],
    desc="获取人民日报url。",
)
def people_daily_url_command_handler(to: SendTo, message: str = "") -> None:
    """发送人民日报url"""
    # 获取今天
    if message == "":
        try:
            url = get_today_people_daliy_url()
        except Exception as e:
            error_message = f"获取今天的人民日报失败，错误信息：{e}"
            logger.error(error_message)
            _send_text_msg(to, error_message)
        else:
            _send_text_msg(to, url)
    # 获取指定日期
    else:
        try:
            url = get_people_daily_url(message)
        except Exception as e:
            error_message = f"输入的日期版本号不符合要求，请重新输入，错误信息：{e}\n若要获取2021年1月2日03版的人民日报的URL，请输入：\n/people-url 2021010203"
            logger.error(error_message)
            _send_text_msg(to, error_message)
        else:
            _send_text_msg(to, url)


def get_people_daily_url(date_version: str) -> str:
    """获取特定日期特定版本的人民日报PDF到本地并返回url"""
    if not date_version.isdigit() or len(date_version) != 10:
        logger.error("输入的日期版本号不符合要求，请重新输入。")
        raise ValueError("输入的日期版本号不符合要求，请重新输入。")

    # 判断字符串是否为数字并且长度为10
    yearmonthday = date_version[:8]  # 20240109
    year = date_version[:4]  # 2024
    month = date_version[4:6]  # 01
    day = date_version[6:8]  # 09
    year_month = f"{year}-{month}"  # 2024-01
    version = date_version[8:]  # 01
    # url = "http://paper.people.com.cn/rmrb/images/2024-01/09/01/rmrb2024010901.pdf"
    return f"http://paper.people.com.cn/rmrb/images/{year_month}/{day}/{version}/rmrb{yearmonthday}{version}.pdf"


def get_today_people_daliy_url() -> str:
    """获取今日01版人民日报PDF的url"""
    yearmonthday = get_current_ymd()
    version = "01"
    today_version = f"{yearmonthday}{version}"
    return get_people_daily_url(today_version)


def _send_file_url_msg(to: SendTo, message: str = "") -> None:
    """封装发送文件URL消息"""
    Sender.send_msg(to, SendMessage(SendMessageType.FILE_URL, message))


def _send_text_msg(to: SendTo, message: str = "") -> None:
    """封装发送文本消息"""
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, message))
