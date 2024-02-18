import enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from wechatter.models.gpt.gpt_chat_info import GptChatInfo
    from wechatter.models.wechat import Message


class GptChatRole(enum.Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class GptChatMessage(BaseModel):
    id: Optional[int] = None
    message: "Message"
    gpt_chat_info: "GptChatInfo"
    gpt_response: str

    def to_turn(self):
        return [
            {
                "role": GptChatRole.user.value,
                "content": self.message.content,
            },
            {
                "role": GptChatRole.assistant.value,
                "content": self.gpt_response,
            },
        ]
