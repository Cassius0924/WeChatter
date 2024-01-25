from typing import List


class PersonInfo:
    """个人消息类"""

    def __init__(
        self,
        id: str,
        name: str,
        alias: str = "",
        gender: int = -1,
        signature: str = "",
        province: str = "",
        city: str = "",
        phone_list: List[str] = [],
        is_star: bool = False,
    ):
        self.id = id
        self.name = name
        self.alias = alias
        self.gender = gender
        self.signature = signature
        self.province = province
        self.city = city
        self.phone_list = phone_list
        self.is_star = is_star

    def __str__(self) -> str:
        return f"ID: {self.id}\n昵称：{self.name}\n备注：{self.alias}\n性别：{self.gender}\n签名：{self.signature}\n手机：{self.phone_list}\n星标：{self.is_star}"
