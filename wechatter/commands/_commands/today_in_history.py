from typing import List

import requests

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender


@command(
    command="today-in-history",
    keys=["历史上的今天", "today-in-history", "t-i-h"],
    desc="获取历史上的今天。",
    value=100,
)
def today_in_history_command_handler(to: SendTo, message: str = "") -> None:
    # 获取历史上的今天
    try:
        response = get_today_in_history_str()
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))
    except Exception as e:
        error_message = f"获取历史上的今天失败，错误信息：{e}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_today_in_history_str() -> str:
    try:
        tih_response = get_today_in_history_response_json()
        tih_list = tih_response.get("data")
    except Exception as e:
        raise Exception(f"解析历史上的今天列表失败，错误信息：{e}")

    if not tih_list:
        raise Exception("历史上的今天列表为空")

    today_in_history_str = "✨=====历史上的今天=====✨\n"
    for i, today_in_history in enumerate(tih_list):
        today_in_history_str += (
            f"{i + 1}. 🗓️ {today_in_history.get('year')} 年\n"
            f"    🌎 {today_in_history.get('title')}\n"
            f"    🌪️ {today_in_history.get('desc')}\n"
        )

    return today_in_history_str


def get_today_in_history_response_json() -> List:
    response: requests.Response
    try:
        url = "https://60s-view.deno.dev/history"
        response = requests.get(url, timeout=10)
    except Exception as e:
        raise Exception(f"请求历史上的今天API失败，错误信息：{e}")

    if response.status_code != 200:
        raise Exception(f"历史上的今天API返回非200状态码：{response.status_code}")

    return response.json()
