import json
from typing import List, Tuple, Union

import requests
from bs4 import BeautifulSoup
from loguru import logger

from wechatter.commands.handlers import command
from wechatter.exceptions import Bs4ParsingError
from wechatter.models.wechat import QuotedResponse, SendTo
from wechatter.sender import sender
from wechatter.utils import get_request, url_encode

COMMAND_NAME = "pai-post"


@command(
    command=COMMAND_NAME,
    keys=["派早报", "pai-post"],
    desc="获取少数派早报。",
)
def pai_post_command_handler(to: Union[str, SendTo], message: str = "") -> None:
    try:
        result, q_response = get_pai_post_str()
    except Exception as e:
        error_message = f"获取少数派早报失败，错误信息：{str(e)}"
        logger.error(error_message)
        sender.send_msg(to, error_message)
    else:
        sender.send_msg(
            to,
            result,
            quoted_response=QuotedResponse(
                command=COMMAND_NAME,
                response=q_response,
            ),
        )


@pai_post_command_handler.quoted_handler
def pai_post_quoted_handler(
    to: SendTo, message: str = "", q_response: str = ""
) -> None:
    if not message.isdigit():
        logger.error("输入的早报编号不是数字")
        sender.send_msg(to, "请输入早报编号")
        return

    post_url_dict = json.loads(q_response)
    try:
        hot_url = post_url_dict[message]
    except Exception:
        logger.error("输入的早报编号错误")
        sender.send_msg(to, "输入的早报编号错误")
        return
    else:
        sender.send_msg(to, hot_url)


@pai_post_command_handler.mainfunc
def get_pai_post_str() -> Tuple[str, str]:
    response = get_request(url="https://sspai.com/")
    pai_post_list = _parse_pai_post_response(response)
    return (
        _generate_pai_post_message(pai_post_list),
        _generate_pai_post_quoted_response(pai_post_list),
    )


def _parse_pai_post_response(response: requests.Response) -> List:
    soup = BeautifulSoup(response.text, "html.parser")
    pai_post_list = []
    articles = soup.select("div.pai_abstract")
    if not articles:
        logger.error("少数派早报列表为空")
        raise Bs4ParsingError("少数派早报列表为空")

    for article in articles:
        pai_post_item = {}

        href = article.select_one("a")
        if href:
            pai_post_item["href"] = href.get("href")

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


def _generate_pai_post_quoted_response(pai_post_list: List) -> str:
    result = {}
    base_url = "https://sspai.com"
    for i, pai_post in enumerate(pai_post_list):
        href = pai_post.get("href", None)
        if href:
            result[str(i + 1)] = url_encode(base_url + href)
    return json.dumps(result)
