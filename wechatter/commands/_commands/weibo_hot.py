# 获取微博热搜命令
from typing import Dict

import requests

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender


@command(
    command="weibo-hot",
    keys=["微博热搜", "weibo-hot"],
    desc="获取微博热搜。",
    value=130,
)
def weibo_hot_command_handler(to: SendTo, message: str = "") -> None:
    try:
        response = get_weibo_hot_str()
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))
    except Exception as e:
        error_message = f"获取微博热搜失败，错误信息: {str(e)}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_weibo_hot_str() -> str:
    try:
        hot_list = (
            get_weibo_hot_response_json()
            .get("data")
            .get("cards")[0]
            .get("card_group")[:20]
        )
    except Exception as e:
        raise Exception(f"解析微博热搜列表失败, 错误信息: {str(e)}")

    if not hot_list:
        raise Exception("微博热搜列表为空")

    hot_search_str = "✨=====微博热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_search_str += f"{i + 1}. {hot_search.get('desc')}\n"
    return hot_search_str


def get_weibo_hot_response_json() -> Dict:
    response: requests.Response
    try:
        url = "https://m.weibo.cn/api/container/getIndex?containerid=106003%26filter_type%3Drealtimehot"
        response = requests.get(url, timeout=10)
    except Exception as e:
        raise Exception(f"请求微博热搜API失败, 错误信息: {str(e)}")

    if response.status_code != 200:
        raise Exception(f"微博热搜API返回非200状态码, 状态码: {response.status_code}")

    try:
        return response.json()
    except Exception as e:
        raise Exception(f"解析微博热搜API返回的JSON失败, 错误信息: {str(e)}")
