# 消息类
import json
from enum import Enum
from typing import List, Union


# 消息类型枚举
class MessageType(Enum):
    TEXT = 0
    FILE = 1
    LINK = 2
    # TODO: 图片识别
    # IMAGE = 3


# 消息来源枚举
class MessageSender(Enum):
    PERSONAL = 0
    GROUP = 1
    # TODO: 文件传输助手
    # FILE_HELPER = 2
    # TODO: 微信运动
    # WECHAT_SPORT = 3


# 个人消息类
class PersonalInfo:
    def __init__(
        self,
        id: str,
        name: str,
        alias: str = "",
        gender: str = "",
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


# 群成员类
class GroupMemberInfo:
    def __init__(
        self,
        id: str,
        name: str,
        alias: str = "",
    ):
        self.id = id
        self.name = name
        self.alias = alias

    def __str__(self) -> str:
        return f"微信ID：{self.id}\n昵称：{self.name}\n备注：{self.alias}"


# 群消息类
class GroupInfo:
    def __init__(
        self,
        id: str,
        name: str,
        admin_id_list: List[str] = [],
        member_list: List[dict] = [],
    ):
        self.id = id
        self.name = name
        self.admin_id_list = admin_id_list
        self.member_list = member_list

    @property
    def admin_id_list(self) -> List[str]:
        return self._admin_id_list

    @admin_id_list.setter
    def admin_id_list(self, admin_id_list: List[str]):
        self._admin_id_list = admin_id_list

    @property
    def member_list(self) -> List[GroupMemberInfo]:
        return self._member_list

    @member_list.setter
    def member_list(self, member_list: List[dict]):
        self._member_list = []
        for m in member_list:
            self._member_list.append(
                GroupMemberInfo(
                    id=m["id"],
                    name=m["name"],
                    alias=m["alias"],
                )
            )

    def __str__(self) -> str:
        # 群成员数量过多，不打印
        # member_list_str = "[\n{}\n]".format('\n'.join([str(m) for m in self.member_list]))
        # return f"群ID: {self.id}\n群名：{self.name}\n管理员：{self.admin_id_list}\n成员：{member_list_str}"
        return f"群ID: {self.id}\n群名：{self.name}\n管理员：{self.admin_id_list}\n成员：{str(self.member_list)}"


# 消息来源类
class MessageSource:
    def __init__(
        self,
        p_info: Union[PersonalInfo, None] = None,
        g_info: Union[GroupInfo, None] = None,
    ):
        self.p_info = p_info
        self.g_info = g_info

    def __str__(self) -> str:
        if self.p_info is not None:
            return str(self.p_info)
        elif self.g_info is not None:
            return str(self.g_info)
        else:
            return "None"


# 消息类，将消息内容、发送者名字、是否群消息、群数据封装成类
class Message:
    def __init__(
        self,
        type: str,
        content: str,
        source: str,
        is_mentioned: str = "0",
    ):
        self.type = type
        self.content = content
        self.source = source
        self.is_mentioned = is_mentioned

    @property
    def type(self) -> MessageType:
        return self._type

    @type.setter
    def type(self, type: str):
        if type == "text":
            self._type = MessageType.TEXT
        elif type == "file":
            self._type = MessageType.FILE
        elif type == "urlLink":
            self._type = MessageType.LINK
        else:
            raise ValueError("消息类型错误")

    # 获取消息内容
    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def source(self) -> MessageSource:
        return self._source

    @source.setter
    def source(self, source_json_str: str):
        if source_json_str == "":
            self._source = MessageSource()
            return
        # 解析json
        source_json = dict()
        try:
            source_json = json.loads(source_json_str)
        except json.JSONDecodeError as e:
            print("消息来源解析失败")
            raise e
        # 判断是群还是个人
        if source_json["room"] != "":  # 群消息
            g_data = source_json["room"]
            id = g_data["id"]
            name = g_data.get("topic", "")
            admin_id_list = g_data.get("payload", {}).get("adminIdList", [])
            member_list = g_data.get("payload", {}).get("memberList", [])
            self._source = MessageSource(
                g_info=GroupInfo(
                    id=id,
                    name=name,
                    admin_id_list=admin_id_list,
                    member_list=member_list,
                )
            )
        elif source_json["from"] != "":  # 个人消息
            payload = source_json.get("from").get("payload", {})
            if payload == {}:
                self._source = MessageSource()
                return
            id = payload.get("id", "")
            name = payload.get("name", "")
            alias = payload.get("alias", "")
            gender = payload.get("gender", "")
            signature = payload.get("signature", "")
            province = payload.get("province", "")
            city = payload.get("city", "")
            phone_list = payload.get("phone", [])
            is_star = payload.get("star", "")
            self._source = MessageSource(
                p_info=PersonalInfo(
                    id=id,
                    name=name,
                    alias=alias,
                    gender=gender,
                    signature=signature,
                    province=province,
                    city=city,
                    phone_list=phone_list,
                    is_star=is_star,
                )
            )
        else:
            self._source = MessageSource()

    @property
    def is_mentioned(self):
        return self._is_mentioned

    @is_mentioned.setter
    def is_mentioned(self, is_mentioned: str):
        if is_mentioned == "1":
            self._is_mentioned = True
        else:
            self._is_mentioned = False

    def __str__(self) -> str:
        return f"消息内容：{self.content}\n消息来源：\n{self.source}\n是否@：{self.is_mentioned}"

    # @property
    # def is_command(self):
    #     return self.content.startswith("/")

    # @property
    # def is_group_command(self):
    #     return self.is_command and self.is_group


"""
  {
    // 消息来自群，会有以下对象，否则为空字符串
    "room": {
      "id": "@@xxx",
      "topic": "abc" // 群名
      "payload": {
        "adminIdList": [],
        "memberList": [{
            id: '@xxxx',
            name:'昵称',
            alias: '备注名'
           }
        ]
      },
    },

    // 消息来自个人，会有以下对象，否则为空字符串
    "to": {
        "id": "@xxx",
        "payload": {
            "alias": "", //备注名
            "gender": 1,
            "name": "xxx",
            "phone": [],
            "signature": "hard mode",
            "star": false,
            "type": 1
        },
      },

    // 消息发送方
    "from": {
      "id": "@xxx",
      "payload": {
        "alias": "",
        "city": "北京",
        "gender": 1,
        "id": "@xxxx",
        "name": "abc", //昵称
        "phone": [],
        "province": "北京",
        "star": false,
        "type": 1
      },
    }

  }
"""
