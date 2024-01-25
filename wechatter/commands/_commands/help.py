# 获取命令帮助消息
from wechatter.commands import commands
from wechatter.commands.handlers import command
from wechatter.models.message import SendTo
from wechatter.sender import Sender
from wechatter.utils.text_to_image import text_to_image


@command(command="help", keys=["帮助", "help"], desc="获取帮助信息。", value=10)
def help_command_handler(to: SendTo, message: str = "") -> None:
    # # 获取帮助信息(文本)
    # from command.help import get_help_msg
    # response = get_help_msg()

    # 获取帮助信息(图片)

    help_msg = get_help_msg()
    response = text_to_image(help_msg)
    if response:
        Sender.send_localfile_msg(to, response)


def get_help_msg() -> str:
    help_msg = "=====帮助信息=====\n"
    for value in commands.values():
        if value["value"] == 0:
            continue
        cmd_msg = ""
        for key in value["keys"]:
            cmd_msg += "/" + key + "\n"
        help_msg += cmd_msg + "-->「" + value["desc"] + "」\n\n"
    return help_msg
