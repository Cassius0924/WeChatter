from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender
from wechatter.utils import get_request_json


@command(
    command="zhihu-hot",
    keys=["知乎热搜", "zhihu-hot"],
    desc="获取知乎热搜。",
    value=140,
)
def zhihu_hot_command_handler(to: SendTo, message: str = "") -> None:
    try:
        response = get_zhihu_hot_str()
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))
    except Exception as e:
        error_message = f"获取知乎热搜失败，错误信息: {str(e)}"
        logger.error(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_zhihu_hot_str() -> str:
    r_json = get_request_json(url="https://api.zhihu.com/topstory/hot-list?limit=10")
    try:
        hot_list = r_json.get("data")
    except (ValueError, AttributeError):
        logger.error("解析知乎热搜返回数据失败")
        raise Exception("解析知乎热搜返回数据失败")

    if not hot_list:
        return "暂无热搜"

    hot_search_str = "✨=====知乎热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_search_str += f"{i + 1}. {hot_search.get('target', {}).get('title', '')}\n"
    return hot_search_str
