from datetime import datetime
from typing import List

from pydantic import BaseModel

from wechatter.models.gpt.gpt_chat_message import GptChatMessage


class GptChatInfo(BaseModel):
    topic: str
    created_time: datetime = datetime.now()
    talk_time: datetime = datetime.now()
    model: str
    is_chatting: bool = True
    # user: User
    gpt_chat_messages: List[GptChatMessage]
