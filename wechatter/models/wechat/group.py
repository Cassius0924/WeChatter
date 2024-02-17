from typing import List

from pydantic import BaseModel


class GroupMember(BaseModel):
    """
    群成员类
    """

    id: str
    name: str
    alias: str


class Group(BaseModel):
    """
    群消息类
    """

    id: str
    name: str
    admin_id_list: List[str]
    member_list: List[GroupMember]
