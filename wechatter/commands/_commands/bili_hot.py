# b站热搜命令
from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender
from wechatter.utils import get_request_json


@command(
    command="bili-hot", keys=["b站热搜", "bili-hot"], desc="获取b站热搜。", value=20
)
def cmd_bili_hot(to: SendTo, message: str = "") -> None:
    try:
        response = get_bili_hot_str()
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))
    except Exception as e:
        error_message = f"获取Bilibili热搜失败，错误信息: {str(e)}"
        logger.error(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_bili_hot_str() -> str:
    r_json = get_request_json(
        url="https://app.bilibili.com/x/v2/search/trending/ranking"
    )
    try:
        hot_list = r_json.get("data").get("list")
    except (AttributeError, KeyError):
        logger.error("解析Bilibili热搜API返回的JSON失败")
        raise Exception("解析Bilibili热搜API返回的JSON失败")

    if not hot_list:
        return "暂无热搜"

    hot_str = "✨=====b站热搜=====✨\n"
    for i, hot_search in enumerate(hot_list):
        hot_str += f"{i + 1}. {hot_search.get('keyword')}\n"

    return hot_str
