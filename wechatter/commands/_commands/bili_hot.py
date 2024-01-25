# b站热搜命令
import requests

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender


@command(
    command="bili-hot", keys=["b站热搜", "bili-hot"], desc="获取b站热搜。", value=20
)
def cmd_bili_hot(to: SendTo, message: str = "") -> None:
    response = get_bili_hot_str()
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))


def get_bili_hot_str() -> str:
    hot_list = get_bili_hot_list()
    if hot_list == []:
        return "获取b站热搜失败"
    hot_str = "✨=====b站热搜=====✨\n"
    for i, hot_search in enumerate(hot_list):
        hot_str += f"{i + 1}. {hot_search.get('keyword')}\n"
    return hot_str


def get_bili_hot_list() -> list:
    response: requests.Response
    try:
        url = "https://app.bilibili.com/x/v2/search/trending/ranking"
        response = requests.get(url, timeout=10)
    except Exception:
        print("请求b站热搜失败")
        return []

    if response.status_code != 200:
        print("获取b站热搜失败")
        return []
    hot_list = response.json()
    return hot_list.get("data", {}).get("list", [])
