# 消息发送类
import requests

from message import MessageSource


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
    url = ""
    port = ""

    @staticmethod
    def send_text_msg(to: SendTo, message: str):
        # 群消息
        if to.g_name != "":
            message = f"@{to.p_name}\n{message}"
            Sender.send_text_msg_g(to.g_name, message)
        # 个人消息
        else:
            Sender.send_text_msg_p(to.p_name, message)

    # 发送消息：curl -X POST http://localhost:3001/webhook/msg
    # 发送给个人
    @staticmethod
    def send_text_msg_p(to_p_name: str, message: str):
        url = "http://localhost:3001/webhook/msg"
        headers = {"Content-Type": "application/json"}
        data = {"to": to_p_name, "type": "text", "content": message}
        requests.post(url, headers=headers, json=data)

    # 发送给群组
    @staticmethod
    def send_text_msg_g(to_g_name: str, message: str):
        url = "http://localhost:3001/webhook/msg"
        headers = {"Content-Type": "application/json"}
        data = {"to": to_g_name, "isRoom": True, "type": "text", "content": message}
        requests.post(url, headers=headers, json=data)

    @staticmethod
    def send_image_msg_p(image_path: str, to_user_name: str):
        pass

    @staticmethod
    def send_image_msg_g(image_path: str, to_user_name: str):
        pass

    @staticmethod
    def send_file_msg_p(file_path: str, to_user_name: str):
        pass

    @staticmethod
    def send_file_msg_g(file_path: str, to_user_name: str):
        pass

    @staticmethod
    def send_url_msg_p(url: str, to_user_name: str):
        pass

    @staticmethod
    def send_url_msg_g(url: str, to_user_name: str):
        pass
