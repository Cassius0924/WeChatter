# 知乎热搜命令
from typing import Dict

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
    try:
        response = get_zhihu_hot_str()
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))
    except Exception as e:
        error_message = f"获取知乎热搜失败，错误信息: {str(e)}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_zhihu_hot_str() -> str:
    try:
        hot_list = get_zhihu_hot_response_json().get("data", [])
    except Exception as e:
        raise Exception(f"解析知乎热搜列表失败, 错误信息: {str(e)}")

    if not hot_list:
        raise Exception("知乎热搜列表为空")

    hot_search_str = "✨=====知乎热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_search_str += f"{i + 1}. {hot_search.get('target', {}).get('title', '')}\n"
    return hot_search_str


def get_zhihu_hot_response_json() -> Dict:
    response: requests.Response
    try:
        # url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
        url = "https://api.zhihu.com/topstory/hot-list?limit=10"
        response = requests.get(url, timeout=10)
    except Exception as e:
        raise Exception(f"请求知乎热搜API失败, 错误信息: {str(e)}")

    if response.status_code != 200:
        raise Exception(f"知乎热搜API返回非200状态码, 状态码: {response.status_code}")

    try:
        return response.json()
    except Exception as e:
        raise Exception(f"解析知乎热搜API返回的JSON失败, 错误信息: {str(e)}")
