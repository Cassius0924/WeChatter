# 命令调用器
from command.gpt_reply import reply_by_gpt35, reply_by_gpt4
from command.help import get_help_msg
from command.bili_hot import get_bili_hot_str
from command.zhihu_hot import get_zhihu_hot_str
from command.weibo_hot import get_weibo_hot_str
from command.transalte import (
    get_reverso_context_tran_str,
    detect_lang,
    check_lang_support,
)
from command.github_trending import get_github_trending_str
from command.douyin_hot import get_douyin_hot_str
from command.pai_post import get_pai_post_str
from command.today_in_history import get_today_in_history_str
from send_msg import send_text_msg, send_file_msg, send_image_msg


class CommandInvoker:
    def __init__(self) -> None:
        pass

    # 命令：/help
    @staticmethod
    def cmd_help(to_user_name: str) -> None:
        send_text_msg(get_help_msg(), to_user_name)

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
        send_text_msg(get_zhihu_hot_str(), to_user_name)

    # 命令：/weibo-hot
    @staticmethod
    def cmd_weibo_hot(to_user_name: str) -> None:
        send_text_msg(get_weibo_hot_str(), to_user_name)

    # 命令：/word
    # TODO: 改成解释单词，不翻译
    @staticmethod
    def cmd_word(message: str, to_user_name: str) -> None:
        # 检测文本语言
        from_lang = detect_lang(message)
        to_lang = "chinese"
        # en -> zh
        # zh -> en
        # other -> zh -> en
        if from_lang == "":
            send_text_msg("无法检测文本语言", to_user_name)
            return
        if from_lang == "chinese":
            to_lang = "english"
        elif from_lang != "english" and not check_lang_support(from_lang, "chinese"):
            to_lang = "english"
        # 获取翻译
        result = get_reverso_context_tran_str(message, from_lang, to_lang)
        send_text_msg(result, to_user_name)

    # 命令：/tran
    @staticmethod
    def cmd_tran(message: str, to_user_name: str) -> None:
        # 获取翻译
        send_text_msg("翻译功能暂未开放", to_user_name)

    # 命令：/people-daily
    @staticmethod
    def cmd_people_daily(to_user_name: str) -> None:
        # 获取人民日报
        send_text_msg("人民日报功能暂未开放", to_user_name)

    # 命令：/today-in-history
    @staticmethod
    def cmd_today_in_history(to_user_name: str) -> None:
        # 获取历史上的今天
        send_text_msg(get_today_in_history_str(), to_user_name)

    # 命令：/github-trending
    @staticmethod
    def cmd_github_trending(to_user_name: str) -> None:
        send_text_msg(get_github_trending_str(), to_user_name)

    # 命令：/douyin-hot
    @staticmethod
    def cmd_douyin_hot(to_user_name: str) -> None:
        send_text_msg(get_douyin_hot_str(), to_user_name)

    # 命令：/pai-post
    @staticmethod
    def cmd_pai_post(to_user_name: str) -> None:
        send_text_msg(get_pai_post_str(), to_user_name)


