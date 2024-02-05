from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.message import SendTo
from wechatter.sender import sender
from wechatter.utils.time import get_current_ymd


@command(
    command="people-daily",
    keys=["人民日报", "people", "people-daily"],
    desc="获取人民日报。",
)
def people_daily_command_handler(to: SendTo, message: str = "") -> None:
    """发送人民日报url"""
    _send_people_daily(to, message, type="fileUrl")


@command(
    command="people-daily-url",
    keys=["人民日报链接", "people-url", "people-daily-url"],
    desc="获取人民日报url。",
)
def people_daily_url_command_handler(to: SendTo, message: str = "") -> None:
    """发送人民日报url"""
    _send_people_daily(to, message, type="text")


def _send_people_daily(to: SendTo, message: str, type: str) -> None:
    if message == "":
        try:
            url = get_today_people_daliy_url()
        except Exception as e:
            error_message = f"获取今天的人民日报失败，错误信息：{str(e)}"
            logger.error(error_message)
            sender.send_msg(to, error_message)
        else:
            sender.send_msg(to, url, type=type)
    # 获取指定日期
    else:
        try:
            url = get_people_daily_url(message)
        except Exception as e:
            error_message = f"输入的日期版本号不符合要求，请重新输入，错误信息：{str(e)}\n若要获取2021年1月2日03版的人民日报的URL，请输入：\n/people-url 2021010203"
            logger.error(error_message)
            sender.send_msg(to, error_message)
        else:
            sender.send_msg(to, url, type=type)


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
