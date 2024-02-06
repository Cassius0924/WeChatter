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


# class GroupMemberInfo:
#     """群成员类"""

#     def __init__(
#         self,
#         id: str,
#         name: str,
#         alias: str = "",
#     ):
#         self.id = id
#         self.name = name
#         self.alias = alias

#     def __str__(self) -> str:
#         return f"微信ID：{self.id}\n昵称：{self.name}\n备注：{self.alias}"


# class GroupInfo:
#     """群消息类"""

#     def __init__(
#         self,
#         id: str,
#         name: str,
#         admin_id_list: List[str] = [],
#         member_list: List[dict] = [],
#     ):
#         self.id = id
#         self.name = name
#         self.admin_id_list = admin_id_list
#         self.member_list = member_list

#     @property
#     def admin_id_list(self) -> List[str]:
#         """获取管理员ID列表"""
#         return self.__admin_id_list

#     @admin_id_list.setter
#     def admin_id_list(self, admin_id_list: List[str]):
#         self.__admin_id_list = admin_id_list

#     @property
#     def member_list(self) -> List[GroupMemberInfo]:
#         """获取群成员列表"""
#         return self.__member_list

#     @member_list.setter
#     def member_list(self, member_list: List[dict]):
#         self.__member_list = []
#         for m in member_list:
#             self.__member_list.append(
#                 GroupMemberInfo(
#                     id=m["id"],
#                     name=m["name"],
#                     alias=m["alias"],
#                 )
#             )

#     def __str__(self) -> str:
#         # 群成员数量过多，不打印
#         # member_list_str = "[\n{}\n]".format('\n'.join([str(m) for m in self.member_list]))
#         # return f"群ID: {self.id}\n群名：{self.name}\n管理员：{self.admin_id_list}\n成员：{member_list_str}"
#         return f"群ID: {self.id}\n群名：{self.name}\n管理员：{self.admin_id_list}\n成员：{str(self.member_list)}"
