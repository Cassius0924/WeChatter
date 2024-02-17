from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wechatter.database.tables import Base
from wechatter.database.tables.gpt_chat_message import GptChatMessage
from wechatter.database.tables.message import Message

if TYPE_CHECKING:
    from wechatter.database.tables.person import Person


class GptChatInfo(Base):
    """
    GPT聊天表
    """

    __tablename__ = "gpt_chat_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_id: Mapped[str] = mapped_column(String, ForeignKey("person.id"))
    topic: Mapped[str]
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now()
    )
    # 改名为 updated_time
    talk_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=datetime.now()
    )
    model: Mapped[str]
    is_chatting: Mapped[bool] = mapped_column(Boolean, default=True)

    person: Mapped["Person"] = relationship("Person", back_populates="gpt_chat_infos")
    gpt_chat_messages: Mapped[List["GptChatMessage"]] = relationship(
        "GptChatMessage", back_populates="gpt_chat_info"
    )

    def get_conversations(self):
        return [message.to_conversation() for message in self.gpt_chat_messages]

    def extend_conversations(self, conversations: List):
        conv = [
            GptChatMessage(
                gpt_chat_id=self.id,
                role=conversation["role"],
                message=Message(type="text", content=conversation["content"]),
                gpt_chat_info=self,
            )
            for conversation in conversations
        ]
        self.gpt_chat_messages.extend(conv)
        return self
