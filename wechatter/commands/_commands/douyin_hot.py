import json
from typing import Dict, List, Tuple, Union

from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.wechat import QuotedResponse, SendTo
from wechatter.sender import sender
from wechatter.utils import get_request_json, url_encode

COMMAND_NAME = "douyin-hot"


@command(
    command=COMMAND_NAME,
    keys=["抖音热搜", "douyin-hot"],
    desc="获取抖音热搜。",
)
def douyin_hot_command_handler(to: Union[str, SendTo], message: str = "") -> None:
    try:
        result, q_response = get_douyin_hot_str()
    except Exception as e:
        error_message = f"获取抖音热搜失败，错误信息: {str(e)}"
        logger.error(error_message)
        sender.send_msg(to, error_message)
    else:
        sender.send_msg(
            to,
            result,
            quoted_response=QuotedResponse(
                command=COMMAND_NAME,
                response=q_response,
            ),
        )


@douyin_hot_command_handler.quoted_handler
def douyin_hot_quoted_handler(
    to: SendTo, message: str = "", q_response: str = ""
) -> None:
    if not message.isdigit():
        logger.error("输入的热搜编号不是数字")
        sender.send_msg(to, "请输入热搜编号")
        return

    hot_url_dict = json.loads(q_response)
    try:
        hot_url = hot_url_dict[message]
    except Exception:
        logger.error("输入的热搜编号错误")
        sender.send_msg(to, "输入的热搜编号错误")
        return
    else:
        sender.send_msg(to, hot_url)


@douyin_hot_command_handler.mainfunc
def get_douyin_hot_str() -> Tuple[str, str]:
    r_json = get_request_json(
        url="https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
    )
    hot_list = _extract_douyin_hot_data(r_json)
    return (
        _generate_douyin_hot_message(hot_list),
        _generate_douyin_hot_quoted_response(hot_list),
    )


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


def _generate_douyin_hot_quoted_response(hot_list: List) -> str:
    search_api = "https://www.douyin.com/search/%s"
    hot_url_dict = {}
    for i, hot_search in enumerate(hot_list[:20]):
        keyword = hot_search.get("word", None)
        if keyword:
            hot_url_dict[str(i + 1)] = url_encode(search_api % keyword)
    return json.dumps(hot_url_dict)
