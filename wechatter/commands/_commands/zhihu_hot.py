# 知乎热搜命令
from typing import List

import requests

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender


@command(
    command="zhihu-hot",
    keys=["知乎热搜", "zhihu-hot"],
    desc="获取知乎热搜。",
    value=140,
)
def zhihu_hot_command_handler(to: SendTo, message: str = "") -> None:
    response = get_zhihu_hot_str()
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))


def get_zhihu_hot_str() -> str:
    hot_list = get_zhihu_hot_list()
    if len(hot_list) == 0:
        return "获取知乎热搜失败"
    hot_search_str = "✨=====知乎热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_search_str += f"{i + 1}. {hot_search.get('target', {}).get('title', '')}\n"
    return hot_search_str


def get_zhihu_hot_list() -> List:
    response: requests.Response
    try:
        # url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
        url = "https://api.zhihu.com/topstory/hot-list?limit=10"
        response = requests.get(url, timeout=10)
    except Exception:
        print("请求知乎热搜失败")
        return []

    if response.status_code != 200:
        print("获取知乎热搜失败")
        return []
    hot_dict = response.json()
    return hot_dict.get("data", [])
