from typing import TYPE_CHECKING, List, Union

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wechatter.database.tables import Base
from wechatter.database.tables.wechat_user import WechatUser
from wechatter.models.message.group_info import GroupInfo

if TYPE_CHECKING:
    from wechatter.database.tables.wechat_message import WechatMessage


class WechatGroup(Base):
    """
    微信群表
    """

    __tablename__ = "wechat_groups"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str]
    alias: Mapped[Union[str, None]] = mapped_column(String, nullable=True)

    members: Mapped[List["WechatUser"]] = relationship(
        "WechatUser",
        secondary="user_group_relations",
        back_populates="groups",
    )
    messages: Mapped[List["WechatMessage"]] = relationship(
        "WechatMessage", back_populates="group"
    )

    @classmethod
    def from_group_info(cls, group_info: GroupInfo):
        return cls(
            id=group_info.id,
            name=group_info.name,
        )
