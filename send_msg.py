# 消息发送类
from enum import Enum
from typing import List
import requests

from message import MessageSource
from main import cr


# 发送对象类
class SendTo:
    def __init__(self, source: MessageSource):
        self.p_name = ""
        self.g_name = ""
        if source.p_info is not None:
            self.p_name = source.p_info.name
        if source.g_info is not None:
            self.g_name = source.g_info.name


# 发送消息类型枚举
class SendMessageType(Enum):
    TEXT = "text"
    FILE_URL = "fileUrl"


# 发送消息类
class SendMessage:
    def __init__(self, type: SendMessageType, content: str):
        self.type = type.value
        self.content = content


# 发送消息列表类，用于给同一个对象发送多条消息
class SendMessageList:
    def __init__(self):
        self.messages: List[SendMessage] = []

    def add(self, message: SendMessage):
        self.messages.append(message)


# 检查发送状态
"""
response: {
"success": true,
"message": "",
"task": {
    "successCount": 0,
    "totalCount": 0,
    "failedCount": 0,
    "reject": [],
    "sentFailed": [],
    "notFound": []
}
"""


def _check(response: requests.Response) -> bool:
    if response.status_code != 200:
        print(f"发送消息失败，状态码：{response.status_code}")
        return False
    result = response.json()
    # 即使code为200，也需要检查success字段
    task = result["task"]
    if not result["success"] or not task["successCount"] == task["totalCount"]:
        print(f"发送消息失败，错误信息：{result['message']}")
        return False
    # 部分成功
    if task["successCount"] > 0 and task["successCount"] < task["totalCount"]:
        print(
            f"发送消息部分成功，成功数：{task['successCount']}, 失败数：{task['failedCount']}"
        )
        return True
    return True


# v2 版本 api 消息发送类
class Sender:
    host = "http://localhost"
    url = f"{host}:{cr.send_port}/webhook/msg/v2"

    # 发送文本消息或链接文件
    """
    curl --location 'http://localhost:3001/webhook/msg/v2' \
    --header 'Content-Type: application/json' \
    --data '{
        "to": "testUser",
        "ioRoom": false,
        "data": { 
            "type": "text",
            "content": "你好👋"
        }
    }'
    curl --location --request POST 'http://localhost:3001/webhook/msg/v2' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "to": "testGroup",
        "type": "fileUrl",
        "content": "https://samplelib.com/lib/preview/mp3/sample-3s.mp3",
        "isRoom": true
    }'
    """

    @staticmethod
    def send_msg(to: SendTo, message: SendMessage) -> bool:
        # 群消息
        if to.g_name != "":
            message.content = f"@{to.p_name}\n{message.content}"
            return Sender.send_msg_g(to.g_name, message)
        # 个人消息
        else:
            return Sender.send_msg_p(to.p_name, message)

    # 发送给个人
    @staticmethod
    def send_msg_p(to_p_name: str, message: SendMessage) -> bool:
        headers = {"Content-Type": "application/json"}
        data = {
            "to": to_p_name,
            "isRoom": False,
            "data": {"type": message.type, "content": message.content},
        }
        return _check(requests.post(Sender.url, headers=headers, json=data))

    # 发送给群组
    @staticmethod
    def send_msg_g(to_g_name: str, message: SendMessage) -> bool:
        headers = {"Content-Type": "application/json"}
        data = {
            "to": to_g_name,
            "isRoom": True,
            "data": {"type": message.type, "content": message.content},
        }
        return _check(requests.post(Sender.url, headers=headers, json=data))

    # 给同一个对象发送多条消息
    """
    curl --location 'http://localhost:3001/webhook/msg' \
    --header 'Content-Type: application/json' \
    --data '{
        "to": "testUser",
        "data": [
            {
                "type": "text",
                "content": "你好👋"
            },
            {
                "type": "fileUrl",
                "content": "https://samplelib.com/lib/preview/mp3/sample-3s.mp3"
            }
        ]
    }'
    """

    @staticmethod
    def send_msgs(to: SendTo, messages: SendMessageList) -> bool:
        if to.g_name != "":
            return Sender.send_msgs_g(to.g_name, messages)
        else:
            return Sender.send_msgs_p(to.p_name, messages)

    # 给同一个人发送多条消息
    @staticmethod
    def send_msgs_p(to_p_name: str, messages: SendMessageList) -> bool:
        headers = {"Content-Type": "application/json"}
        data = {"to": to_p_name, "isRoom": False, "data": []}
        for message in messages.messages:
            msg = {"type": message.type, "content": message.content}
            data["data"].append(msg)
        return _check(requests.post(Sender.url, headers=headers, json=data))

    # 给同一个群组发送多条消息
    @staticmethod
    def send_msgs_g(to_g_name: str, messages: SendMessageList) -> bool:
        headers = {"Content-Type": "application/json"}
        data = {"to": to_g_name, "isRoom": True, "data": []}
        for message in messages.messages:
            msg = {"type": message.type, "content": message.content}
            data["data"].append(msg)
        return _check(requests.post(Sender.url, headers=headers, json=data))

    # 给多个人发送一条消息（群发）
    """
    curl --location 'http://localhost:3001/webhook/msg/v2' \
    --header 'Content-Type: application/json' \
    --data '[
        {
            "to": "testUser1",
            "data": {
                "content": "你好👋"
            }
        },
        {
            "to": "testUser2",
            "data": {
                "content": "你好👋"
              },
        }
    ]'
    """

    # 给多个人发送一条消息
    @staticmethod
    def send_msg_ps(to_p_names: List[str], message: SendMessage) -> bool:
        headers = {"Content-Type": "application/json"}
        data = []
        for to_p_name in to_p_names:
            msg = {
                "to": to_p_name,
                "isRoom": False,
                "data": {"type": message.type, "content": message.content},
            }
            data.append(msg)
        return _check(requests.post(Sender.url, headers=headers, json=data))

    # 给多个群组发送一条消息
    @staticmethod
    def send_msg_gs(to_g_names: List[str], message: SendMessage) -> bool:
        headers = {"Content-Type": "application/json"}
        data = []
        for to_g_name in to_g_names:
            msg = {
                "to": to_g_name,
                "isRoom": True,
                "data": {"type": message.type, "content": message.content},
            }
            data.append(msg)
        return _check(requests.post(Sender.url, headers=headers, json=data))

    # TODO: 给多个人发送多条消息

    # 本地文件发送
    """
    curl --location --request POST 'http://localhost:3001/webhook/msg' \
    --form 'to=testGroup' \
    --form content=@"$HOME/demo.jpg" \
    --form 'isRoom=1'
    """

    @staticmethod
    def send_localfile_msg(to: SendTo, file_path: str) -> bool:
        if to.g_name != "":
            return Sender.send_localfile_msg_g(to.g_name, file_path)
        else:
            return Sender.send_localfile_msg_p(to.p_name, file_path)

    @staticmethod
    def send_localfile_msg_p(to_p_name: str, file_path: str) -> bool:
        url = "http://localhost:3001/webhook/msg"
        data = {"to": to_p_name, "isRoom": 0}
        files = {"content": open(file_path, "rb")}
        return _check(requests.post(url, data=data, files=files))

    @staticmethod
    def send_localfile_msg_g(to_g_name: str, file_path: str) -> bool:
        url = "http://localhost:3001/webhook/msg"
        data = {"to": to_g_name, "isRoom": 1}
        files = {"content": open(file_path, "rb")}
        return _check(requests.post(url, data=data, files=files))


# v1 版本 api 消息发送类
class SenderV1:
    host = "http://localhost"
    url = f"{host}:{cr.send_port}/webhook/msg"

    # 发送文本消息
    """
    curl --location --request POST 'http://localhost:3001/webhook/msg' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "to": "testUser",
        "type": "text",
        "content": "Hello World!"
    }'
    """

    @staticmethod
    def send_text_msg(to: SendTo, message: str) -> None:
        # 群消息
        if to.g_name != "":
            message = f"@{to.p_name}\n{message}"
            SenderV1.send_text_msg_g(to.g_name, message)
        # 个人消息
        else:
            SenderV1.send_text_msg_p(to.p_name, message)

    # 发送给个人
    @staticmethod
    def send_text_msg_p(to_p_name: str, message: str) -> None:
        url = "http://localhost:3001/webhook/msg"
        headers = {"Content-Type": "application/json"}
        data = {"to": to_p_name, "type": "text", "content": message}
        requests.post(url, headers=headers, json=data)

    # 发送给群组
    @staticmethod
    def send_text_msg_g(to_g_name: str, message: str) -> None:
        url = "http://localhost:3001/webhook/msg"
        headers = {"Content-Type": "application/json"}
        data = {"to": to_g_name, "isRoom": True, "type": "text", "content": message}
        requests.post(url, headers=headers, json=data)

    # 通过文件URL发送文件
    """
    curl --location --request POST 'http://localhost:3001/webhook/msg' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "to": "testGroup",
        "type": "fileUrl",
        "content": "https://samplelib.com/lib/preview/mp3/sample-3s.mp3",
        "isRoom": true
    }'
    """

    @staticmethod
    def send_urlfile_msg(to: SendTo, file_path: str) -> None:
        if to.g_name != "":
            SenderV1.send_urlfile_msg_g(to.g_name, file_path)
        else:
            SenderV1.send_urlfile_msg_p(to.p_name, file_path)

    @staticmethod
    def send_urlfile_msg_p(to_p_name: str, file_url: str) -> None:
        url = "http://localhost:3001/webhook/msg"
        headers = {"Content-Type": "application/json"}
        data = {"to": to_p_name, "type": "fileUrl", "content": file_url}
        requests.post(url, headers=headers, json=data)

    @staticmethod
    def send_urlfile_msg_g(to_g_name: str, file_url: str) -> None:
        url = "http://localhost:3001/webhook/msg"
        headers = {"Content-Type": "application/json"}
        data = {"to": to_g_name, "isRoom": True, "type": "fileUrl", "content": file_url}
        requests.post(url, headers=headers, json=data)

    # 本地文件发送
    """
    curl --location --request POST 'http://localhost:3001/webhook/msg' \
    --form 'to=testGroup' \
    --form content=@"$HOME/demo.jpg" \
    --form 'isRoom=1'
    """

    @staticmethod
    def send_localfile_msg(to: SendTo, file_path: str) -> None:
        if to.g_name != "":
            SenderV1.send_localfile_msg_g(to.g_name, file_path)
        else:
            SenderV1.send_localfile_msg_p(to.p_name, file_path)

    @staticmethod
    def send_localfile_msg_p(to_p_name: str, file_path: str) -> None:
        url = "http://localhost:3001/webhook/msg"
        data = {"to": to_p_name, "isRoom": 0}
        files = {"content": open(file_path, "rb")}
        requests.post(url, data=data, files=files)

    @staticmethod
    def send_localfile_msg_g(to_g_name: str, file_path: str) -> None:
        url = "http://localhost:3001/webhook/msg"
        data = {"to": to_g_name, "isRoom": 1}
        files = {"content": open(file_path, "rb")}
        requests.post(url, data=data, files=files)
