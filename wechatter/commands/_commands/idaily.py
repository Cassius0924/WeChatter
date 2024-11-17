from typing import Dict, Union

from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.wechat import SendTo
from wechatter.sender import sender
from wechatter.utils import get_request_json
from wechatter.utils.time import get_current_bdy, get_yesterday_bdy


@command(
    command="idaily",
    keys=["每日环球视野", "idaily"],
    desc="获取每日环球视野。",
)
def idaily_command_handler(to: Union[str, SendTo], message: str = "") -> None:
    # 获取每日环球视野
    try:
        result = get_idaily_str()
    except Exception as e:
        error_message = f"获取每日环球视野失败，错误信息：{str(e)}"
        logger.error(error_message)
        sender.send_msg(to, error_message)
    else:
        sender.send_msg(to, result)


@idaily_command_handler.mainfunc
def get_idaily_str() -> str:
    response = get_request_json(url="https://idaily-cdn.idailycdn.com/api/list/v3/iphone")
    tih_list = _extract_idaily_data(response)
    return _generate_idaily_message(tih_list)


def _extract_idaily_data(r_json: Dict) -> dict:
    try:
        tih_list = r_json
    except (KeyError, TypeError) as e:
        logger.error("解析每日环球视野API返回的JSON失败")
        raise RuntimeError("解析每日环球视野API返回的JSON失败") from e
    return tih_list


def _generate_idaily_message(tih_list: dict) -> str:
    if not tih_list:
        return "暂无每日环球视野"

    idaily_str = ["✨=====每日环球视野=====✨"]
    content_list = []
    today = get_current_bdy()
    yesterday = get_yesterday_bdy()
    today_has_idaily = False

    def format_entry(index, entry):
        title = entry['title_wechat_tml'].split(" - ")[0]
        content = entry['content']
        return f"{index + 1}. 🌎 {title}\n    🌪️ {content}"

    for index, entry in enumerate(tih_list):
        if entry["pubdate"] == str(today):
            today_has_idaily = True
            content_list.append(format_entry(index, entry))
        elif not today_has_idaily and entry["pubdate"] == str(yesterday):
            content_list.append(format_entry(index, entry))

    if today_has_idaily:
        idaily_str.append(f"🗓️ 今天是 {today}")
    else:
        idaily_str.append("今天的iDaily还没更新，现在为您呈现的是：")
        idaily_str.append(f"🗓️ 时间: {yesterday}")

    idaily_str.extend(content_list)
    return "\n".join(idaily_str)


# def _generate_idaily_message(tih_list: dict) -> str:
#     if not tih_list:
#         return "暂无每日环球视野"
# 
#     idaily_str = "✨=====每日环球视野=====✨\n"
#     this_str = ""
#     _today = get_current_bdy()
#     today_has_idaily = False
# 
#     _yesterday = get_yesterday_bdy()
#     for i in range(len(tih_list)):
#         if tih_list[i]["pubdate"] == str(_today):
#             today_has_idaily = True
#             title_wechat_tml = tih_list[i]['title_wechat_tml'].split(" - ")[0]
#             this_str += (
#                 f"{i + 1}. 🌎 {title_wechat_tml}\n"
#                 f"    🌪️ {tih_list[i]['content']}\n"
#             )
#         if not today_has_idaily:
#             if tih_list[i]["pubdate"] == str(_yesterday):
#                 title_wechat_tml = tih_list[i]['title_wechat_tml'].split(" - ")[0]
#                 this_str += (
#                     f"{i + 1}. 🌎 {title_wechat_tml}\n"
#                     f"    🌪️ {tih_list[i]['content']}\n"
#                 )
#     if today_has_idaily:
#         idaily_str += "🗓️ 今天是" + _today + "\n"
#     else:
#         idaily_str += "今天的iDaily还没更新，现在为您呈现的是：\n"
#         idaily_str += "🗓️ 时间: " + _yesterday + "\n"
#     idaily_str += this_str
#     return idaily_str


if __name__ == '__main__':
    print(get_idaily_str())
