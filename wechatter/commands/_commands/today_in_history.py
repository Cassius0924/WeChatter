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
    response = get_today_in_history_str()
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))


def get_today_in_history_str() -> str:
    today_in_history_list = get_today_in_history_list()
    if today_in_history_list == []:
        return "获取历史上的今天失败"

    today_in_history_str = "✨=====历史上的今天=====✨\n"
    for i, today_in_history in enumerate(today_in_history_list):
        today_in_history_str += (
            f"{i + 1}. 🗓️ {today_in_history.get('year')}\n"
            f"    🌎 {today_in_history.get('title')}\n"
            f"    🌪️ {today_in_history.get('desc')}\n"
        )
    return today_in_history_str


def get_today_in_history_list() -> List:
    response: requests.Response
    try:
        url = "https://60s-view.deno.dev/history"
        response = requests.get(url, timeout=10)
    except Exception:
        print("请求历史上的今天失败")
        return []

    if response.status_code != 200:
        print("获取历史上的今天失败")
        return []
    today_in_history_list = response.json()
    return today_in_history_list.get("data", [])
