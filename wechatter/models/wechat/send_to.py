from typing import Optional

from loguru import logger
from pydantic import BaseModel, computed_field

from wechatter.models.wechat.group import Group
from wechatter.models.wechat.person import Person


class SendTo(BaseModel):
    """
    发送对象类
    """

    person: Person
    group: Optional[Group] = None

    @computed_field
    @property
    def p_id(self) -> str:
        return self.person.id

    @computed_field
    @property
    def p_name(self) -> str:
        return self.person.name

    @computed_field
    @property
    def p_alias(self) -> str:
        return self.person.alias

    @computed_field
    @property
    def g_id(self) -> Optional[str]:
        try:
            return self.group.id
        except AttributeError:
            logger.warning("此发送对象不是群聊")
            return None

    @computed_field
    @property
    def g_name(self) -> Optional[str]:
        try:
            return self.group.name
        except AttributeError:
            logger.warning("此发送对象不是群聊")
            return None
