from typing import List
import random

import requests
from bs4 import BeautifulSoup

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
    #TODO：获取共有多少期
    random_number = random.randint(1, 917)
    try:
        response = get_request(
            url=f"http://www.quzhishi.com/shiwangelengzhishi{random_number}.html"
        )
        response.encoding = response.apparent_encoding
        trivia_list = parse_trivia_response(response)
        result = generate_trivia_message(trivia_list, random_number)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, result))
    except Exception as e:
        error_message = f"获取冷知识失败，错误信息：{e}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def parse_trivia_response(response: requests.Response) -> List:
    soup = BeautifulSoup(response.text, "html.parser")
    trivia_list = []
    articles = soup.select_one("div.list").find_all("li")
    for article in articles:
        trivia = article.text.strip()
        if trivia:
            trivia_list.append(trivia)
    if not trivia_list:
        raise Bs4ParsingError("解析冷知识失败")
    return trivia_list


def generate_trivia_message(trivia_list: List, random_number) -> str:
    trivia_str = "✨=====冷知识=====✨\n"
    trivia_str += f"这是第{random_number}期冷知识\n"
    for i, trivia in enumerate(trivia_list):
        trivia_str += f"{i + 1}. {trivia}\n"
    return trivia_str

#TODO：获取随机一期冷知识中的随机一条冷知识
