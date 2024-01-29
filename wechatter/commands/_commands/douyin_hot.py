# 抖音热搜命令
from typing import Dict

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
    try:
        response = get_douyin_hot_str()
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))
    except Exception as e:
        error_message = f"获取抖音热搜失败，错误信息: {str(e)}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_douyin_hot_str() -> str:
    try:
        hot_list = get_douyin_hot_response_json().get("word_list")
    except Exception as e:
        raise Exception(f"解析抖音热搜列表失败, 错误信息: {str(e)}")

    if not hot_list:
        raise Exception("抖音热搜列表为空")

    hot_str = "✨=====抖音热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_str += f"{i + 1}.  {hot_search.get('word')}\n"

    return hot_str


def get_douyin_hot_response_json() -> Dict:
    response: requests.Response
    try:
        url = "https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
        response = requests.get(url, timeout=10)
    except Exception as e:
        raise Exception(f"请求抖音热搜API失败, 错误信息: {str(e)}")

    if response.status_code != 200:
        raise Exception(f"抖音热搜API返回非200状态码, 状态码: {response.status_code}")

    try:
        return response.json()
    except Exception as e:
        raise Exception(f"解析抖音热搜API返回的JSON失败, 错误信息: {str(e)}")
