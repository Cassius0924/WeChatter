from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from wechatter.database.tables import Base
from wechatter.models.wechat import QuotedResponse as QuotedResponseModel


class QuotedResponse(Base):
    """
    引用回复表
    """

    __tablename__ = "quoted_response"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quotable_id: Mapped[str] = mapped_column(String(10))
    command: Mapped[str]
    response: Mapped[str]

    @classmethod
    def from_model(cls, model: QuotedResponseModel):
        return cls(
            id=model.id,
            quotable_id=model.quotable_id,
            command=model.command,
            response=model.response,
        )

    def to_model(self) -> QuotedResponseModel:
        return QuotedResponseModel(
            id=self.id,
            quotable_id=self.quotable_id,
            command=self.command,
            response=self.response,
        )
