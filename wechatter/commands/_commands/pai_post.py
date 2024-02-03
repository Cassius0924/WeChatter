from typing import List

import requests
from bs4 import BeautifulSoup
from loguru import logger

from wechatter.commands.handlers import command
from wechatter.exceptions import Bs4ParsingError
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender
from wechatter.utils import get_request


@command(
    command="pai-post",
    keys=["派早报", "pai-post"],
    desc="获取少数派早报。",
)
def pai_post_command_handler(to: SendTo, message: str = "") -> None:
    try:
        result = get_pai_post_str()
    except Exception as e:
        error_message = f"获取少数派早报失败，错误信息：{str(e)}"
        logger.error(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))
    else:
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, result))


def get_pai_post_str() -> str:
    response = get_request(url="https://sspai.com/")
    pai_post_list = _parse_pai_post_response(response)
    return _generate_pai_post_message(pai_post_list)


def _parse_pai_post_response(response: requests.Response) -> List:
    soup = BeautifulSoup(response.text, "html.parser")
    pai_post_list = []
    articles = soup.select("div.pai_abstract")
    if not articles:
        logger.error("少数派早报列表为空")
        raise Bs4ParsingError("少数派早报列表为空")

    for article in articles:
        pai_post_item = {}

        title = article.select_one("a div")
        if title:
            pai_post_item["title"] = title.text.strip()

        if pai_post_item:
            pai_post_list.append(pai_post_item)

    if not pai_post_list:
        logger.error("少数派早报列表返回值格式错误")
        raise Bs4ParsingError("少数派早报列表返回值格式错误")

    return pai_post_list


def _generate_pai_post_message(pai_post_list: List) -> str:
    if not pai_post_list:
        return "暂无少数派早报"

    pai_post_str = "✨=====派早报=====✨\n"
    for i, pai_post in enumerate(pai_post_list):
        pai_post_str += f"{i + 1}. {pai_post.get('title')}\n"

    return pai_post_str
