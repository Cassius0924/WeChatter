import enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wechatter.database.tables import Base

if TYPE_CHECKING:
    from wechatter.database.tables.gpt_chat_info import GptChatInfo
    from wechatter.database.tables.message import Message


class GptChatRole(enum.Enum):
    """
    GPT聊天角色
    """

    system = "system"
    user = "user"
    assistant = "assistant"


class GptChatMessage(Base):
    """
    GPT对话消息表
    """

    __tablename__ = "gpt_chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("messages.id"), unique=True
    )
    gpt_chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("gpt_chat_infos.id"))
    role: Mapped[GptChatRole]

    message: Mapped["Message"] = relationship(
        "Message", back_populates="gpt_chat_message"
    )
    gpt_chat_info: Mapped["GptChatInfo"] = relationship(
        "GptChatInfo", back_populates="gpt_chat_messages"
    )

    def to_conversation(self):
        return {
            "role": self.role.value,
            "content": self.message.content,
        }
