import json
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wechatter.database.tables import Base
from wechatter.models.game.game_states import GameStates as GameStatesModel
from wechatter.utils.unique_list import UniqueListDecoder, UniqueListEncoder

if TYPE_CHECKING:
    from wechatter.database.tables.group import Group
    from wechatter.database.tables.person import Person


class GameStates(Base):
    """
    游戏状态表
    """

    __tablename__ = "game_states"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    host_person_id: Mapped[str] = mapped_column(String, ForeignKey("person.id"))
    host_group_id: Mapped[str] = mapped_column(
        String, ForeignKey("group.id"), nullable=True
    )
    game_class_name: Mapped[str] = mapped_column(String)
    states: Mapped[str] = mapped_column(String)
    is_over: Mapped[bool] = mapped_column(Boolean, default=False)
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    host_person: Mapped["Person"] = relationship(
        "Person", back_populates="game_states_list"
    )
    host_group: Mapped["Group"] = relationship(
        "Group", back_populates="game_states_list"
    )

    @classmethod
    def from_model(cls, game_states_model: GameStatesModel):
        group_id = None
        if game_states_model.host_group:
            group_id = game_states_model.host_group.id
        return cls(
            id=game_states_model.id,
            host_person_id=game_states_model.host_person.id,
            host_group_id=group_id,
            game_class_name=game_states_model.game_class_name,
            states=json.dumps(game_states_model.states, cls=UniqueListEncoder),
            create_time=game_states_model.create_time,
            is_over=game_states_model.is_over,
        )

    def to_model(self) -> GameStatesModel:
        host_group = None
        if self.host_group:
            host_group = self.host_group.to_model()
        return GameStatesModel(
            id=self.id,
            host_person=self.host_person.to_model(),
            host_group=host_group,
            game_class_name=self.game_class_name,
            states=json.loads(self.states, cls=UniqueListDecoder),
            create_time=self.create_time,
            is_over=self.is_over,
        )

    def update(self, game_states_model: GameStatesModel):
        group_id = None
        if game_states_model.host_group:
            group_id = game_states_model.host_group.id
        self.host_person_id = game_states_model.host_person.id
        self.host_group_id = group_id
        self.game_class_name = game_states_model.game_class_name
        self.states = json.dumps(game_states_model.states, cls=UniqueListEncoder)
        self.create_time = game_states_model.create_time
        self.is_over = game_states_model.is_over
        return self
