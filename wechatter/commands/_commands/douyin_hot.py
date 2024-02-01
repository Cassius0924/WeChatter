from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender
from wechatter.utils import get_request_json


@command(
    command="douyin-hot",
    keys=["抖音热搜", "douyin-hot"],
    desc="获取抖音热搜。",
    value=50,
)
def douyin_hot_command_handler(to: SendTo, message: str = "") -> None:
    try:
        response = get_douyin_hot_str()
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))
    except Exception as e:
        error_message = f"获取抖音热搜失败，错误信息: {str(e)}"
        logger.error(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_douyin_hot_str() -> str:
    r_json = get_request_json(
        url="https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
    )
    try:
        hot_list = r_json.get("word_list")
    except (ValueError, AttributeError):
        logger.error("解析抖音热搜列表失败")
        raise Exception("解析抖音热搜列表失败")

    if not hot_list:
        return "暂无热搜"

    hot_str = "✨=====抖音热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_str += f"{i + 1}.  {hot_search.get('word')}\n"

    return hot_str
