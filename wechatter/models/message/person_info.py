from typing import List

from pydantic.dataclasses import dataclass


@dataclass
class PersonInfo:
    """个人消息类"""

    id: str
    name: str
    alias: str
    gender: int
    signature: str
    province: str
    city: str
    phone_list: List[str]
    is_star: bool
