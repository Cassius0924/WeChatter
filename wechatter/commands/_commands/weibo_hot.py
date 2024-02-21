import json
from typing import Dict, List, Tuple, Union

from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.wechat import QuotedResponse, SendTo
from wechatter.sender import sender
from wechatter.utils import get_request_json, url_encode

COMMAND_NAME = "weibo-hot"


@command(
    command=COMMAND_NAME,
    keys=["微博热搜", "weibo-hot"],
    desc="获取微博热搜。",
)
def weibo_hot_command_handler(to: Union[str, SendTo], message: str = "") -> None:
    try:
        result, q_response = get_weibo_hot_str()
    except Exception as e:
        error_message = f"获取微博热搜失败，错误信息: {str(e)}"
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


@weibo_hot_command_handler.quoted_handler
def weibo_hot_quoted_handler(to: SendTo, message: str = "", q_response: str = ""):
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


@weibo_hot_command_handler.mainfunc
def get_weibo_hot_str() -> Tuple[str, str]:
    r_json = get_request_json(
        url="https://m.weibo.cn/api/container/getIndex?containerid=106003%26filter_type%3Drealtimehot"
    )
    hot_list = _extract_weibo_hot_data(r_json)
    return (
        _generate_weibo_hot_message(hot_list),
        _generate_weibo_hot_quoted_response(hot_list),
    )


def _extract_weibo_hot_data(r_json: Dict) -> List:
    try:
        hot_list = r_json["data"]["cards"][0]["card_group"][:20]
    except (KeyError, TypeError) as e:
        logger.error("微博列表返回值格式错误")
        raise RuntimeError("微博列表返回值格式错误") from e
    return hot_list


def _generate_weibo_hot_message(hot_list: List) -> str:
    if not hot_list:
        return "微博热搜列表为空"

    hot_search_str = "✨=====微博热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_search_str += f"{i + 1}. {hot_search.get('desc')}\n"

    return hot_search_str


def _generate_weibo_hot_quoted_response(hot_list: List) -> str:
    result = {}
    search_url = "https://s.weibo.com/weibo?q=%s"
    for i, hot_search in enumerate(hot_list):
        keyword = hot_search.get("desc", None)
        if keyword:
            result[str(i + 1)] = search_url % url_encode(keyword)
    return json.dumps(result)
