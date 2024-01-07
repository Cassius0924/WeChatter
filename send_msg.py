# 消息发送类
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


# TODO: 将URL端口保存到配置文件中
class Sender:
    host = "http://localhost"
    url = f'{host}:{cr.send_port}/webhook/msg'

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
            Sender.send_text_msg_g(to.g_name, message)
        # 个人消息
        else:
            Sender.send_text_msg_p(to.p_name, message)

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
            Sender.send_urlfile_msg_g(to.g_name, file_path)
        else:
            Sender.send_urlfile_msg_p(to.p_name, file_path)

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
            Sender.send_localfile_msg_g(to.g_name, file_path)
        else:
            Sender.send_localfile_msg_p(to.p_name, file_path)

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
