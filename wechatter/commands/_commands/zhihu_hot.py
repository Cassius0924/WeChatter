import json
from typing import Dict, List, Tuple, Union

from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.wechat import QuotedResponse, SendTo
from wechatter.sender import sender
from wechatter.utils import get_request_json

COMMAND_NAME = "zhihu-hot"


@command(
    command=COMMAND_NAME,
    keys=["知乎热搜", "zhihu-hot"],
    desc="获取知乎热搜。",
)
def zhihu_hot_command_handler(to: Union[str, SendTo], message: str = "") -> None:
    try:
        result, q_response = get_zhihu_hot_str()
    except Exception as e:
        error_message = f"获取知乎热搜失败，错误信息: {str(e)}"
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


@zhihu_hot_command_handler.quoted_handler
def zhihu_hot_quoted_handler(
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


@zhihu_hot_command_handler.mainfunc
def get_zhihu_hot_str() -> Tuple[str, str]:
    response = get_request_json(url="https://api.zhihu.com/topstory/hot-list?limit=10")
    hot_list = _extract_zhihu_hot_data(response)
    return (
        _generate_zhihu_hot_message(hot_list),
        _generate_zhihu_hot_quoted_response(hot_list),
    )


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


def _generate_zhihu_hot_quoted_response(hot_list: List) -> str:
    hot_url_dict = {}
    for i, hot_search in enumerate(hot_list[:20]):
        url = hot_search.get("target", {}).get("url", "")
        hot_url_dict[str(i + 1)] = url.replace("api", "www", 1).replace(
            "questions", "question", 1
        )

    return json.dumps(hot_url_dict)
