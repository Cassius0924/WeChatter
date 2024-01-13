# 使用 Copilot-GPT4-Server 回复
from typing import Dict, List
import requests
import json
from utils.path import PathManager as pm
from utils.file_manager import FileManager as fm
from utils.time import get_current_timestamp
from main import cr


class CopilotGPT4:
    """Copilot-GPT4"""

    api = f"{cr.cp_gpt4_api_host}:{cr.cp_gpt4_port}/v1/chat/completions"
    bearer_token = "Bearer " + cr.cp_token
    save_path = pm.get_abs_path("data/copilot_gpt4/chats/")

    @staticmethod
    def create_chat(
        person_id: str,
        system_content: str = "你是一个乐于助人的助手",
        model: str = "gpt-4",
    ) -> Dict:
        """创建一个新的对话"""
        # 创建个人文件夹
        if not fm.is_folder_exist(CopilotGPT4.save_path, person_id):
            print("创建文件夹")
            fm.create_folder(CopilotGPT4.save_path, person_id)
        else:
            # 生成上一次对话的主题
            CopilotGPT4._generate_previous_chat_topic(person_id)
            # 修改文件名前缀
            CopilotGPT4._update_chating_prefix_to_chat(person_id, 2)
        timestamp = get_current_timestamp()
        chat_info = {
            "create_time": timestamp,
            "last_chat_time": timestamp,
            "has_topic": False,
            "topic": "💬无主题对话（对话进行中）",
            "model": model,
            "conversation": [{"role": "system", "content": system_content}],
        }
        # 保存对话记录
        CopilotGPT4._save_chat(person_id, chat_info)
        return chat_info

    @staticmethod
    def continue_chat(person_id: str, chat_index: int) -> Dict:
        """继续对话，从对话记录文件中读取对话记录
        :param person_id: 用户ID
        :param conversation_index: 对话记录索引（从1开始）
        :return: 简略的对话记录
        """
        # 读取对话记录文件
        chat_info = CopilotGPT4._read_chat(person_id, chat_index)
        # 读取失败
        if chat_info == {}:
            return {}
        # 生成上一次对话的主题
        CopilotGPT4._generate_previous_chat_topic(person_id)
        CopilotGPT4._update_chat_prefix_to_chating(person_id, chat_index)
        CopilotGPT4._update_chating_prefix_to_chat(person_id, 2)
        # 修正选中的对话记录文件的文件名
        return chat_info["conversation"]

    @staticmethod
    # def _fix_chat_info_file_name(person_id: str, chat_index: int) -> None:
    def _update_chat_prefix_to_chating(person_id: str, chat_index: int) -> None:
        """将正在对话的文件名前缀 chat_ 修改为 chating_"""
        # 读取对话记录文件，save_path/person_id 的第 conversation_index 个文件
        chat_index = chat_index - 1
        files = CopilotGPT4._list_chat_info_file(person_id)
        if len(files) <= chat_index:
            print("对话记录文件不存在")
            return
        file_name = files[chat_index]
        print(file_name)
        if file_name.startswith("chat_"):
            file_path = pm.join_path(CopilotGPT4.save_path, person_id, file_name)
            fm.rename_file(file_path, "chating_" + file_name[5:])

    @staticmethod
    def get_brief_conversation_str(chat_info: Dict) -> str:
        """获取对话记录的字符串"""
        conversation_str = "✨ GPT4对话记录 ✨\n"
        if chat_info == []:
            conversation_str += "无对话记录"
            return conversation_str
        for conv in chat_info[-10:]:
            content = conv["content"][:30]
            if len(conv["content"]) > 30:
                content += "..."
            if conv["role"] == "system":
                conversation_str += f"⭐️：{content}\n"
            elif conv["role"] == "assistant":
                conversation_str += f"🤖：{content}\n"
            elif conv["role"] == "user":
                conversation_str += f"💬: {content}\n"
        conversation_str += "====================\n"
        conversation_str += "对话已选中，输入 /gpt4 命令继续对话"
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
    def _generate_previous_chat_topic(person_id: str) -> None:
        """更新上一次对话的主题"""
        chat_info = CopilotGPT4.get_chat_info(person_id, 1)
        if chat_info == {}:
            return
        if chat_info["has_topic"]:
            return
        # 生成对话主题
        topic = CopilotGPT4._generate_chat_topic(person_id, chat_info)
        if topic == "":
            return
        # 更新对话主题
        chat_info["topic"] = topic
        chat_info["has_topic"] = True
        CopilotGPT4._save_chat(person_id, chat_info)

    @staticmethod
    def _update_chating_prefix_to_chat(person_id: str, chat_index: int) -> None:
        """将正在对话的文件名前缀 chating_ 修改为 chat_"""
        chat_index = chat_index - 1
        files = CopilotGPT4._list_chat_info_file(person_id)
        if len(files) <= chat_index:
            print("对话记录文件不存在")
            return
        file_name = files[chat_index]
        if file_name.startswith("chating_"):
            file_path = pm.join_path(CopilotGPT4.save_path, person_id, file_name)
            fm.rename_file(file_path, "chat_" + file_name[8:])

    @staticmethod
    def is_chat_valid(chat_info: Dict) -> bool:
        """判断对话是否有效"""
        # 通过 conversation 长度判断对话是否有效
        if chat_info == {}:
            return False
        if len(chat_info["conversation"]) <= 1:
            return False
        return True

    @staticmethod
    def _list_chat_info(person_id: str) -> List[Dict]:
        """列出用户的所有对话记录"""
        # 读取对话记录文件夹
        # 读取对话记录文件
        files = CopilotGPT4._list_chat_info_file(person_id)
        # 取前20个文件
        files = files[:20]
        chat_info_list = []
        for file in files:
            file_path = pm.join_path(CopilotGPT4.save_path, person_id, file)
            with open(file_path, "r", encoding="utf-8") as f:
                chat_info_list.append(json.load(f))
        return chat_info_list

    @staticmethod
    def get_chat_list_str(person_id: str) -> str:
        """获取用户的所有对话记录"""
        chat_info_list = CopilotGPT4._list_chat_info(person_id)
        if chat_info_list == []:
            return "无对话记录"
        chat_info_list_str = "✨ GPT4对话记录 ✨\n"
        for i, chat in enumerate(chat_info_list):
            chat_info_list_str += f"{i+1}. {chat['topic']}\n"
        return chat_info_list_str

    @staticmethod
    def _read_chat(person_id: str, chat_index: int) -> Dict:
        """读取对话记录文件"""
        file_name = CopilotGPT4._get_chat_info_file(person_id, chat_index)
        if file_name == "":
            return {}
        file_path = pm.join_path(CopilotGPT4.save_path, person_id, file_name)
        result = {}
        # 读取 JSON 文件，conversation 字段是对话记录
        with open(file_path, "r", encoding="utf-8") as file:
            result = json.load(file)
        return result

    @staticmethod
    def _list_chat_info_file(person_id: str) -> List[str]:
        """获取对话记录文件名列表"""
        # 读取对话记录文件
        files = fm.list_files(pm.join_path(CopilotGPT4.save_path, person_id))
        # 文件名是时间戳开头，所以按照字母倒序排序，第一个就是最新的
        files.sort(reverse=True)
        return files

    @staticmethod
    def _get_chat_info_file(person_id: str, chat_index: int) -> str:
        """获取对话记录文件名"""
        # 读取对话记录文件，save_path/person_id 的第 conversation_index 个文件
        files = CopilotGPT4._list_chat_info_file(person_id)
        if len(files) <= chat_index - 1:
            print("对话记录文件不存在")
            return ""
        return files[chat_index - 1]

    @staticmethod
    def _save_chat(person_id: str, chat_info: Dict) -> None:
        """保存对话记录
        :param conversation: 对话记录
        """
        # 文件名由时间戳和对话主题组成
        create_time = chat_info["create_time"]
        # 以"chating"前缀开头表示正在进行中的对话
        save_path = pm.join_path(
            CopilotGPT4.save_path, person_id, f"chating_{str(create_time)}" + ".json"
        )
        # 对话记录格式
        chat_info["last_chat_time"] = get_current_timestamp()
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(chat_info, ensure_ascii=False))
        # CopilotGPT4._delete_old_chats(person_id)
        # 删除旧的对话记录，保持20个最新的对话记录

    @staticmethod
    def _delete_old_chat(person_id: str) -> None:
        """删除旧的对话记录，保持20个最新的对话记录"""
        # 读取对话记录文件夹
        # 读取对话记录文件
        files = CopilotGPT4._list_chat_info_file(person_id)
        # 删除旧的对话记录，保持20个最新的对话记录
        if len(files) > 20:
            for file in files[20:]:
                file_path = pm.join_path(CopilotGPT4.save_path, person_id, file)
                fm.delete_file(file_path)

    @staticmethod
    def get_chat_info(person_id: str, chat_index: int) -> Dict:
        """获取用户的对话信息"""
        # 读取对话记录文件，save_path/person_id 的第一个文件
        file_name = CopilotGPT4._get_chat_info_file(person_id, chat_index)
        # 无对话记录
        if file_name == "":
            return {}
        file_path = pm.join_path(CopilotGPT4.save_path, person_id, file_name)
        chat_info = {}
        # 读取 JSON 文件
        with open(file_path, "r", encoding="utf-8") as file:
            chat_info = json.load(file)
        return chat_info

    @staticmethod
    def chat(person_id: str, chat_info: Dict, message: str) -> str:
        """使用 Copilot-GPT4-Server 持续对话"""
        # 对外暴露的对话方法，必须保存对话记录
        response = CopilotGPT4._chat(
            person_id=person_id, chat_info=chat_info, message=message, is_save=True
        )
        return response

    @staticmethod
    def _chat(
        person_id: str, chat_info: Dict, message: str, is_save: bool = True
    ) -> str:
        """使用 Copilot-GPT4-Server 持续对话
        :param message: 用户消息
        :param is_save: 是否保存此轮对话记录
        """
        # TODO: 判断是否创建了对话
        # if len(CopilotGPT4.conv) <= 0:

        conversation = chat_info["conversation"]
        conversation.append({"role": "user", "content": message})
        # 发送请求
        try:
            # print(conversation)
            response = requests.post(
                CopilotGPT4.api,
                headers={
                    "Authorization": CopilotGPT4.bearer_token,
                    "Content-Type": "application/json",
                },
                json={
                    "model": chat_info["model"],
                    "messages": conversation,
                },
            )
        except Exception as e:
            print(e)
            conversation.pop()
            return "调用Copilot-GPT4-Server失败"

        if response.status_code != 200:
            conversation.pop()
            return "调用Copilot-GPT4-Server失败"

        # 解析返回值JSON
        response_json = {}
        try:
            response_json = response.json()
        except Exception as e:
            print(response.text)
            print(e)
            conversation.pop()
            return "解析Copilot-GPT4-Server JSON失败"
        # 判断是否有 error 或 code 字段
        if "error" in response_json or "code" in response_json:
            conversation.pop()
            return "Copilot-GPT4-Server返回值错误"
        msg = response_json["choices"][0]["message"]
        msg_content = msg.get("content", "调用Copilot-GPT4-Server失败")
        # 将返回的 assistant 回复添加到对话记录中
        conversation.append({"role": "assistant", "content": msg_content})
        # 如果不保存此轮对话，则删除最后两条对话
        if is_save:
            CopilotGPT4._save_chat(person_id, chat_info)
        else:
            conversation.pop()
            conversation.pop()
        print("#" * 20)
        print(msg_content)
        return msg_content

    @staticmethod
    def _add_u_conv(conversation: List, msg: str) -> List:
        """添加一条用户对话"""
        conversation.append({"role": "user", "content": msg})
        return conversation

    @staticmethod
    def _add_a_conv(conversation: List, msg: str) -> List:
        """添加一条助手对话"""
        conversation.append({"role": "assistant", "content": msg})
        return conversation

    @staticmethod
    def _generate_chat_topic(person_id: str, chat_info: Dict) -> str:
        """生成对话主题，用于保存对话记录"""
        # 通过 conversation 长度判断对话是否有效

        if len(chat_info["conversation"]) <= 1:
            return ""
        # 通过一次对话生成对话主题，但这次对话不保存到对话记录中
        prompt = "请用10个字以内总结一下这次对话的主题"
        topic = CopilotGPT4._chat(
            person_id=person_id, chat_info=chat_info, message=prompt, is_save=False
        )
        # 限制主题长度
        if len(topic) > 21:
            topic = topic[:21] + "..."
        return topic


"""
一次 Chat 信息的 JSON 格式
{
  "last_chat_time": "2024-01-02 00:00:00",
  "topic": "Topic",
  "model": "gpt-4",
  "conversation": [
    {
      "role": "system",
      "content": "你是一个乐于助人的助手"
    },
    {
      "role": "user",
      "content": "你好"
    }
  ]
}
"""
