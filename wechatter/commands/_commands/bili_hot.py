import json
from typing import Dict, List, Tuple, Union

from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.wechat import QuotedResponse, SendTo
from wechatter.sender import sender
from wechatter.utils import get_request_json, url_encode

COMMAND_NAME = "bili-hot"


# TODO: 所有的handler代码逻辑都一样，可以尝试优化为一个函数，都调用各自的mainfunc
@command(
    command=COMMAND_NAME,
    keys=["b站热搜", "bili-hot"],
    desc="获取b站热搜。",
)
def bili_hot_command_handler(to: Union[SendTo, str], message: str = ""):
    try:
        result, q_response = get_bili_hot_str()
    except Exception as e:
        error_message = f"获取Bilibili热搜失败，错误信息: {str(e)}"
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


@bili_hot_command_handler.quoted_handler
def bili_hot_quoted_handler(to: SendTo, message: str = "", q_response: str = ""):
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


@bili_hot_command_handler.mainfunc
def get_bili_hot_str() -> Tuple[str, str]:
    response = get_request_json(
        url="https://app.bilibili.com/x/v2/search/trending/ranking"
    )
    hot_list = _extract_bili_hot_data(response)
    return (
        _generate_bili_hot_message(hot_list),
        _generate_bili_hot_quoted_response(hot_list),
    )


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

    # TODO: 写一个generate_message的框架函数，统一处理消息的格式，确保消息格式统一。
    hot_str = "✨=====Bilibili热搜=====✨\n"
    for i, hot_search in enumerate(hot_list):
        hot_str += f"{i + 1}. {hot_search.get('keyword')}\n"

    return hot_str


def _generate_bili_hot_quoted_response(hot_list: List) -> str:
    search_api = "https://search.bilibili.com/all?keyword=%s"
    result = {}
    for i, hot_search in enumerate(hot_list):
        keyword = hot_search.get("keyword", None)
        if keyword:
            result[str(i + 1)] = url_encode(search_api % keyword)
    return json.dumps(result)
