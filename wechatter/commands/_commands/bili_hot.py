# b站热搜命令
from typing import Dict
import requests

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender


@command(
    command="bili-hot", keys=["b站热搜", "bili-hot"], desc="获取b站热搜。", value=20
)
def cmd_bili_hot(to: SendTo, message: str = "") -> None:
    try:
        response = get_bili_hot_str()
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))
    except Exception as e:
        error_message = f"获取b站热搜失败，错误信息: {str(e)}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_bili_hot_str() -> str:
    try:
        hot_list = get_bili_hot_response_json().get("data").get("list")
    except Exception as e:
        raise Exception(f"解析b站热搜列表失败, 错误信息: {str(e)}")

    if not hot_list:
        raise Exception("b站热搜列表为空")

    hot_str = "✨=====b站热搜=====✨\n"
    for i, hot_search in enumerate(hot_list):
        hot_str += f"{i + 1}. {hot_search.get('keyword')}\n"

    return hot_str


def get_bili_hot_response_json() -> Dict:
    response: requests.Response
    try:
        url = "https://app.bilibili.com/x/v2/search/trending/ranking"
        response = requests.get(url, timeout=10)
    except Exception as e:
        raise Exception(f"请求b站热搜API失败, 错误信息: {str(e)}")

    if response.status_code != 200:
        raise Exception(f"b站热搜API返回非200状态码, 状态码: {response.status_code}")

    try:
        return response.json()
    except Exception as e:
        raise Exception(f"解析b站热搜API返回的JSON失败, 错误信息: {str(e)}")
