from datetime import datetime

from wechatter.config import config
from ..handlers import command
from ...models.wechat import SendTo
from ..basechat import BaseChat, DEFAULT_CONVERSATION
from wechatter.models.gpt import GptChatInfo
from ...utils import post_request_json
from wechatter.database import (
    GptChatInfo as DbGptChatInfo,
    GptChatMessage as DbGptChatMessage,
    make_db_session,
)

this_model = config["spark_model"]


class SparkChat(BaseChat):
    def __init__(self):
        super().__init__(
            model=this_model,
            api_url=config["spark_api"],
            token="Bearer " + config["spark_token"]
        )

    def _chat(self, chat_info: GptChatInfo, message: str, message_obj, is_save: bool) -> str:
        """
        持续对话
        :param chat_info: 对话信息
        :param message: 用户消息
        :param message_obj: 消息对象
        :param is_save: 是否保存此轮对话记录
        :return: GPT 回复
        """
        newconv = [{"role": "user", "content": message}]
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
        }
        json = {
            "model": chat_info.model,
            "messages": DEFAULT_CONVERSATION + chat_info.get_conversation() + newconv,
        }
        r_json = post_request_json(url=self.api_url, headers=headers, json=json, timeout=60)

        if "error" in r_json in r_json:
            raise ValueError(f"服务返回值错误: {r_json}")

        msg = r_json["choices"][0]["message"]
        msg_content = msg.get("content", "调用服务失败")
        if is_save:
            newconv.append({"role": "assistant", "content": msg_content})
            chat_info.extend_conversation(newconv)
            with make_db_session() as session:
                _chat_info = session.query(DbGptChatInfo).filter_by(id=chat_info.id).first()
                _chat_info.talk_time = datetime.now()
                for chat_message in chat_info.gpt_chat_messages[-len(newconv) // 2:]:
                    _chat_message = DbGptChatMessage.from_model(chat_message)
                    _chat_message.message_id = message_obj.id
                    _chat_info.gpt_chat_messages.append(_chat_message)
                session.commit()
        return msg_content


SparkChat = SparkChat()


@command(
    command="spark",
    keys=["spark", "spark_chat"],
    desc="与 Spark AI 聊天",
)
def spark_command_handler(to: SendTo, message: str = "", message_obj=None) -> None:
    SparkChat.gptx(this_model, to, message, message_obj)


@command(
    command="spark-chats",
    keys=["spark-chats", "spark对话记录"],
    desc="列出Spark对话记录。",
)
def spark_chats_command_handler(to: SendTo, message: str = "", message_obj=None) -> None:
    SparkChat.gptx_chats(this_model, to, message, message_obj)


@command(
    command="spark-record",
    keys=["spark-record", "spark记录"],
    desc="获取Spark对话记录。",
)
def spark_record_command_handler(
        to: SendTo, message: str = "", message_obj=None
) -> None:
    SparkChat.gptx_record(this_model, to, message)


@command(
    command="spark-continue",
    keys=["spark-continue", "spark继续"],
    desc="继续Spark对话。",
)
def spark_continue_command_handler(
        to: SendTo, message: str = "", message_obj=None
) -> None:
    SparkChat.gptx_continue(this_model, to, message)
