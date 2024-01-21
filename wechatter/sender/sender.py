from collections.abc import Callable
from typing import List

import requests

from main import cr
from wechatter.sender.send_message import (
    SendMessage,
    SendMessageList,
    SendMessageType,
    SendTo,
)


def _check(response: requests.Response) -> bool:
    """检查发送状态"""
    if response.status_code != 200:
        print(f"发送消息失败，状态码：{response.status_code}")
        return False
    result = response.json()
    # 即使code为200，也需要检查success字段
    task = result.get("task", None)
    if task is not None:
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


def _retry(times: int, func: Callable) -> bool:
    """重试函数"""
    for _ in range(times):
        if func():
            return True
    return False


class Sender:
    """v2 版本 api 消息发送类"""

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
        """发送消息（文本或链接文件）"""
        # 群消息
        if to.g_name != "":
            if message.type == SendMessageType.TEXT.value:
                message.content = f"@{to.p_name}\n{message.content}"
            return Sender.send_msg_g(to.g_name, message)
        # 个人消息
        else:
            return Sender.send_msg_p(to.p_name, message)

    @staticmethod
    def send_msg_p(to_p_name: str, message: SendMessage) -> bool:
        """发送给个人"""
        headers = {"Content-Type": "application/json"}
        data = {
            "to": to_p_name,
            "isRoom": False,
            "data": {"type": message.type, "content": message.content},
        }
        # 判断是否发送成功，如果失败则重试，最多重试 3 次
        return _retry(
            3, lambda: _check(requests.post(Sender.url, headers=headers, json=data))
        )

    @staticmethod
    def send_msg_g(to_g_name: str, message: SendMessage) -> bool:
        """发送给群组"""
        headers = {"Content-Type": "application/json"}
        data = {
            "to": to_g_name,
            "isRoom": True,
            "data": {"type": message.type, "content": message.content},
        }
        # 判断是否发送成功，如果失败则重试，最多重试 3 次
        return _retry(
            3, lambda: _check(requests.post(Sender.url, headers=headers, json=data))
        )

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
        return _retry(
            3, lambda: _check(requests.post(Sender.url, headers=headers, json=data))
        )

    # 给同一个群组发送多条消息
    @staticmethod
    def send_msgs_g(to_g_name: str, messages: SendMessageList) -> bool:
        headers = {"Content-Type": "application/json"}
        data = {"to": to_g_name, "isRoom": True, "data": []}
        for message in messages.messages:
            msg = {"type": message.type, "content": message.content}
            data["data"].append(msg)
        return _retry(
            3, lambda: _check(requests.post(Sender.url, headers=headers, json=data))
        )

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

    @staticmethod
    def send_msg_ps(to_p_names: List[str], message: SendMessage) -> bool:
        """给多个人发送一条消息"""
        headers = {"Content-Type": "application/json"}
        data = []
        for to_p_name in to_p_names:
            msg = {
                "to": to_p_name,
                "isRoom": False,
                "data": {"type": message.type, "content": message.content},
            }
            data.append(msg)
        return _retry(
            3, lambda: _check(requests.post(Sender.url, headers=headers, json=data))
        )

    @staticmethod
    def send_msg_gs(to_g_names: List[str], message: SendMessage) -> bool:
        """给多个群组发送一条消息"""
        headers = {"Content-Type": "application/json"}
        data = []
        for to_g_name in to_g_names:
            msg = {
                "to": to_g_name,
                "isRoom": True,
                "data": {"type": message.type, "content": message.content},
            }
            data.append(msg)
        return _retry(
            3, lambda: _check(requests.post(Sender.url, headers=headers, json=data))
        )

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
        """发送本地文件"""
        if to.g_name != "":
            return Sender.send_localfile_msg_g(to.g_name, file_path)
        else:
            return Sender.send_localfile_msg_p(to.p_name, file_path)

    @staticmethod
    def send_localfile_msg_p(to_p_name: str, file_path: str) -> bool:
        """发送本地文件给个人"""
        url = "http://localhost:3001/webhook/msg"
        data = {"to": to_p_name, "isRoom": 0}
        files = {"content": open(file_path, "rb")}
        return _retry(3, lambda: _check(requests.post(url, data=data, files=files)))

    @staticmethod
    def send_localfile_msg_g(to_g_name: str, file_path: str) -> bool:
        """发送本地文件给群组"""
        url = "http://localhost:3001/webhook/msg"
        data = {"to": to_g_name, "isRoom": 1}
        files = {"content": open(file_path, "rb")}
        return _retry(3, lambda: _check(requests.post(url, data=data, files=files)))

    @staticmethod
    def send_msg_to_all_admin(message: str) -> None:
        """发送消息给所有管理员"""
        if len(cr.admin_list) == 0:
            print("管理员列表为空")
            return
        Sender.send_msg_ps(cr.admin_list, SendMessage(SendMessageType.TEXT, message))
        if len(cr.admin_group_list) == 0:
            print("管理员群列表为空")
            return
        Sender.send_msg_gs(
            cr.admin_group_list, SendMessage(SendMessageType.TEXT, message)
        )


class SenderV1:
    """v1 版本 api 消息发送类"""

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
        """发送文本消息"""
        # 群消息
        if to.g_name != "":
            message = f"@{to.p_name}\n{message}"
            SenderV1.send_text_msg_g(to.g_name, message)
        # 个人消息
        else:
            SenderV1.send_text_msg_p(to.p_name, message)

    @staticmethod
    def send_text_msg_p(to_p_name: str, message: str) -> None:
        """发送文本消息给个人"""
        url = "http://localhost:3001/webhook/msg"
        headers = {"Content-Type": "application/json"}
        data = {"to": to_p_name, "type": "text", "content": message}
        requests.post(url, headers=headers, json=data)

    @staticmethod
    def send_text_msg_g(to_g_name: str, message: str) -> None:
        """发送文本消息给群组"""
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
        """通过文件URL发送文件"""
        if to.g_name != "":
            SenderV1.send_urlfile_msg_g(to.g_name, file_path)
        else:
            SenderV1.send_urlfile_msg_p(to.p_name, file_path)

    @staticmethod
    def send_urlfile_msg_p(to_p_name: str, file_url: str) -> None:
        """通过文件URL发送文件给个人"""
        url = "http://localhost:3001/webhook/msg"
        headers = {"Content-Type": "application/json"}
        data = {"to": to_p_name, "type": "fileUrl", "content": file_url}
        requests.post(url, headers=headers, json=data)

    @staticmethod
    def send_urlfile_msg_g(to_g_name: str, file_url: str) -> None:
        """通过文件URL发送文件给群组"""
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
        """发送本地文件"""
        if to.g_name != "":
            SenderV1.send_localfile_msg_g(to.g_name, file_path)
        else:
            SenderV1.send_localfile_msg_p(to.p_name, file_path)

    @staticmethod
    def send_localfile_msg_p(to_p_name: str, file_path: str) -> None:
        """发送本地文件给个人"""
        url = "http://localhost:3001/webhook/msg"
        data = {"to": to_p_name, "isRoom": 0}
        files = {"content": open(file_path, "rb")}
        requests.post(url, data=data, files=files)

    @staticmethod
    def send_localfile_msg_g(to_g_name: str, file_path: str) -> None:
        """发送本地文件给群组"""
        url = "http://localhost:3001/webhook/msg"
        data = {"to": to_g_name, "isRoom": 1}
        files = {"content": open(file_path, "rb")}
        requests.post(url, data=data, files=files)
