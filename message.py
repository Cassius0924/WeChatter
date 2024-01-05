# 消息类
import json
import re
from enum import Enum
from typing import List, Union
from bot_info import BotInfo

from command.command_set import cmd_dict


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
        return self.__admin_id_list

    @admin_id_list.setter
    def admin_id_list(self, admin_id_list: List[str]):
        self.__admin_id_list = admin_id_list

    @property
    def member_list(self) -> List[GroupMemberInfo]:
        return self.__member_list

    @member_list.setter
    def member_list(self, member_list: List[dict]):
        self.__member_list = []
        for m in member_list:
            self.__member_list.append(
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


# 消息类
# msg: 消息内容
# source: 消息来源
# is_mentioned: 是否@机器人
# is_quote: 是否引用机器人消息
# is_cmd: 是否是命令
# cmd: 命令
# cmd_desc: 命令描述
# cmd_value: 命令值


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
        self.__parse_command()

    # 获取消息类型
    @property
    def type(self) -> MessageType:
        return self.__type

    @type.setter
    def type(self, type: str):
        if type == "text":
            self.__type = MessageType.TEXT
        elif type == "file":
            self.__type = MessageType.FILE
        elif type == "urlLink":
            self.__type = MessageType.LINK
        else:
            raise ValueError("消息类型错误")

    # 获取消息内容
    @property
    def msg(self) -> str:
        return self.__msg

    # 获取消息来源
    @property
    def source(self) -> MessageSource:
        return self.__source

    @source.setter
    def source(self, source_json_str: str):
        if source_json_str == "":
            self.__source = MessageSource()
            return
        # 解析json
        source_json = dict()
        try:
            source_json = json.loads(source_json_str)
        except json.JSONDecodeError as e:
            print("消息来源解析失败")
            raise e

        message_source = MessageSource()
        # from为发送者信息，无论是个人消息还是群消息，都有from
        if source_json["from"] != "":
            payload = source_json.get("from").get("payload", {})
            if payload == {}:
                self.__source = MessageSource()
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
            message_source.p_info = PersonalInfo(
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
        # room为群信息，只有群消息才有room
        if source_json["room"] != "":
            g_data = source_json["room"]
            id = g_data["id"]
            payload = g_data.get("payload", {})
            name = payload.get("topic", "")
            admin_id_list = payload.get("adminIdList", [])
            member_list = payload.get("memberList", [])
            message_source.g_info = GroupInfo(
                id=id,
                name=name,
                admin_id_list=admin_id_list,
                member_list=member_list,
            )
        self.__source = message_source

    # 解析命令
    def __parse_command(self) -> None:
        # 判断是否为引用消息
        quote_pattern = (
            r"(?s)「(.*?)」\n- - - - - - - - - - - - - - -"  # 引用消息的正则
        )
        match_result = re.match(quote_pattern, self.content)
        self.__is_quote = bool(match_result)
        # 判断是否为群消息
        self.__is_group = bool(self.source.g_info)
        # 不带命令前缀和@前缀的消息内容
        self.__msg = ""
        content = self.content
        if self.__is_mentioned and self.__is_group:
            # 去掉"@机器人名"的前缀
            content = content.replace(f"@{BotInfo.name} ", "")
        for cmd, value in cmd_dict.items():
            for key in value["keys"]:
                # 第一个空格前的内容即为指令
                cont_list = content.split(" ", 1)
                if cont_list[0].lower() == "/" + key.lower():
                    self.__is_cmd = True  # 是否是命令
                    self.__cmd = cmd  # 命令
                    if len(cont_list) == 2:
                        self.__msg = cont_list[1]  # 消息内容
                    return
        self.__is_cmd = False
        self.__cmd = "None"

    @property
    def is_mentioned(self) -> bool:
        return self.__is_mentioned

    @is_mentioned.setter
    def is_mentioned(self, is_mentioned: str):
        if is_mentioned == "1":
            self.__is_mentioned = True
        else:
            self.__is_mentioned = False

    @property
    def is_command(self) -> bool:
        return self.__is_cmd

    @property
    def cmd(self) -> str:
        return self.__cmd

    @property
    def cmd_desc(self) -> str:
        return cmd_dict[self.cmd]["desc"]

    @property
    def cmd_value(self) -> int:
        return cmd_dict[self.cmd]["value"]

    @property
    def is_group(self) -> bool:
        return self.__is_group

    @property
    def is_quote(self) -> bool:
        if not self.__is_quote:
            return False
        bot_name = BotInfo.name
        if bot_name == "":
            print("机器人名字为空")
            return False
        if self.content.startswith(f"「{bot_name}"):
            return True
        return False

    def __str__(self) -> str:
        return f"消息内容：{self.content}\n消息来源：\n{self.source}\n是否@：{self.is_mentioned}\n是否引用：{self.is_quote}"


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
