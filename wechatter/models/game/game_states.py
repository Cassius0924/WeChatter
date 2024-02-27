from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel

from wechatter.models.wechat import Group, Person


class GameStates(BaseModel):
    id: Optional[int] = None
    host_person: Person
    host_group: Optional[Group] = None
    game_class_name: str
    states: Dict
    create_time: datetime = datetime.now()
    is_over: bool = False
