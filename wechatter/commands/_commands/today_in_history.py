from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender
from wechatter.utils import get_request_json


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
        logger.error(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_today_in_history_str() -> str:
    tih_response = get_request_json(url="https://60s-view.deno.dev/history")
    try:
        tih_list = tih_response.get("data")
    except ValueError:
        raise ValueError("获取的历史上的今天数据格式错误")

    if not tih_list:
        return []

    today_in_history_str = "✨=====历史上的今天=====✨\n"
    for i, today_in_history in enumerate(tih_list):
        today_in_history_str += (
            f"{i + 1}. 🗓️ {today_in_history.get('year')} 年\n"
            f"    🌎 {today_in_history.get('title')}\n"
            f"    🌪️ {today_in_history.get('desc')}\n"
        )

    return today_in_history_str
