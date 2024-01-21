# 使用 Copilot-GPT4-Server 回复
from typing import Dict, List, Union

import requests
from wechatter.sqlite.sqlite_manager import SqliteManager
from wechatter.utils.path_manager import PathManager as pm
from wechatter.utils.time import get_current_timestamp

from main import cr

DEFAULT_TOPIC = "（对话进行中*）"
DEFAULT_MODEL = "gpt-4"
DEFAULT_CONVERSATIONS = [{"role": "system", "content": "你是一位乐于助人的助手"}]


class ChatInfo:
    """对话信息（与 copilot_chats 表对应）"""

    def __init__(
        self,
        wx_id: str = "",
        chat_created_time: int = -1,
        chat_talk_time: int = -1,
        chat_topic: str = DEFAULT_TOPIC,
        chat_model: str = DEFAULT_MODEL,
        conversations: List[Dict] = DEFAULT_CONVERSATIONS,
        is_chating: bool = False,
        chat_id: int = -1,
    ):
        self.chat_id = chat_id
        self.wx_id = wx_id
        self.chat_created_time = chat_created_time
        self.chat_talk_time = chat_talk_time
        self.chat_topic = chat_topic
        self.chat_model = chat_model
        self.conversations = conversations
        self.is_chating = is_chating

    @property
    def has_topic(self) -> bool:
        """是否有对话主题"""
        if self.chat_topic == DEFAULT_TOPIC:
            return False
        return True

    @property
    def dict(self) -> Dict:
        """将对象转为字典（删去 conversations 字段）"""
        chat_info_dict = self.__dict__.copy()
        chat_info_dict.pop("conversations")
        return chat_info_dict


class CopilotGPT4:
    """Copilot-GPT4"""

    api = f"{cr.cp_gpt4_api_host}:{cr.cp_gpt4_port}/v1/chat/completions"
    bearer_token = "Bearer " + cr.cp_token
    save_path = pm.get_abs_path("data/copilot_gpt4/chats/")

    @staticmethod
    def create_chat(
        wx_id: str,
        model: str,
    ) -> ChatInfo:
        """创建一个新的对话"""
        # 生成上一次对话的主题
        CopilotGPT4._generate_chating_chat_topic(wx_id, model)
        CopilotGPT4._set_all_chats_unchating(wx_id, model)
        timestamp = get_current_timestamp()
        chat_info = ChatInfo(
            wx_id=wx_id,
            chat_created_time=timestamp,
            chat_talk_time=timestamp,
            chat_model=model,
            is_chating=True,
        )
        # 保存对话记录
        chat_info_dict = chat_info.dict
        # 删去 chat_id 字段，让数据库自动生成
        chat_info_dict.pop("chat_id")
        sqlm = SqliteManager()
        sqlm.insert("copilot_chats", chat_info_dict)
        # 获取 SQLite 自动生成的 chat_id
        sql = (
            "SELECT chat_id "
            "FROM copilot_chats "
            "WHERE wx_id = ? AND is_chating = TRUE AND chat_model = ? "
        )
        result = sqlm.fetch_one(sql, (wx_id, model))
        chat_info.chat_id = result[0]
        # 插入对话记录
        sqlm.insert(
            "chat_conversations",
            {
                "chat_id": chat_info.chat_id,
                "conversation_role": chat_info.conversations[0]["role"],
                "conversation_content": chat_info.conversations[0]["content"],
                "conversation_timestamp": get_current_timestamp(),
            },
        )
        return chat_info

    @staticmethod
    def continue_chat(wx_id: str, model: str, chat_index: int) -> Union[ChatInfo, None]:
        """继续对话，从对话记录文件中读取对话记录
        :param wx_id: 微信用户ID
        :param chat_index: 对话记录索引（从1开始）
        :return: 简略的对话记录
        """
        # 读取对话记录文件
        chat_info = CopilotGPT4.get_chat_info(wx_id, model, chat_index)
        if chat_info is None:
            return None
        chating_chat_info = CopilotGPT4.get_chating_chat_info(wx_id, model)
        if not CopilotGPT4.is_chat_valid(chating_chat_info):
            # 如果对话无效，则删除该对话记录后再继续对话
            CopilotGPT4._delete_chat(wx_id, chating_chat_info.chat_id)
        else:
            # 生成上一次对话的主题
            CopilotGPT4._generate_chating_chat_topic(wx_id, model)
        CopilotGPT4._set_chating_chat(wx_id, model, chat_info.chat_id)
        return chat_info

    @staticmethod
    def _set_chating_chat(wx_id: str, model: str, chat_id: int) -> None:
        """设置正在进行中的对话记录"""
        # 先将所有对话记录的 is_chating 字段设置为 False
        CopilotGPT4._set_all_chats_unchating(wx_id, model)
        sqlm = SqliteManager()
        sqlm.update(
            "copilot_chats",
            {"is_chating": True},
            f"wx_id = '{wx_id}' AND chat_id = {chat_id}",
        )

    @staticmethod
    def _delete_chat(wx_id: str, chat_id: int) -> None:
        """删除对话记录"""
        sqlm = SqliteManager()
        # 先删除对话记录
        sqlm.delete("chat_conversations", f"chat_id = {chat_id}")
        # 再删除对话元数据
        sqlm.delete("copilot_chats", f"wx_id = '{wx_id}' AND chat_id = {chat_id}")

    @staticmethod
    def get_brief_conversation_str(chat_info: ChatInfo) -> str:
        """获取对话记录的字符串"""
        conversation_str = f"✨==={chat_info.chat_topic}===✨\n"
        if chat_info == []:
            conversation_str += "无对话记录"
            return conversation_str
        for conv in chat_info.conversations[-10:]:
            content = conv["content"][:30]
            if len(conv["content"]) > 30:
                content += "..."
            if conv["role"] == "system":
                conversation_str += f"⭐️：{content}\n"
            elif conv["role"] == "assistant":
                conversation_str += f"🤖：{content}\n"
            elif conv["role"] == "user":
                conversation_str += f"💬：{content}\n"
        return conversation_str

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
    def _generate_chat_topic(chat_info: ChatInfo) -> None:
        """生成对话的主题"""
        # 只生成一次对话主题
        if chat_info.has_topic:
            return
        # 生成对话主题
        topic = CopilotGPT4._generate_chat_topic(chat_info)
        if topic == "":
            return
        # 更新对话主题
        chat_info.chat_topic = topic
        CopilotGPT4._update_chat(chat_info)

    @staticmethod
    def _generate_chating_chat_topic(wx_id: str, model: str) -> None:
        """生成正在进行的对话的主题"""
        chat_info = CopilotGPT4.get_chating_chat_info(wx_id, model)
        if chat_info is None:
            return
        # 只生成一次对话主题
        if chat_info.has_topic:
            return
        # 生成对话主题
        topic = CopilotGPT4._generate_chat_topic(chat_info)
        if topic == "":
            return
        # 更新对话主题
        chat_info.chat_topic = topic
        CopilotGPT4._update_chat(chat_info)

    @staticmethod
    def _set_all_chats_unchating(wx_id: str, model: str) -> None:
        """将所有对话记录的 is_chating 字段设置为 False"""
        sqlm = SqliteManager()
        sqlm.update(
            "copilot_chats",
            {"is_chating": False},
            f"wx_id = '{wx_id}' AND chat_model = '{model}'",
        )

    @staticmethod
    def is_chat_valid(chat_info: ChatInfo) -> bool:
        """判断对话是否有效"""
        # 通过 conversation 长度判断对话是否有效
        if len(chat_info.conversations) <= 1:
            return False
        return True

    @staticmethod
    def _list_chat_info(wx_id: str, model: str) -> List:
        """列出用户的所有对话记录"""
        # 读取对话记录文件夹，按照 chat_talk_time 字段倒序排序，取前20个
        sqlm = SqliteManager()
        sql = (
            "SELECT chat_id, wx_id, chat_created_time, chat_talk_time, chat_topic, chat_model, is_chating "
            "FROM copilot_chats "
            "WHERE wx_id = ? AND chat_model = ? "
            "ORDER BY "
            "CASE WHEN is_chating THEN 1 ELSE 0 END DESC, "
            "chat_talk_time DESC LIMIT 20 "
        )
        result = sqlm.fetch_all(sql, (wx_id, model))
        chat_info_list = []
        for chat in result:
            chat_info_list.append(
                ChatInfo(
                    chat_id=chat[0],
                    wx_id=chat[1],
                    chat_created_time=chat[2],
                    chat_talk_time=chat[3],
                    chat_topic=chat[4],
                    chat_model=chat[5],
                    is_chating=chat[6],
                )
            )
        return chat_info_list

    @staticmethod
    def get_chat_list_str(wx_id: str, model: str) -> str:
        """获取用户的所有对话记录"""
        chat_info_list = CopilotGPT4._list_chat_info(wx_id, model)
        chat_info_list_str = "✨===GPT4对话记录===✨\n"
        if chat_info_list == []:
            chat_info_list_str += "     📭 无对话记录"
            return chat_info_list_str
        for i, chat in enumerate(chat_info_list):
            if chat.is_chating:
                chat_info_list_str += f"{i+1}. 💬{chat.chat_topic}\n"
            else:
                chat_info_list_str += f"{i+1}. {chat.chat_topic}\n"
        return chat_info_list_str

    @staticmethod
    def _update_chat(chat_info: ChatInfo, newconv: List = []) -> None:
        """保存对话记录
        :param chat_info: 对话记录数据
        :param newconv: 新增对话记录
        """
        # 对话记录格式
        chat_info.chat_talk_time = get_current_timestamp()
        sqlm = SqliteManager()
        chat_info_dict = chat_info.dict
        # 更新对话元数据
        sqlm.update(
            "copilot_chats",
            chat_info_dict,
            f"chat_id = {chat_info.chat_id}",
        )
        # 插入对话记录
        for conv in newconv:
            sqlm.insert(
                "chat_conversations",
                {
                    "chat_id": chat_info.chat_id,
                    "conversation_role": conv["role"],
                    "conversation_content": conv["content"],
                    "conversation_timestamp": get_current_timestamp(),
                },
            )

    @staticmethod
    def get_chat_info(wx_id: str, model: str, chat_index: int) -> Union[ChatInfo, None]:
        """获取用户的对话信息"""
        chat_index = chat_index - 1
        sql = (
            "SELECT chat_id, wx_id, chat_created_time, chat_talk_time, chat_topic, chat_model, is_chating "
            "FROM copilot_chats "
            "WHERE wx_id = ? AND chat_model = ? "
            "ORDER BY "
            "CASE WHEN is_chating THEN 1 ELSE 0 END DESC, "
            "chat_talk_time DESC LIMIT 20 "
        )
        sqlm = SqliteManager()
        result = sqlm.fetch_all(sql, (wx_id, model))
        if result == []:
            return None
        if len(result) <= chat_index:
            return None
        chat = result[chat_index]
        # 获取对话记录
        conv = CopilotGPT4._get_chat_conversations(chat[0])
        chat_info = ChatInfo(
            chat_id=chat[0],
            wx_id=chat[1],
            chat_created_time=chat[2],
            chat_talk_time=chat[3],
            chat_topic=chat[4],
            chat_model=chat[5],
            conversations=conv,
            is_chating=chat[6],
        )
        return chat_info

    @staticmethod
    def _get_chat_conversations(chat_id: int) -> List:
        sql = (
            "SELECT conversation_role, conversation_content, conversation_timestamp FROM chat_conversations "
            "WHERE chat_id = ?"
        )
        sqlm = SqliteManager()
        result = sqlm.fetch_all(sql, (chat_id,))
        conversations = []
        for conv in result:
            conversations.append(
                {
                    "role": conv[0],
                    "content": conv[1],
                    "timestamp": conv[2],
                }
            )
        return conversations

    @staticmethod
    def get_chating_chat_info(wx_id: str, model: str) -> Union[ChatInfo, None]:
        """获取正在进行中的对话信息"""
        # 获取对话元信息
        sql = (
            "SELECT chat_id, wx_id, chat_created_time, chat_talk_time, chat_topic, chat_model, is_chating "
            "FROM copilot_chats "
            "WHERE wx_id = ? AND is_chating = TRUE AND chat_model = ? "
        )
        sqlm = SqliteManager()
        meta_info = sqlm.fetch_one(sql, (wx_id, model))
        if meta_info is None:
            return None
        # 获取对话记录
        conv = CopilotGPT4._get_chat_conversations(meta_info[0])
        return ChatInfo(
            chat_id=meta_info[0],
            wx_id=meta_info[1],
            chat_created_time=meta_info[2],
            chat_talk_time=meta_info[3],
            chat_topic=meta_info[4],
            chat_model=meta_info[5],
            conversations=conv,
            is_chating=meta_info[6],
        )

    @staticmethod
    def chat(chat_info: ChatInfo, message: str) -> str:
        """使用 Copilot-GPT4-Server 持续对话"""
        # 对外暴露的对话方法，必须保存对话记录
        return CopilotGPT4._chat(chat_info=chat_info, message=message, is_save=True)

    @staticmethod
    def _chat(chat_info: ChatInfo, message: str, is_save: bool = True) -> str:
        """使用 Copilot-GPT4-Server 持续对话
        :param message: 用户消息
        :param is_save: 是否保存此轮对话记录
        """
        newconv = []
        conversations = chat_info.conversations.copy()
        # 将conversation 内字典的所有 timestamp 字段删除
        for conv in conversations:
            if "timestamp" in conv:
                conv.pop("timestamp")
        newconv.append({"role": "user", "content": message})
        # 发送请求
        try:
            response = requests.post(
                CopilotGPT4.api,
                headers={
                    "Authorization": CopilotGPT4.bearer_token,
                    "Content-Type": "application/json",
                },
                json={
                    "model": chat_info.chat_model,
                    # "messages": str(conv)
                    "messages": conversations + newconv,
                },
            )
        except Exception as e:
            print(e)
            return "调用Copilot-GPT4-Server失败"

        if response.status_code != 200:
            return "调用Copilot-GPT4-Server失败"

        # 解析返回值JSON
        response_json = {}
        try:
            response_json = response.json()
        except Exception as e:
            print(response.text)
            print(e)
            return "解析Copilot-GPT4-Server JSON失败"
        # 判断是否有 error 或 code 字段
        if "error" in response_json or "code" in response_json:
            return "Copilot-GPT4-Server返回值错误"
        msg = response_json["choices"][0]["message"]
        msg_content = msg.get("content", "调用Copilot-GPT4-Server失败")
        # 将返回的 assistant 回复添加到对话记录中
        if is_save:
            newconv.append({"role": "assistant", "content": msg_content})
            chat_info.conversations.extend(newconv)
            CopilotGPT4._update_chat(chat_info, newconv)
        print("#" * 30)
        print(msg_content)
        return msg_content

    @staticmethod
    def _generate_chat_topic(chat_info: ChatInfo) -> str:
        """生成对话主题，用于保存对话记录"""
        # 通过 conversation 长度判断对话是否有效

        if len(chat_info.conversations) <= 1:
            return ""
        # 通过一次对话生成对话主题，但这次对话不保存到对话记录中
        prompt = "请用10个字以内总结一下这次对话的主题，不带任何标点符号"
        topic = CopilotGPT4._chat(chat_info=chat_info, message=prompt, is_save=False)
        # 限制主题长度
        if len(topic) > 21:
            topic = topic[:21] + "..."
        return topic
