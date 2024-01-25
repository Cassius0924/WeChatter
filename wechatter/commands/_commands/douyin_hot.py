from typing import List

import requests

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender


@command(
    command="douyin-hot",
    keys=["抖音热搜", "douyin-hot"],
    desc="获取抖音热搜。",
    value=50,
)
def douyin_hot_command_handler(to: SendTo, message: str = "") -> None:
    response = get_douyin_hot_str()
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))


def get_douyin_hot_str() -> str:
    hot_list = get_douyin_hot_list()
    if hot_list == []:
        return "获取抖音热搜失败"
    hot_str = "✨=====抖音热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_str += f"{i + 1}.  {hot_search.get('word')}\n"
    return hot_str


def get_douyin_hot_list() -> List:
    url = "https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print("获取抖音热搜失败")
        return []
    hot_dict = response.json()
    return hot_dict.get("word_list", [])
