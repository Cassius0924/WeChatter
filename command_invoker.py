# 命令调用器
import re

from command.bili_hot import get_bili_hot_str
from command.douyin_hot import get_douyin_hot_str
from command.github_trending import get_github_trending_str
from command.gpt_reply import reply_by_gpt4, reply_by_gpt35
from command.pai_post import get_pai_post_str
from command.qrcode import generate_qrcode
from command.today_in_history import get_today_in_history_str
from command.todo import add_todo_task, remove_todo_task, view_todos
from command.translate import (
    check_lang_support,
    detect_lang,
    get_reverso_context_tran_str,
)
from command.weibo_hot import get_weibo_hot_str
from command.zhihu_hot import get_zhihu_hot_str
from send_msg import Sender, SendMessage, SendMessageType, SendTo


class CommandInvoker:
    """命令调用器"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def _send_text_msg(to: SendTo, message: str = "") -> None:
        """封装发送文本消息"""
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, message))

    # 命令：/help
    @staticmethod
    def cmd_help(to: SendTo, message: str = "") -> None:
        from command.help import get_help_msg
        response = get_help_msg()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/gpt
    @staticmethod
    def cmd_gpt35(to: SendTo, message: str = "") -> None:
        response = reply_by_gpt35(message)
        CommandInvoker._send_text_msg(to, response)

    # 命令：/gpt4
    @staticmethod
    def cmd_gpt4(to: SendTo, message: str = "") -> None:
        response = reply_by_gpt4(message)
        CommandInvoker._send_text_msg(to, response)

    # 命令：/bili-hot
    @staticmethod
    def cmd_bili_hot(to: SendTo, message: str = "") -> None:
        response = get_bili_hot_str()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/zhihu-hot
    @staticmethod
    def cmd_zhihu_hot(to: SendTo, message: str = "") -> None:
        response = get_zhihu_hot_str()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/weibo-hot
    @staticmethod
    def cmd_weibo_hot(to: SendTo, message: str = "") -> None:
        response = get_weibo_hot_str()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/word
    # TODO: 改成解释单词，不翻译
    @staticmethod
    def cmd_word(to: SendTo, message: str = "") -> None:
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
    def cmd_tran(to: SendTo, message: str = "") -> None:
        # 获取翻译
        response = "翻译功能暂未开放"
        CommandInvoker._send_text_msg(to, response)

    # 命令：/people-daily
    @staticmethod
    def cmd_people_daily(to: SendTo, message: str = "") -> None:
        # 获取人民日报
        response = "人民日报功能暂未开放"
        CommandInvoker._send_text_msg(to, response)

    # 命令：/today-in-history
    @staticmethod
    def cmd_today_in_history(to: SendTo, message: str = "") -> None:
        # 获取历史上的今天
        response = get_today_in_history_str()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/github-trending
    @staticmethod
    def cmd_github_trending(to: SendTo, message: str = "") -> None:
        response = get_github_trending_str()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/douyin-hot
    @staticmethod
    def cmd_douyin_hot(to: SendTo, message: str = "") -> None:
        response = get_douyin_hot_str()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/pai-post
    @staticmethod
    def cmd_pai_post(to: SendTo, message: str = "") -> None:
        response = get_pai_post_str()
        CommandInvoker._send_text_msg(to, response)

    # 命令：/qrcode
    @staticmethod
    def cmd_qrcode(to: SendTo, message: str = "") -> None:
        # 获取二维码
        response = generate_qrcode(message)
        Sender.send_localfile_msg(to, response)

    # 命令：/todo
    @staticmethod
    def cmd_todo(to: SendTo, message: str = "") -> None:
        # 判断是查询还是添加
        if message == "":
            # 获取待办事项
            result = view_todos(to.p_id, to.p_name)
            CommandInvoker._send_text_msg(to, result)
        else:
            # 添加待办事项
            add_success = add_todo_task(to.p_id, message)
            if add_success:
                result = view_todos(to.p_id, to.p_name)
                CommandInvoker._send_text_msg(to, result)
            else:
                CommandInvoker._send_text_msg(to, "添加失败")

    # 命令：/rmtd
    @staticmethod
    def cmd_remove_todo(to: SendTo, message: str = "") -> None:
        indices = [
            int(idx.strip()) - 1
            for idx in re.split(r"[\s,]+", message)
            if idx.strip().isdigit()
        ]
        if not indices:
            CommandInvoker._send_text_msg(to, "请输入有效数字来删除待办事项")
            return

        remove_result = remove_todo_task(to.p_id, indices)
        CommandInvoker._send_text_msg(to, remove_result)
        result = view_todos(to.p_id, to.p_name)
        CommandInvoker._send_text_msg(to, result)
