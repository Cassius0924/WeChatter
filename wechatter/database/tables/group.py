from typing import TYPE_CHECKING, List, Union

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wechatter.database.tables import Base
from wechatter.models.wechat import Group as GroupModel

if TYPE_CHECKING:
    from wechatter.database.tables.message import Message
    from wechatter.database.tables.person import Person


class Group(Base):
    """
    微信群表
    """

    __tablename__ = "group"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str]
    alias: Mapped[Union[str, None]] = mapped_column(String, nullable=True)

    members: Mapped[List["Person"]] = relationship(
        "Person",
        secondary="person_group_relation",
        back_populates="groups",
    )
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="group")

    @classmethod
    def from_model(cls, group_model: GroupModel):
        return cls(
            id=group_model.id,
            name=group_model.name,
        )

    def to_model(self) -> GroupModel:
        member_list = []
        for member in self.members:
            member_list.append(member.to_model())
        return GroupModel(
            id=self.id,
            name=self.name,
            member_list=member_list,
        )

    def update(self, group_model: GroupModel):
        self.name = group_model.name
        member_list = []
        for member in self.members:
            member_list.append(Person.from_member_model(member))
        self.members = member_list
