from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from wechatter.database.tables import Base


class UserGroupRelation(Base):
    """
    用户和群组的关系表
    """

    __tablename__ = "user_group_relations"

    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id"), primary_key=True
    )
    group_id: Mapped[str] = mapped_column(
        String, ForeignKey("groups.id"), primary_key=True
    )
