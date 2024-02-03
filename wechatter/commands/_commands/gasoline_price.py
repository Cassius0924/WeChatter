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
    command="gasoline_price",
    keys=["汽油", "gasoline_price", "汽油价格"],
    desc="获取汽油价格。",
    value=180,
)
def gasoline_price_command_handler(to: SendTo, message: str = "") -> None:
    try:
        response = get_request(
            url="https://www.icauto.com.cn/oil/price_440700_2_1.html"
        )
        gasoline_price = _parse_gasoline_price_response(response)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, gasoline_price))
    except Exception as e:
        error_message = f"获取汽油价格失败，错误信息：{e}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def _parse_gasoline_price_response(response: requests.Response) -> str:
    soup = BeautifulSoup(response.text, 'html.parser')
    article_body_div = soup.select_one("div.articlebody")

    if article_body_div:
        # 找到div内的第二个p元素
        second_p_element = article_body_div.find_all('p')[1]

        if second_p_element:
            # 提取第二个p元素的文本内容
            text_content = second_p_element.get_text()
            desired_text = text_content.split('，若需要计算')[0]

        else:
            logger.error("找不到第二个p元素")
            raise Bs4ParsingError("找不到第二个p元素")
    else:
        logger.error("找不到class等于'articlebody'的div")
        raise Bs4ParsingError("找不到class等于'articlebody'的div")
    return desired_text
