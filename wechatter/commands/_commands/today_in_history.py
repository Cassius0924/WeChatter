from typing import Dict, List

from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.wechat import SendTo
from wechatter.sender import sender
from wechatter.utils import get_request_json


@command(
    command="today-in-history",
    keys=["历史上的今天", "today-in-history", "t-i-h"],
    desc="获取历史上的今天。",
)
def today_in_history_command_handler(to: SendTo, message: str = "") -> None:
    # 获取历史上的今天
    try:
        result = get_today_in_history_str()
    except Exception as e:
        error_message = f"获取历史上的今天失败，错误信息：{str(e)}"
        logger.error(error_message)
        sender.send_msg(to, error_message)
    else:
        sender.send_msg(to, result)


def get_today_in_history_str() -> str:
    response = get_request_json(url="https://60s-view.deno.dev/history")
    tih_list = _extract_today_in_history_data(response)
    return _generate_today_in_history_message(tih_list)


def _extract_today_in_history_data(r_json: Dict) -> List:
    try:
        tih_list = r_json["data"]
    except (KeyError, TypeError) as e:
        logger.error("解析历史上的今天API返回的JSON失败")
        raise RuntimeError("解析历史上的今天API返回的JSON失败") from e
    return tih_list


def _generate_today_in_history_message(tih_list: List) -> str:
    if not tih_list:
        return "暂无历史上的今天"

    today_in_history_str = "✨=====历史上的今天=====✨\n"
    for i, today_in_history in enumerate(tih_list):
        today_in_history_str += (
            f"{i + 1}. 🗓️ {today_in_history.get('year')} 年\n"
            f"    🌎 {today_in_history.get('title')}\n"
            f"    🌪️ {today_in_history.get('desc')}\n"
        )

    return today_in_history_str
