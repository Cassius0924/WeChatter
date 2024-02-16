from typing import List

from pydantic.dataclasses import dataclass


@dataclass
class GroupMemberInfo:
    """群成员类"""

    id: str
    name: str
    alias: str


@dataclass
class GroupInfo:
    """群消息类"""

    id: str
    name: str
    admin_id_list: List[str]
    member_list: List[GroupMemberInfo]
