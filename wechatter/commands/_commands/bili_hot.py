from typing import Dict, List

from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.message import SendTo
from wechatter.sender import sender
from wechatter.utils import get_request_json


@command(
    command="bili-hot",
    keys=["b站热搜", "bili-hot"],
    desc="获取b站热搜。",
)
def bili_hot_command_handler(to: SendTo, message: str = "") -> None:
    try:
        result = get_bili_hot_str()
    except Exception as e:
        error_message = f"获取Bilibili热搜失败，错误信息: {str(e)}"
        logger.error(error_message)
        sender.send_msg(to, error_message)
    else:
        sender.send_msg(to, result)


def get_bili_hot_str() -> str:
    response = get_request_json(
        url="https://app.bilibili.com/x/v2/search/trending/ranking"
    )
    hot_list = _extract_bili_hot_data(response)
    return _generate_bili_hot_message(hot_list)


def _extract_bili_hot_data(r_json: Dict) -> List:
    try:
        hot_list = r_json["data"]["list"]
    except (KeyError, TypeError) as e:
        logger.error("解析Bilibili热搜API返回的JSON失败")
        raise RuntimeError("解析Bilibili热搜API返回的JSON失败") from e
    return hot_list


def _generate_bili_hot_message(hot_list: List) -> str:
    if not hot_list:
        return "暂无Bilibili热搜"

    hot_str = "✨=====Bilibili热搜=====✨\n"
    for i, hot_search in enumerate(hot_list):
        hot_str += f"{i + 1}. {hot_search.get('keyword')}\n"

    return hot_str
