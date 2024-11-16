import random
from typing import List, Union

import requests
from bs4 import BeautifulSoup
from loguru import logger

from wechatter.commands.handlers import command
from wechatter.exceptions import Bs4ParsingError
from wechatter.models.wechat import SendTo
from wechatter.sender import sender
from wechatter.utils import get_request


# TODO: 重写!!!
@command(
    command="trivia",
    keys=["冷知识", "trivia"],
    desc="获取冷知识。",
)
def trivia_command_handler(to: Union[str, SendTo], message: str = "") -> None:
    random_number = random.randint(1, 946)  # nosec
    try:
        response = get_request(
            url=f"http://www.zhangzaixi.com/shiwangelengzhishi/{random_number}.html"
        )
        trivia_list = _parse_trivia_response(response)
        result = _generate_trivia_message(trivia_list, random_number)
        sender.send_msg(to, result)
    except Exception as e:
        error_message = f"获取冷知识失败，错误信息：{str(e)}"
        logger.error(error_message)
        sender.send_msg(to, error_message)


def _parse_trivia_response(response: requests.Response) -> List:
    soup = BeautifulSoup(response.text, "html.parser")
    trivia_list = []
    list_div = soup.select_one("div.list")
    if list_div:
        articles = list_div.find_all("li")
        if articles:
            for article in articles:
                trivia = article.text.strip()
                if trivia:
                    trivia_list.append(trivia)
                else:
                    logger.error("冷知识为空")
                    raise Bs4ParsingError("冷知识为空")
        else:
            logger.error("未找到li标签")
            raise Bs4ParsingError("未找到li标签")
    else:
        logger.error("未找到div.list标签")
        raise Bs4ParsingError("未找到div.list标签")

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
    trivia_str += f"❇️第{random_number}期的第{random_numbers}条冷知识❇️"
    return trivia_str
