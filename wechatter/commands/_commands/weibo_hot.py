# 获取微博热搜命令
from typing import List

import requests

from wechatter.sender import Sender
from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo


@command(
    command="weibo-hot",
    keys=["微博热搜", "weibo-hot"],
    desc="获取微博热搜。",
    value=130,
)
def weibo_hot_command_handler(to: SendTo, message: str = "") -> None:
    response = get_weibo_hot_str()
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))


def get_weibo_hot_str() -> str:
    hot_list = get_weibo_hot_list()
    if hot_list == []:
        return "获取微博热搜失败"
    hot_search_str = "✨=====微博热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_search_str += f"{i + 1}. {hot_search.get('desc')}\n"
    return hot_search_str


def get_weibo_hot_list() -> List:
    response: requests.Response
    try:
        # url = "https://weibo.com/ajax/side/hotSearch"
        url = "https://m.weibo.cn/api/container/getIndex?containerid=106003%26filter_type%3Drealtimehot"
        response = requests.get(url, timeout=10)
    except Exception:
        print("请求微博热搜失败")
        return []

    if response.status_code != 200:
        print("获取微博热搜失败")
        return []
    hot_dict = response.json()
    return hot_dict.get("data", {}).get("cards", [])[0].get("card_group", [])[:20]
