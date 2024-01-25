from typing import Optional

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender
from wechatter.utils.time import get_current_ymd


@command(
    command="people",
    keys=["人民日报", "people", "people-daily"],
    desc="获取人民日报。",
    value=80,
)
def people_daily_command_handler(to: SendTo, message: str = "") -> None:
    """发送人民日报url"""
    # 发送当天01版本的人民日报PDF
    if message.lower() == "url":
        url = get_paper_people_url()
        _send_text_msg(to, url)
    elif message.lower().startswith("url"):
        # 发送特定日期特定版本的url
        parts = message.lower().split()
        if len(parts) == 2 and parts[0] == "url" and parts[1].isdigit():
            url = get_paper_people_pdf_url(parts[1])
            if url:
                _send_text_msg(to, url)
            if url is None:
                e = "输入的日期版本号不符合要求，请重新输入\n若要获取2021年1月2日03版的人民日报的url，请输入\n/people url 2021010203"
                _send_text_msg(to, e)
    else:
        # 发送人民日报PDF文件
        # 发送特定日期特定版本的人民日报PDF
        if message != "":
            url = get_paper_people_pdf_url(message)
            if url:
                _send_file_url_msg(to, url)
            if url is None:
                e = "输入的日期版本号不符合要求，请重新输入\n若要获取2021年1月2日03版的人民日报的pdf，请输入\n/people 2021010203"
                _send_text_msg(to, e)

        # 发送当天01版本的人民日报PDF
        if message == "":
            url = get_paper_people_url()
            _send_file_url_msg(to, url)


def _send_file_url_msg(to: SendTo, message: str = "") -> None:
    """封装发送文件URL消息"""
    Sender.send_msg(to, SendMessage(SendMessageType.FILE_URL, message))


def _send_text_msg(to: SendTo, message: str = "") -> None:
    """封装发送文本消息"""
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, message))


def get_paper_people_pdf_url(date_version: str) -> Optional[str]:  # 2024010901
    """获取特定日期特定版本的人民日报pdf到本地并返回url"""
    # 判断字符串是否为数字并且长度为10
    if date_version.isdigit() and len(date_version) == 10:
        yearmonthday = date_version[:8]  # 20240109
        year = date_version[:4]  # 2024
        month = date_version[4:6]  # 01
        day = date_version[6:8]  # 09
        year_month = f"{year}-{month}"  # 2024-01
        version = date_version[8:]  # 01
        # url = "http://paper.people.com.cn/rmrb/images/2024-01/09/01/rmrb2024010901.pdf"
        url = f"http://paper.people.com.cn/rmrb/images/{year_month}/{day}/{version}/rmrb{yearmonthday}{version}.pdf"
        return url
    if not (date_version.isdigit() and len(date_version) == 10):
        print("输入的日期版本号不符合要求，请重新输入...")
        return None


def get_paper_people_url() -> str:
    """获取今日01版人民日报pdf的url"""
    yearmonthday = get_current_ymd()
    version = "01"
    today_version = f"{yearmonthday}{version}"
    url = get_paper_people_pdf_url(today_version)
    return url
