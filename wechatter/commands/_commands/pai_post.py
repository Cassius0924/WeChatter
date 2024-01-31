from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender


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
        error_message = f"获取少数派早报失败，错误信息: {str(e)}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_pai_post_str() -> str:
    try:
        response = get_pai_post_response()
        pai_post_list = parse_pai_post_response(response)
    except Exception as e:
        raise Exception(f"解析少数派早报列表失败, 错误信息: {str(e)}")

    if not pai_post_list:
        raise Exception("少数派早报列表为空")

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
        raise Exception("解析少数派早报内容失败")

    return pai_post_list


def get_pai_post_response() -> requests.Response:
    response: requests.Response
    try:
        url = "https://sspai.com/"
        response = requests.get(url, timeout=10)
    except Exception as e:
        raise Exception(f"请求少数派早报API失败, 错误信息: {str(e)}")

    if response.status_code != 200:
        raise Exception(f"少数派早报API返回非200状态码, 状态码: {response.status_code}")

    return response
