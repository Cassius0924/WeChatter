from dataclasses import dataclass, field
from typing import List


@dataclass
class PersonInfo:
    """个人消息类"""

    id: str
    name: str
    alias: str = ""
    gender: int = -1
    signature: str = ""
    province: str = ""
    city: str = ""
    phone_list: List[str] = field(default_factory=list)
    is_star: bool = False
