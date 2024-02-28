from typing import List, Optional

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
    # alias: str 目前上游不支持
    admin_id_list: Optional[List[str]] = None
    member_list: List[GroupMember]
    is_gaming: bool = False

    def to_dict(self):
        result = self.__dict__.copy()
        member_list = []
        for member in self.member_list:
            member_list.append(member.__dict__.copy())
        result["member_list"] = member_list
        return result
