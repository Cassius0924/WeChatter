import enum

from pydantic import BaseModel


class Gender(enum.Enum):
    """
    性别类
    """

    male = "male"
    female = "female"
    unknown = "unknown"


class Person(BaseModel):
    """
    个人消息类
    """

    id: str
    name: str
    alias: str
    gender: Gender
    signature: str
    province: str
    city: str
    # phone_list: List[str]
    is_star: bool
    is_friend: bool
