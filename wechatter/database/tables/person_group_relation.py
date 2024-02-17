from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from wechatter.database.tables import Base


class PersonGroupRelation(Base):
    """
    用户和群组的关系表
    """

    __tablename__ = "person_group_relation"

    person_id: Mapped[str] = mapped_column(
        String, ForeignKey("person.id"), primary_key=True
    )
    group_id: Mapped[str] = mapped_column(
        String, ForeignKey("group.id"), primary_key=True
    )
