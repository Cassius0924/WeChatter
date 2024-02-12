from datetime import datetime
from typing import List, Union

from loguru import logger

import wechatter.config as config
import wechatter.utils.path_manager as pm
from wechatter.commands.handlers import command
from wechatter.database import (
    GptChatInfo,
    GptChatMessage,
    WechatMessage,
    make_db_session,
)
from wechatter.models.message import SendTo
from wechatter.sender import sender
from wechatter.utils import post_request_json

DEFAULT_TOPIC = "（对话进行中*）"
# DEFAULT_MODEL = "gpt-4"
# TODO: 初始化对话，Prompt选择
DEFAULT_CONVERSATIONS = [{"role": "system", "content": "你是一位乐于助人的助手"}]


@command(
    command="gpt35",
    keys=["gpt"],
    desc="使用GPT3.5进行对话。",
)
def gpt35_command_handler(to: SendTo, message: str = "") -> None:
    _gptx("gpt-3.5-turbo", to, message)


@command(
    command="gpt35-chats",
    keys=["gpt-chats", "gpt对话记录"],
    desc="列出GPT3.5对话记录。",
)
def gpt35_chats_command_handler(to: SendTo, message: str = "") -> None:
    _gptx_chats("gpt-3.5-turbo", to, message)


@command(
    command="gpt35-record",
    keys=["gpt-record", "gpt记录"],
    desc="获取GPT3.5对话记录。",
)
def gpt35_record_command_handler(to: SendTo, message: str = "") -> None:
    _gptx_record("gpt-3.5-turbo", to, message)


@command(
    command="gpt35-continue",
    keys=["gpt-continue", "gpt继续"],
    desc="继续GPT3.5对话。",
)
def gpt35_continue_command_handler(to: SendTo, message: str = "") -> None:
    _gptx_continue("gpt-3.5-turbo", to, message)


@command(
    command="gpt4",
    keys=["gpt4"],
    desc="使用GPT4进行对话。",
)
def gpt4_command_handler(to: SendTo, message: str = "") -> None:
    _gptx("gpt-4", to, message)


@command(
    command="gpt4-chats",
    keys=["gpt4-chats", "gpt4对话记录"],
    desc="列出GPT4对话记录。",
)
def gpt4_chats_command_handler(to: SendTo, message: str = "") -> None:
    _gptx_chats("gpt-4", to, message)


@command(
    command="gpt4-record",
    keys=["gpt4-record", "gpt4记录"],
    desc="获取GPT4对话记录。",
)
def gpt4_record_command_handler(to: SendTo, message: str = "") -> None:
    _gptx_record("gpt-4", to, message)


@command(
    command="gpt4-continue",
    keys=["gpt4-continue", "gpt4继续"],
    desc="继续GPT4对话。",
)
def gpt4_continue_command_handler(to: SendTo, message: str = "") -> None:
    _gptx_continue("gpt-4", to, message)


# TODO:
# 命令：/gpt4-remove
def gpt4_remove_command_handler(to: SendTo, message: str = "") -> None:
    pass


def _gptx(model: str, to: SendTo, message: str = "") -> None:
    wx_id = to.p_id
    # 获取文件夹下最新的对话记录
    id = CopilotGPT4.get_chatting_chat_info(wx_id, model)
    if message == "":  # /gpt4
        # 判断对话是否有效
        sender.send_msg(to, "正在创建新对话...")
        if id is None or CopilotGPT4.is_chat_valid(id):
            CopilotGPT4.create_chat(wx_id=wx_id, model=model)
            logger.info("创建新对话成功")
            sender.send_msg(to, "创建新对话成功")
            return
        logger.info("对话未开始，继续上一次对话")
        sender.send_msg(to, "对话未开始，继续上一次对话")
    else:  # /gpt4 <message>
        # 如果没有对话记录，则创建新对话
        sender.send_msg(to, f"正在调用 {model} 进行对话...")
        if id is None:
            id = CopilotGPT4.create_chat(wx_id=wx_id, model=model)
            logger.info("无历史对话记录，创建新对话成功")
            sender.send_msg(to, "无历史对话记录，创建新对话成功")
        try:
            response = CopilotGPT4.chat(id, message)
            logger.info(response)
            sender.send_msg(to, response)
        except Exception as e:
            error_message = f"调用Copilot-GPT4-Server失败，错误信息：{str(e)}"
            logger.error(error_message)
            sender.send_msg(to, error_message)


def _gptx_chats(model: str, to: SendTo, message: str = "") -> None:
    response = CopilotGPT4.get_chat_list_str(to.p_id, model)
    sender.send_msg(to, response)


def _gptx_record(model: str, to: SendTo, message: str = "") -> None:
    wx_id = to.p_id
    id = None
    if message == "":
        # 获取当前对话的对话记录
        id = CopilotGPT4.get_chatting_chat_info(wx_id, model)
    else:
        # 获取指定对话的对话记录
        id = CopilotGPT4.get_chat_info(wx_id, model, int(message))
    if id is None:
        logger.warning("对话不存在")
        sender.send_msg(to, "对话不存在")
        return
    response = CopilotGPT4.get_brief_conversation_str(id)
    logger.info(response)
    sender.send_msg(to, response)


def _gptx_continue(model: str, to: SendTo, message: str = "") -> None:
    wx_id = to.p_id
    # 判断message是否为数字
    if not message.isdigit():
        logger.info("请输入对话记录编号")
        sender.send_msg(to, "请输入对话记录编号")
        return
    sender.send_msg(to, f"正在切换到对话记录 {message}...")
    chat_info = CopilotGPT4.continue_chat(
        wx_id=wx_id, model=model, chat_index=int(message)
    )
    if chat_info is None:
        warning_message = "选择历史对话失败，对话不存在"
        logger.warning(warning_message)
        sender.send_msg(to, warning_message)
        return
    response = CopilotGPT4.get_brief_conversation_str(chat_info)
    response += "====================\n"
    response += "对话已选中，输入命令继续对话"
    logger.info(response)
    sender.send_msg(to, response)


class CopilotGPT4:
    """Copilot-GPT4"""

    api = f"{config.cp_gpt4_api_host}:{config.cp_gpt4_port}/v1/chat/completions"
    bearer_token = "Bearer " + config.cp_token
    save_path = pm.get_abs_path("data/copilot_gpt4/chats/")

    @staticmethod
    def create_chat(wx_id: str, model: str) -> int:
        """创建一个新的对话"""
        # 生成上一次对话的主题
        CopilotGPT4._save_chatting_chat_topic(wx_id, model)
        CopilotGPT4._set_all_chats_unchatting(wx_id, model)
        gpt_chat_info = GptChatInfo(
            user_id=wx_id,
            model=model,
            talk_time=datetime.now(),
            topic=DEFAULT_TOPIC,
            is_chatting=True,
            gpt_chat_messages=[],
        )
        with make_db_session() as session:
            session.add(gpt_chat_info)
            session.commit()
            # 获取 SQLite 自动生成的 chat_id
            session.refresh(gpt_chat_info)
            return gpt_chat_info.id

    @staticmethod
    def continue_chat(wx_id: str, model: str, chat_index: int) -> Union[int, None]:
        """继续对话，从对话记录文件中读取对话记录
        :param wx_id: 微信用户ID
        :param chat_index: 对话记录索引（从1开始）
        :return: 简略的对话记录
        """
        # 读取对话记录文件
        id = CopilotGPT4.get_chat_info(wx_id, model, chat_index)
        if id is None:
            return None
        chatting_chat_info = CopilotGPT4.get_chatting_chat_info(wx_id, model)
        if not CopilotGPT4.is_chat_valid(chatting_chat_info):
            # 如果对话无效，则删除该对话记录后再继续对话
            CopilotGPT4._delete_chat(wx_id, chatting_chat_info.id)
        else:
            # 生成上一次对话的主题
            CopilotGPT4._save_chatting_chat_topic(wx_id, model)
        CopilotGPT4._set_chatting_chat(wx_id, model, id)
        return id

    @staticmethod
    def _set_chatting_chat(wx_id: str, model: str, chat_id: int) -> None:
        """设置正在进行中的对话记录"""
        # 先将所有对话记录的 is_chating 字段设置为 False
        CopilotGPT4._set_all_chats_unchatting(wx_id, model)
        with make_db_session() as session:
            chat_info = session.query(GptChatInfo).filter_by(id=chat_id).first()
            chat_info.is_chatting = True
            session.commit()

    @staticmethod
    def _delete_chat(wx_id: str, chat_id: int) -> None:
        """删除对话记录"""
        with make_db_session() as session:
            session.query(GptChatMessage).filter_by(gpt_chat_id=chat_id).delete()
            session.query(GptChatInfo).filter_by(id=chat_id).delete()
            session.commit()

    @staticmethod
    def get_brief_conversation_str(chat_info_id: int) -> str:
        """获取对话记录的字符串"""
        with make_db_session() as session:
            chat_info = session.query(GptChatInfo).filter_by(id=chat_info_id).first()
            conversation_str = f"✨==={chat_info.topic}===✨\n"
            if chat_info is None:
                conversation_str += "无对话记录"
                return conversation_str
            for msg in chat_info.gpt_chat_messages:
                content = msg.message.content[:30]
                if len(msg.message.content) > 30:
                    content += "..."
                if msg.role.value == "system":
                    conversation_str += f"⭐️：{content}\n"
                elif msg.role.value == "assistant":
                    conversation_str += f"🤖：{content}\n"
                elif msg.role.value == "user":
                    conversation_str += f"💬：{content}\n"
            return conversation_str

    # TODO: 删掉
    @staticmethod
    def _get_brief_conversation_content(conversation: List) -> List:
        """获取简略的对话记录的内容"""
        content_list = []
        for conv in conversation[1:]:
            if len(conv["content"]) > 20:
                conv["content"] = conv["content"][:20] + "..."
            content_list.append(conv["content"])
        return content_list

    @staticmethod
    def _set_all_chats_unchatting(wx_id: str, model: str) -> None:
        """将所有对话记录的 is_chatting 字段设置为 False"""
        with make_db_session() as session:
            session.query(GptChatInfo).filter_by(user_id=wx_id, model=model).update(
                {"is_chatting": False}
            )
            session.commit()

    @staticmethod
    def is_chat_valid(chat_info_id: int) -> bool:
        """判断对话是否有效"""
        # 通过 conversation 长度判断对话是否有效
        with make_db_session() as session:
            chat_info = session.query(GptChatInfo).filter_by(id=chat_info_id).first()
            if len(chat_info.gpt_chat_messages) <= 1:
                return False
            return True

    @staticmethod
    def _list_chat_info(wx_id: str, model: str) -> List:
        """列出用户的所有对话记录"""
        # 取出id，按照 chat_talk_time 字段倒序排序，取前20个
        with make_db_session() as session:
            chat_info_list = (
                session.query(GptChatInfo.id)
                .filter_by(user_id=wx_id, model=model)
                .order_by(
                    GptChatInfo.is_chatting.desc(),
                    GptChatInfo.talk_time.desc(),
                )
                .limit(20)
                .all()
            )
            return [chat_info[0] for chat_info in chat_info_list]

    @staticmethod
    def get_chat_list_str(wx_id: str, model: str) -> str:
        """获取用户的所有对话记录"""
        chat_info_list = CopilotGPT4._list_chat_info(wx_id, model)
        chat_info_list_str = "✨===GPT4对话记录===✨\n"
        if chat_info_list == []:
            chat_info_list_str += "     📭 无对话记录"
            return chat_info_list_str
        with make_db_session() as session:
            for i, id in enumerate(chat_info_list):
                chat = session.query(GptChatInfo).filter_by(id=id).first()
                if chat.is_chatting:
                    chat_info_list_str += f"{i+1}. 💬{chat.topic}\n"
                else:
                    chat_info_list_str += f"{i+1}. {chat.topic}\n"
            return chat_info_list_str

    @staticmethod
    def _update_chat(chat_info: GptChatInfo, newconv: List = []) -> None:
        """保存对话记录
        :param chat_info: 对话记录数据
        :param newconv: 新增对话记录
        """
        # 对话记录格式
        with make_db_session() as session:
            chat_info.talk_time = datetime.now()
            # session.commit()
            for conv in newconv:
                wx_message = WechatMessage(
                    user_id=chat_info.user_id,
                    type="text",
                    content=conv["content"],
                )
                chat_message = GptChatMessage(
                    gpt_chat_id=chat_info.id,
                    role=conv["role"],
                    message=wx_message,
                )
                session.add(chat_message)
            session.commit()

    @staticmethod
    def get_chat_info(wx_id: str, model: str, chat_index: int) -> Union[int, None]:
        """获取用户的对话信息"""
        chat_info_id_list = CopilotGPT4._list_chat_info(wx_id, model)
        if chat_info_id_list == []:
            return None
        if chat_index <= 0 or chat_index > len(chat_info_id_list):
            return None
        return chat_info_id_list[chat_index - 1]

    @staticmethod
    def _get_chat_conversations(chat_id: int) -> List[GptChatMessage]:
        """获取对话记录"""
        with make_db_session() as session:
            chat_info = session.query(GptChatInfo).filter_by(id=chat_id).first()
            return chat_info.gpt_chat_messages

    @staticmethod
    def get_chatting_chat_info(wx_id: str, model: str) -> Union[int, None]:
        """获取正在进行中的对话信息"""
        # 获取对话元信息
        with make_db_session() as session:
            chat_info_id = (
                session.query(GptChatInfo.id)
                .filter_by(user_id=wx_id, model=model, is_chatting=True)
                .first()
            )
            if chat_info_id is None:
                return None
            return chat_info_id[0]

    @staticmethod
    def chat(chat_info_id: int, message: str) -> str:
        """使用 Copilot-GPT4-Server 持续对话"""
        # 对外暴露的对话方法，必须保存对话记录
        return CopilotGPT4._chat(
            chat_info_id=chat_info_id, message=message, is_save=True
        )

    @staticmethod
    def _chat(chat_info_id: int, message: str, is_save: bool = True) -> str:
        """使用 Copilot-GPT4-Server 持续对话
        :param message: 用户消息
        :param is_save: 是否保存此轮对话记录
        """
        with make_db_session() as session:
            chat_info = session.query(GptChatInfo).filter_by(id=chat_info_id).first()
            newconv = []
            newconv.append({"role": "user", "content": message})

            # 发送请求
            headers = {
                "Authorization": CopilotGPT4.bearer_token,
                "Content-Type": "application/json",
            }
            json = {
                "model": chat_info.model,
                "messages": DEFAULT_CONVERSATIONS
                + chat_info.get_conversations()
                + newconv,
            }
            r_json = post_request_json(
                url=CopilotGPT4.api, headers=headers, json=json, timeout=60
            )

            # 判断是否有 error 或 code 字段
            if "error" in r_json or "code" in r_json:
                raise ValueError("Copilot-GPT4-Server返回值错误")

            msg = r_json["choices"][0]["message"]
            msg_content = msg.get("content", "调用Copilot-GPT4-Server失败")

            # 将返回的 assistant 回复添加到对话记录中
            if is_save is True:
                newconv.append({"role": "assistant", "content": msg_content})
                chat_info.extend_conversations(newconv)

                # CopilotGPT4._update_chat(chat_info, newconv)
                chat_info.talk_time = datetime.now()
                with make_db_session() as session:
                    # TODO: ^^^^
                    for conv in newconv:
                        wx_message = WechatMessage(
                            user_id=chat_info.user_id,
                            type="text",
                            content=conv["content"],
                        )
                        chat_message = GptChatMessage(
                            gpt_chat_id=chat_info.id,
                            role=conv["role"],
                            message=wx_message,
                        )
                        session.add(chat_message)
                    session.commit()
            return msg_content

    @staticmethod
    def _has_topic(chat_info_id: int) -> bool:
        """判断对话是否有主题"""
        with make_db_session() as session:
            chat_info = session.query(GptChatInfo).filter_by(id=chat_info_id).first()
            return chat_info.topic != DEFAULT_TOPIC

    @staticmethod
    def _save_chatting_chat_topic(wx_id: str, model: str) -> None:
        """生成正在进行的对话的主题"""
        id = CopilotGPT4.get_chatting_chat_info(wx_id, model)
        if id is None or CopilotGPT4._has_topic(id):
            return
        # 生成对话主题
        if not CopilotGPT4.is_chat_valid(id):
            logger.error("对话记录长度小于1")
            return

        topic = CopilotGPT4._generate_chat_topic(id)
        if topic == "":
            logger.error("生成对话主题失败")
            raise ValueError("生成对话主题失败")
        # 更新对话主题
        with make_db_session() as session:
            chat_info = session.query(GptChatInfo).filter_by(id=id).first()
            chat_info.topic = topic
            session.commit()

    @staticmethod
    def _generate_chat_topic(chat_info_id: int) -> str:
        """生成对话主题，用于保存对话记录"""
        assert CopilotGPT4.is_chat_valid(chat_info_id)
        # 通过一次对话生成对话主题，但这次对话不保存到对话记录中
        prompt = "请用10个字以内总结一下这次对话的主题，不带任何标点符号"
        topic = CopilotGPT4._chat(
            chat_info_id=chat_info_id, message=prompt, is_save=False
        )
        # 限制主题长度
        if len(topic) > 21:
            topic = topic[:21] + "..."
        logger.info(f"生成对话主题：{topic}")
        return topic
