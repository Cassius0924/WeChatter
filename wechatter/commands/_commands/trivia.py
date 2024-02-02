from typing import List
import random

import requests
from bs4 import BeautifulSoup
from loguru import logger

from wechatter.commands.handlers import command
from wechatter.exceptions import Bs4ParsingError
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender
from wechatter.utils import get_request


@command(
    command="trivia",
    keys=["冷知识", "trivia"],
    desc="获取冷知识。",
    value=170,
)
def trivia_command_handler(to: SendTo, message: str = "") -> None:
    random_number = random.randint(1, 917)
    try:
        response = get_request(
            url=f"http://www.quzhishi.com/shiwangelengzhishi/{random_number}.html"
        )
        trivia_list = _parse_trivia_response(response)
        result = _generate_trivia_message(trivia_list, random_number)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, result))
    except Exception as e:
        error_message = f"获取冷知识失败，错误信息：{e}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def _parse_trivia_response(response: requests.Response) -> List:
    soup = BeautifulSoup(response.text, "html.parser")
    trivia_list = []
    articles = soup.select_one("div.list").find_all("li")
    for article in articles:
        trivia = article.text.strip()
        if trivia:
            trivia_list.append(trivia)
    if not trivia_list:
        logger.error("解析冷知识失败")
        raise Bs4ParsingError("解析冷知识失败")
    return trivia_list


def _generate_trivia_message(trivia_list: List, random_number) -> str:
    if not trivia_list:
        return "获取冷知识失败"

    random_numbers = random.sample(range(1, len(trivia_list)), 3)
    trivia_str = "✨=====冷知识=====✨\n"
    trivia_str += f"1.{trivia_list[random_numbers[0]]}\n\n"
    trivia_str += f"2.{trivia_list[random_numbers[1]]}\n\n"
    trivia_str += f"3.{trivia_list[random_numbers[2]]}\n"
    trivia_str += f"❇️第{random_number}期的第{random_numbers}条冷知识❇️\n"
    return trivia_str
