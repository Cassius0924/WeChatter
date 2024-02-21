from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wechatter.database.tables import Base
from wechatter.models.gpt import GptChatMessage as GptChatMessageModel

if TYPE_CHECKING:
    from wechatter.database.tables.gpt_chat_info import GptChatInfo
    from wechatter.database.tables.message import Message


class GptChatMessage(Base):
    """
    GPT对话消息表
    """

    __tablename__ = "gpt_chat_message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("message.id"), unique=True
    )
    gpt_chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("gpt_chat_info.id"))
    gpt_response: Mapped[str]

    message: Mapped["Message"] = relationship(
        "Message", back_populates="gpt_chat_message"
    )
    gpt_chat_info: Mapped["GptChatInfo"] = relationship(
        "GptChatInfo", back_populates="gpt_chat_messages"
    )

    @classmethod
    def from_model(cls, gpt_chat_message_model: GptChatMessageModel):
        return cls(
            message_id=gpt_chat_message_model.message.id,
            gpt_chat_id=gpt_chat_message_model.gpt_chat_info.id,
            gpt_response=gpt_chat_message_model.gpt_response,
        )

    def to_model(self) -> GptChatMessageModel:
        return GptChatMessageModel(
            id=self.id,
            message=self.message.to_model(),
            gpt_chat_info=self.gpt_chat_info.to_model(),
            gp_response=self.gpt_response,
        )
