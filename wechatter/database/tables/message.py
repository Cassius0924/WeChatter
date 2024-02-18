import enum
from datetime import datetime
from typing import TYPE_CHECKING, Union

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wechatter.database.tables import Base
from wechatter.database.tables.gpt_chat_message import GptChatMessage

if TYPE_CHECKING:
    from wechatter.database.tables.group import Group
    from wechatter.database.tables.person import Person
    from wechatter.models.wechat import Message as MessageModel


class MessageType(enum.Enum):
    """
    消息类型
    """

    text = "text"
    file = "file"
    urlLink = "urlLink"
    friendship = "friendship"


class Message(Base):
    """
    消息表
    """

    __tablename__ = "message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_id: Mapped[str] = mapped_column(String, ForeignKey("person.id"))
    group_id: Mapped[Union[str, None]] = mapped_column(
        String, ForeignKey("group.id"), nullable=True
    )
    type: Mapped[MessageType]
    content: Mapped[str]
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_mentioned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_quoted: Mapped[bool] = mapped_column(Boolean, default=False)

    person: Mapped["Person"] = relationship("Person", back_populates="messages")
    group: Mapped[Union["Group", None]] = relationship(
        "Group", back_populates="messages"
    )
    gpt_chat_message: Mapped[Union["GptChatMessage", None]] = relationship(
        "GptChatMessage", back_populates="message", uselist=False
    )

    @classmethod
    def from_model(cls, message_model: "MessageModel"):
        group_id = None
        if message_model.is_group:
            group_id = message_model.source.g_info.id

        return cls(
            person_id=message_model.source.p_info.id,
            group_id=group_id,
            type=message_model.type.value,
            content=message_model.content,
            is_mentioned=message_model.is_mentioned,
            is_quoted=message_model.is_quoted,
        )

    # @classmethod
    # def create_gpt_chat_message(
    #     cls,
