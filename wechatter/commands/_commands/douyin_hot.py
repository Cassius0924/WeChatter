from typing import Dict, List

from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.wechat import SendTo
from wechatter.sender import sender
from wechatter.utils import get_request_json


@command(
    command="douyin-hot",
    keys=["抖音热搜", "douyin-hot"],
    desc="获取抖音热搜。",
)
def douyin_hot_command_handler(to: SendTo, message: str = "") -> None:
    try:
        result = get_douyin_hot_str()
    except Exception as e:
        error_message = f"获取抖音热搜失败，错误信息: {str(e)}"
        logger.error(error_message)
        sender.send_msg(to, error_message)
    else:
        sender.send_msg(to, result)


def get_douyin_hot_str() -> str:
    r_json = get_request_json(
        url="https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
    )
    hot_list = _extract_douyin_hot_data(r_json)
    return _generate_douyin_hot_message(hot_list)


def _extract_douyin_hot_data(r_json: Dict) -> List:
    try:
        hot_list = r_json["word_list"]
    except (KeyError, TypeError) as e:
        logger.error("解析抖音热搜列表失败")
        raise RuntimeError("解析抖音热搜列表失败") from e
    return hot_list


def _generate_douyin_hot_message(hot_list: List) -> str:
    if not hot_list:
        return "暂无抖音热搜"

    hot_str = "✨=====抖音热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_str += f"{i + 1}.  {hot_search.get('word')}\n"

    return hot_str
