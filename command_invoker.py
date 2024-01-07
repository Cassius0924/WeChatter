# 命令调用器
from command.gpt_reply import reply_by_gpt35, reply_by_gpt4
from command.help import get_help_msg
from command.bili_hot import get_bili_hot_str
from command.zhihu_hot import get_zhihu_hot_str
from command.weibo_hot import get_weibo_hot_str
from command.translate import (
    get_reverso_context_tran_str,
    detect_lang,
    check_lang_support,
)
from command.github_trending import get_github_trending_str
from command.douyin_hot import get_douyin_hot_str
from command.pai_post import get_pai_post_str
from command.today_in_history import get_today_in_history_str
from send_msg import SendMessage, SendMessageType, SendTo, Sender


class CommandInvoker:
    def __init__(self) -> None:
        pass

    # 封装发送文本消息
    @staticmethod
    def _send_text_msg(to: SendTo, message: str) -> None:
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, message))

    # 命令：/help
    @staticmethod
    def cmd_help(to: SendTo) -> None:
        response = get_help_msg()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/gpt
    @staticmethod
    def cmd_gpt35(to: SendTo, message: str) -> None:
        response = reply_by_gpt35(message)
        CommandInvoker._send_text_msg(to, response)

    # 命令：/gpt4
    @staticmethod
    def cmd_gpt4(to: SendTo, message: str) -> None:
        response = reply_by_gpt4(message)
        CommandInvoker._send_text_msg(to, response)

    # 命令：/bili-hot
    @staticmethod
    def cmd_bili_hot(to: SendTo) -> None:
        response = get_bili_hot_str()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/zhihu-hot
    @staticmethod
    def cmd_zhihu_hot(to: SendTo) -> None:
        response = get_zhihu_hot_str()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/weibo-hot
    @staticmethod
    def cmd_weibo_hot(to: SendTo) -> None:
        response = get_weibo_hot_str()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/word
    # TODO: 改成解释单词，不翻译
    @staticmethod
    def cmd_word(to: SendTo, message: str) -> None:
        # 检测文本语言
        from_lang = detect_lang(message)
        to_lang = "chinese"
        # en -> zh
        # zh -> en
        # other -> zh -> en
        if from_lang == "":
            response = "无法识别语言"
            CommandInvoker._send_text_msg(to, response)
            return
        if from_lang == "chinese":
            to_lang = "english"
        elif from_lang != "english" and not check_lang_support(from_lang, "chinese"):
            to_lang = "english"
        # 获取翻译
        response = get_reverso_context_tran_str(message, from_lang, to_lang)
        CommandInvoker._send_text_msg(to, response)

    # 命令：/tran
    @staticmethod
    def cmd_tran(to: SendTo, message: str) -> None:
        # 获取翻译
        response = "翻译功能暂未开放"
        CommandInvoker._send_text_msg(to, response)

    # 命令：/people-daily
    @staticmethod
    def cmd_people_daily(to: SendTo) -> None:
        # 获取人民日报
        response = "人民日报功能暂未开放"
        CommandInvoker._send_text_msg(to, response)

    # 命令：/today-in-history
    @staticmethod
    def cmd_today_in_history(to: SendTo) -> None:
        # 获取历史上的今天
        response = get_today_in_history_str()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/github-trending
    @staticmethod
    def cmd_github_trending(to: SendTo) -> None:
        response = get_github_trending_str()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/douyin-hot
    @staticmethod
    def cmd_douyin_hot(to: SendTo) -> None:
        response = get_douyin_hot_str()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/pai-post
    @staticmethod
    def cmd_pai_post(to: SendTo) -> None:
        response = get_pai_post_str()
        CommandInvoker._send_text_msg(to, response)
