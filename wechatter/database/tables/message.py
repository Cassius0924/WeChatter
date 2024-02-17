import enum
from datetime import datetime
from typing import TYPE_CHECKING, Union

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wechatter.database.tables import Base
from wechatter.database.tables.gpt_chat_message import GptChatMessage
from wechatter.models.wechat import Message

if TYPE_CHECKING:
    from wechatter.database.tables.group import Group
    from wechatter.database.tables.user import User


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

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    group_id: Mapped[Union[str, None]] = mapped_column(
        String, ForeignKey("groups.id"), nullable=True
    )
    type: Mapped[MessageType]
    content: Mapped[str]
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_mentioned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_quoted: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship("User", back_populates="messages")
    group: Mapped[Union["Group", None]] = relationship(
        "Group", back_populates="messages"
    )
    gpt_chat_message: Mapped[Union["GptChatMessage", None]] = relationship(
        "GptChatMessage", back_populates="message", uselist=False
    )

    @classmethod
    def from_message(cls, message: Message):
        """
        从消息对象构造消息表对象
        """
        if message.is_group:
            group_id = message.source.g_info.id
        else:
            group_id = None

        return cls(
            user_id=message.source.p_info.id,
            group_id=group_id,
            type=message.type.value,
            content=message.content,
            is_mentioned=message.is_mentioned,
            is_quoted=message.is_quoted,
        )

    # @classmethod
    # def create_gpt_chat_message(
    #     cls,
