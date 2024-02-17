import enum

from pydantic import BaseModel

from wechatter.models.wechat.message import Message


class GptChatRole(enum.Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class GptChatMessage(BaseModel):
    gpt_chat_id: int
    role: GptChatRole
    message: Message
