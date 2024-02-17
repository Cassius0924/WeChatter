import enum
from typing import TYPE_CHECKING, List, Union

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wechatter.database.tables import Base
from wechatter.models.wechat.person_info import PersonInfo

if TYPE_CHECKING:
    from wechatter.database.tables.gpt_chat_info import GptChatInfo
    from wechatter.database.tables.group import Group
    from wechatter.database.tables.message import Message


class Gender(enum.Enum):
    """
    性别表
    """

    # 用命名小写，否则sqlalchemy会报错
    male = "male"
    female = "female"
    unknown = "unknown"


class User(Base):
    """
    微信用户表
    """

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str]
    alias: Mapped[Union[str, None]] = mapped_column(String, nullable=True)
    gender: Mapped[Union[Gender, None]]
    province: Mapped[Union[str, None]]
    city: Mapped[Union[str, None]]
    # phone: Mapped[Union[str, None]] = mapped_column(String, nullable=True)
    is_star: Mapped[bool] = mapped_column(Boolean, default=False)
    is_friend: Mapped[bool] = mapped_column(Boolean, default=False)

    groups: Mapped[List["Group"]] = relationship(
        "Group",
        secondary="user_group_relations",
        back_populates="members",
    )
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="user")
    gpt_chat_infos: Mapped[List["GptChatInfo"]] = relationship(
        "GptChatInfo", back_populates="user"
    )

    @classmethod
    def from_person_info(cls, person_info: PersonInfo):
        return cls(
            id=person_info.id,
            name=person_info.name,
            alias=person_info.alias,
            gender=person_info.gender.value,
            province=person_info.province,
            city=person_info.city,
            is_star=person_info.is_star,
            is_friend=person_info.is_friend,
        )

    @classmethod
    def from_member_info(cls, member_info: PersonInfo):
        return cls(
            id=member_info.id,
            name=member_info.name,
            alias=member_info.alias,
        )
