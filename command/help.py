# 获取命令帮助消息
from command.command_set import cmd_dict


def get_help_msg() -> str:
    help_msg = "=====帮助信息=====\n"
    for value in cmd_dict.values():
        if value["value"] == 0:
            continue
        cmd_msg = ""
        for key in value["keys"]:
            cmd_msg += "/" + key + "\n"
        help_msg += cmd_msg + "-->「" + value["desc"] + "」\n\n"
    return help_msg
