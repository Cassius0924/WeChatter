from typing import TYPE_CHECKING, List, Union

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wechatter.database.tables import Base
from wechatter.models.wechat.group_info import GroupInfo

if TYPE_CHECKING:
    from wechatter.database.tables.message import Message
    from wechatter.database.tables.user import User


class Group(Base):
    """
    微信群表
    """

    __tablename__ = "groups"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str]
    alias: Mapped[Union[str, None]] = mapped_column(String, nullable=True)

    members: Mapped[List["User"]] = relationship(
        "User",
        secondary="user_group_relations",
        back_populates="groups",
    )
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="group")

    @classmethod
    def from_group_info(cls, group_info: GroupInfo):
        return cls(
            id=group_info.id,
            name=group_info.name,
        )
