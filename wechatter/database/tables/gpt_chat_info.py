from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wechatter.database.tables import Base
from wechatter.database.tables.gpt_chat_message import GptChatMessage
from wechatter.database.tables.wechat_message import WechatMessage

if TYPE_CHECKING:
    from wechatter.database.tables.wechat_user import WechatUser


class GptChatInfo(Base):
    """
    GPT聊天表
    """

    __tablename__ = "gpt_chat_infos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("wechat_users.id"))
    topic: Mapped[str]
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    talk_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    model: Mapped[str]
    is_chatting: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["WechatUser"] = relationship(
        "WechatUser", back_populates="gpt_chat_infos"
    )
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
                message=WechatMessage(type="text", content=conversation["content"]),
                gpt_chat_info=self,
            )
            for conversation in conversations
        ]
        self.gpt_chat_messages.extend(conv)
        return self
