from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wechatter.database.tables import Base
from wechatter.database.tables.gpt_chat_message import GptChatMessage
from wechatter.models.gpt import (
    GptChatInfo as GptChatInfoModel,
    GptChatMessage as GptChatMessageModel,
)

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
    model: Mapped[str]
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now()
    )
    talk_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=datetime.now()
    )
    is_chatting: Mapped[bool] = mapped_column(Boolean, default=True)

    person: Mapped["Person"] = relationship("Person", back_populates="gpt_chat_infos")
    gpt_chat_messages: Mapped[List["GptChatMessage"]] = relationship(
        "GptChatMessage", back_populates="gpt_chat_info"
    )

    @classmethod
    def from_model(cls, gpt_chat_info_model: GptChatInfoModel):
        gpt_chat_messages = []
        for message in gpt_chat_info_model.gpt_chat_messages:
            gpt_chat_messages.append(GptChatMessage.from_model(message))

        return cls(
            id=gpt_chat_info_model.id,
            person_id=gpt_chat_info_model.person.id,
            topic=gpt_chat_info_model.topic,
            model=gpt_chat_info_model.model,
            created_time=gpt_chat_info_model.created_time,
            talk_time=gpt_chat_info_model.talk_time,
            is_chatting=gpt_chat_info_model.is_chatting,
            gpt_chat_messages=gpt_chat_messages,
        )

    def to_model(self) -> GptChatInfoModel:
        gpt_chat_info = GptChatInfoModel(
            id=self.id,
            person=self.person.to_model(),
            topic=self.topic,
            model=self.model,
            created_time=self.created_time,
            talk_time=self.talk_time,
            is_chatting=self.is_chatting,
        )

        gpt_chat_messages = []
        for message in self.gpt_chat_messages:
            gpt_chat_messages.append(
                GptChatMessageModel(
                    id=message.id,
                    message=message.message.to_model(),
                    gpt_chat_info=gpt_chat_info,
                    gpt_response=message.gpt_response,
                    # role=message.role.value,
                )
            )
        gpt_chat_info.gpt_chat_messages = gpt_chat_messages

        return gpt_chat_info
