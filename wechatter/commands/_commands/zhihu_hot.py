from typing import Dict, List

from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.message import SendTo
from wechatter.sender import sender
from wechatter.utils import get_request_json


@command(
    command="zhihu-hot",
    keys=["知乎热搜", "zhihu-hot"],
    desc="获取知乎热搜。",
)
def zhihu_hot_command_handler(to: SendTo, message: str = "") -> None:
    try:
        result = get_zhihu_hot_str()
    except Exception as e:
        error_message = f"获取知乎热搜失败，错误信息: {str(e)}"
        logger.error(error_message)
        sender.send_msg(to, error_message)
    else:
        sender.send_msg(to, result)


def get_zhihu_hot_str() -> str:
    response = get_request_json(url="https://api.zhihu.com/topstory/hot-list?limit=10")
    hot_list = _extract_zhihu_hot_data(response)
    return _generate_zhihu_hot_message(hot_list)


def _extract_zhihu_hot_data(r_json: Dict) -> List:
    try:
        hot_list = r_json["data"]
    except (KeyError, TypeError) as e:
        logger.error("解析知乎热搜返回数据失败")
        raise RuntimeError("解析知乎热搜返回数据失败") from e
    return hot_list


def _generate_zhihu_hot_message(hot_list: List) -> str:
    if not hot_list:
        return "暂无知乎热搜"

    hot_search_str = "✨=====知乎热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_search_str += f"{i + 1}. {hot_search.get('target', {}).get('title', '')}\n"

    return hot_search_str
