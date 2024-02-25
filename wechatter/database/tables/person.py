from typing import TYPE_CHECKING, List, Union

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wechatter.database.tables import Base
from wechatter.models.wechat import Gender, GroupMember, Person as PersonModel

if TYPE_CHECKING:
    from wechatter.database.tables.gpt_chat_info import GptChatInfo
    from wechatter.database.tables.group import Group
    from wechatter.database.tables.message import Message


class Person(Base):
    """
    微信用户表（包括公众号）
    """

    __tablename__ = "person"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str]
    alias: Mapped[Union[str, None]] = mapped_column(String, nullable=True)
    gender: Mapped[Union[Gender, None]] = mapped_column(String, nullable=True)
    province: Mapped[Union[str, None]] = mapped_column(String, nullable=True)
    city: Mapped[Union[str, None]] = mapped_column(String, nullable=True)
    # phone: Mapped[Union[str, None]] = mapped_column(String, nullable=True)
    is_star: Mapped[bool] = mapped_column(Boolean, default=False)
    is_friend: Mapped[bool] = mapped_column(Boolean, default=False)
    is_official_account: Mapped[bool] = mapped_column(Boolean, default=False)

    groups: Mapped[List["Group"]] = relationship(
        "Group",
        secondary="person_group_relation",
        back_populates="members",
    )
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="person")
    gpt_chat_infos: Mapped[List["GptChatInfo"]] = relationship(
        "GptChatInfo", back_populates="person"
    )

    @classmethod
    def from_model(cls, person_model: PersonModel):
        return cls(
            id=person_model.id,
            name=person_model.name,
            alias=person_model.alias,
            gender=person_model.gender.value,
            province=person_model.province,
            city=person_model.city,
            is_star=person_model.is_star,
            is_friend=person_model.is_friend,
            is_official_account=person_model.is_official_account,
        )

    @classmethod
    def from_member_model(cls, member_model: "GroupMember"):
        return cls(
            id=member_model.id,
            name=member_model.name,
            alias=member_model.alias,
        )

    def to_model(self) -> PersonModel:
        return PersonModel(
            id=self.id,
            name=self.name,
            alias=self.alias,
            gender=self.gender,
            signature="",
            province=self.province,
            city=self.city,
            is_star=self.is_star,
            is_friend=self.is_friend,
            is_official_account=self.is_official_account,
        )

    def update(self, person_model: PersonModel):
        self.name = person_model.name
        self.alias = person_model.alias
        self.gender = person_model.gender.value
        self.province = person_model.province
        self.city = person_model.city
        self.is_star = person_model.is_star
        self.is_friend = person_model.is_friend
        self.is_official_account = person_model.is_official_account
