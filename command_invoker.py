# 命令调用器
import re

from command.bili_hot import get_bili_hot_str
from command.douyin_hot import get_douyin_hot_str
from command.github_trending import get_github_trending_str
from command.pai_post import get_pai_post_str
from command.paper_people import get_paper_people_pdf_url, get_paper_people_url
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
from command.copilot_gpt4 import CopilotGPT4
from utils.text_to_image import text_to_image


def _send_text_msg(to: SendTo, message: str = "") -> None:
    """封装发送文本消息"""
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, message))


def _send_file_url_msg(to: SendTo, message: str = "") -> None:
    """封装发送文件URL消息"""
    Sender.send_msg(to, SendMessage(SendMessageType.FILE_URL, message))


def _gptx(model: str, to: SendTo, message: str = "") -> None:
    wx_id = to.p_id
    # 获取文件夹下最新的对话记录
    chat_info = CopilotGPT4.get_chating_chat_info(wx_id, model)
    if message == "":  # /gpt4
        # 判断对话是否有效
        if chat_info is None or CopilotGPT4.is_chat_valid(chat_info):
            CopilotGPT4.create_chat(wx_id=wx_id, model=model)
            _send_text_msg(to, "创建新对话成功")
            return
        _send_text_msg(to, "对话未开始，继续上一次对话")
    else:  # /gpt4 <message>
        # 如果没有对话记录，则创建新对话
        if chat_info is None:
            chat_info = CopilotGPT4.create_chat(wx_id=wx_id, model=model)
            _send_text_msg(to, "无历史对话记录，创建新对话成功")
        response = CopilotGPT4.chat(chat_info, message)
        _send_text_msg(to, response)


def _gptx_chats(model: str, to: SendTo, message: str = "") -> None:
    response = CopilotGPT4.get_chat_list_str(to.p_id, model)
    _send_text_msg(to, response)


def _gptx_record(model: str, to: SendTo, message: str = "") -> None:
    wx_id = to.p_id
    chat_info = None
    if message == "":
        # 获取当前对话的对话记录
        chat_info = CopilotGPT4.get_chating_chat_info(wx_id, model)
    else:
        # 获取指定对话的对话记录
        chat_info = CopilotGPT4.get_chat_info(wx_id, model, int(message))
    if chat_info is None:
        _send_text_msg(to, "对话不存在")
        return
    response = CopilotGPT4.get_brief_conversation_str(chat_info)
    _send_text_msg(to, response)


def _gptx_continue(model: str, to: SendTo, message: str = "") -> None:
    wx_id = to.p_id
    # 判断message是否为数字
    if not message.isdigit():
        _send_text_msg(to, "请输入对话记录编号")
        return
    chat_info = CopilotGPT4.continue_chat(
        wx_id=wx_id, model=model, chat_index=int(message)
    )
    if chat_info is None:
        _send_text_msg(to, "对话不存在")
        return
    response = CopilotGPT4.get_brief_conversation_str(chat_info)
    response += "====================\n"
    response += "对话已选中，输入命令继续对话"
    _send_text_msg(to, response)


class CommandInvoker:
    """命令调用器"""

    def __init__(self) -> None:
        pass

    # 命令：/help
    @staticmethod
    def cmd_help(to: SendTo, message: str = "") -> None:
        # # 获取帮助信息(文本)
        # from command.help import get_help_msg
        # response = get_help_msg()
        # CommandInvoker._send_text_msg(to, response)

        # 获取帮助信息(图片)
        from command.help import get_help_msg

        help_msg = get_help_msg()
        response = text_to_image(help_msg)
        if response:
            Sender.send_localfile_msg(to, response)

    # 命令：/gpt35
    @staticmethod
    def cmd_gpt35(to: SendTo, message: str = "") -> None:
        _gptx("gpt-3.5-turbo", to, message)

    # 命令：/gpt35-chats
    @staticmethod
    def cmd_gpt35_chats(to: SendTo, message: str = "") -> None:
        _gptx_chats("gpt-3.5-turbo", to, message)

    # 命令：/gpt35-record
    @staticmethod
    def cmd_gpt35_record(to: SendTo, message: str = "") -> None:
        _gptx_record("gpt-3.5-turbo", to, message)

    # 命令：/gpt35-continue
    @staticmethod
    def cmd_gpt35_continue(to: SendTo, message: str = "") -> None:
        _gptx_continue("gpt-3.5-turbo", to, message)

    # 命令：/gpt4
    @staticmethod
    def cmd_gpt4(to: SendTo, message: str = "") -> None:
        _gptx("gpt-4", to, message)

    # 命令：/gpt4-chats
    @staticmethod
    def cmd_gpt4_chats(to: SendTo, message: str = "") -> None:
        _gptx_chats("gpt-4", to, message)

    # 命令：/gpt4-record
    @staticmethod
    def cmd_gpt4_record(to: SendTo, message: str = "") -> None:
        _gptx_record("gpt-4", to, message)

    # 命令：/gpt4-continue
    @staticmethod
    def cmd_gpt4_continue(to: SendTo, message: str = "") -> None:
        _gptx_continue("gpt-4", to, message)

    # TODO:
    # 命令：/gpt4-remove
    @staticmethod
    def cmd_gpt4_remove(to: SendTo, message: str = "") -> None:
        pass

    # 命令：/bili-hot
    @staticmethod
    def cmd_bili_hot(to: SendTo, message: str = "") -> None:
        response = get_bili_hot_str()
        _send_text_msg(to, response)

    # 命令：/zhihu-hot
    @staticmethod
    def cmd_zhihu_hot(to: SendTo, message: str = "") -> None:
        response = get_zhihu_hot_str()
        _send_text_msg(to, response)

    # 命令：/weibo-hot
    @staticmethod
    def cmd_weibo_hot(to: SendTo, message: str = "") -> None:
        response = get_weibo_hot_str()
        _send_text_msg(to, response)

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
            _send_text_msg(to, response)
            return
        if from_lang == "chinese":
            to_lang = "english"
        elif from_lang != "english" and not check_lang_support(from_lang, "chinese"):
            to_lang = "english"
        # 获取翻译
        response = get_reverso_context_tran_str(message, from_lang, to_lang)
        _send_text_msg(to, response)

    # 命令：/tran
    @staticmethod
    def cmd_tran(to: SendTo, message: str = "") -> None:
        # 获取翻译
        response = "翻译功能暂未开放"
        _send_text_msg(to, response)

    # 命令：/people
    @staticmethod
    def cmd_people_daily(to: SendTo, message: str = "") -> None:
        """发送人民日报url"""
        # 发送当天01版本的人民日报PDF
        if message.lower() == "url":
            url = get_paper_people_url()
            _send_text_msg(to, url)
        elif message.lower().startswith("url"):
            # 发送特定日期特定版本的url
            parts = message.lower().split()
            if len(parts) == 2 and parts[0] == "url" and parts[1].isdigit():
                url = get_paper_people_pdf_url(parts[1])
                if url:
                    _send_text_msg(to, url)
                if url is None:
                    e = "输入的日期版本号不符合要求，请重新输入\n若要获取2021年1月2日03版的人民日报的url，请输入\n/people url 2021010203"
                    _send_text_msg(to, e)
        else:
            # 发送人民日报PDF文件
            # 发送特定日期特定版本的人民日报PDF
            if message != "":
                url = get_paper_people_pdf_url(message)
                if url:
                    _send_file_url_msg(to, url)
                if url is None:
                    e = "输入的日期版本号不符合要求，请重新输入\n若要获取2021年1月2日03版的人民日报的pdf，请输入\n/people 2021010203"
                    _send_text_msg(to, e)

            # 发送当天01版本的人民日报PDF
            if message == "":
                url = get_paper_people_url()
                _send_file_url_msg(to, url)

    # 命令：/today-in-history
    @staticmethod
    def cmd_today_in_history(to: SendTo, message: str = "") -> None:
        # 获取历史上的今天
        response = get_today_in_history_str()
        _send_text_msg(to, response)

    # 命令：/github-trending
    @staticmethod
    def cmd_github_trending(to: SendTo, message: str = "") -> None:
        response = get_github_trending_str()
        _send_text_msg(to, response)

    # 命令：/douyin-hot
    @staticmethod
    def cmd_douyin_hot(to: SendTo, message: str = "") -> None:
        response = get_douyin_hot_str()
        _send_text_msg(to, response)

    # 命令：/pai-post
    @staticmethod
    def cmd_pai_post(to: SendTo, message: str = "") -> None:
        response = get_pai_post_str()
        _send_text_msg(to, response)

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
            _send_text_msg(to, result)
        else:
            # 添加待办事项
            add_success = add_todo_task(to.p_id, message)
            if add_success:
                result = view_todos(to.p_id, to.p_name)
                _send_text_msg(to, result)
            else:
                _send_text_msg(to, "添加失败")

    # 命令：/rmtd
    @staticmethod
    def cmd_remove_todo(to: SendTo, message: str = "") -> None:
        indices = [
            int(idx.strip()) - 1
            for idx in re.split(r"[\s,]+", message)
            if idx.strip().isdigit()
        ]
        if not indices:
            _send_text_msg(to, "请输入有效数字来删除待办事项")
            return

        remove_result = remove_todo_task(to.p_id, indices)
        _send_text_msg(to, remove_result)
        result = view_todos(to.p_id, to.p_name)
        _send_text_msg(to, result)
