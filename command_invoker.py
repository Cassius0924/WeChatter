from command.gpt_reply import reply_by_gpt35, reply_by_gpt4
from command.help import get_help_msg
from command.bili_hot import get_bili_hot_str
from send_msg import send_text_msg, send_file_msg, send_image_msg


class CommandInvoker:
    def __init__(self) -> None:
        pass

    # 命令：/help
    @staticmethod
    def cmd_help(to_user_name: str) -> None:
        send_text_msg(get_help_msg(), to_user_name)
        pass

    # 命令：/gpt
    @staticmethod
    def cmd_gpt35(message: str, to_user_name: str) -> None:
        # 获取 gpt3.5 回复
        send_text_msg(reply_by_gpt35(message), to_user_name)

    # 命令：/gpt4
    @staticmethod
    def cmd_gpt4(message: str, to_user_name: str) -> None:
        send_text_msg(reply_by_gpt4(message), to_user_name)

    # 命令：/bili-hot
    @staticmethod
    def cmd_bili_hot(to_user_name: str) -> None:
        send_text_msg(get_bili_hot_str(), to_user_name)

    # 命令：/zhihu-hot
    @staticmethod
    def cmd_zhihu_hot(to_user_name: str) -> None:
        send_text_msg("get_zhihu_hot_str()", to_user_name)

    # 命令：/weibo-hot
    @staticmethod
    def cmd_weibo_hot(to_user_name: str) -> None:
        pass

    # 命令：/












