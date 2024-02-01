from typing import Dict, List

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
    value=70,
)
def pai_post_command_handler(to: SendTo, message: str = "") -> None:
    try:
        response = get_pai_post_str()
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))
    except Exception as e:
        error_message = f"获取少数派早报失败，错误信息：{e}"
        logger.error(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_pai_post_str() -> str:
    response = get_request(url="https://sspai.com/")
    try:
        pai_post_list = parse_pai_post_response(response)
    except Bs4ParsingError:
        logger.error("少数派早报列表返回值格式错误")
        raise Bs4ParsingError("少数派早报列表返回值格式错误")

    if not pai_post_list:
        return "少数派早报列表为空"

    pai_post_str = "✨=====派早报=====✨\n"
    for i, pai_post in enumerate(pai_post_list):
        pai_post_str += f"{i + 1}. {pai_post.get('title')}\n"

    return pai_post_str


def parse_pai_post_response(response: requests.Response) -> List[Dict[str, str]]:
    soup = BeautifulSoup(response.text, "html.parser")
    pai_post_list = []
    articles = soup.select("div.pai_abstract")
    for article in articles:
        pai_post_item = {}

        title = article.select_one("a div")
        if title:
            pai_post_item["title"] = title.text.strip()

        if pai_post_item:
            pai_post_list.append(pai_post_item)

    if not pai_post_list:
        raise Bs4ParsingError

    return pai_post_list
