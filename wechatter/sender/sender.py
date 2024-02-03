import json
from typing import List

import requests
import tenacity
from loguru import logger

import wechatter.config as config
import wechatter.utils.http_request as http_request
from wechatter.models.message import (
    SendMessage,
    SendMessageList,
    SendMessageType,
    SendTo,
)


# 对retry装饰器重新包装，增加日志输出
def _retry(
    stop=tenacity.stop_after_attempt(3),
    retry_error_log_level="ERROR",
):
    def wrapper(func):
        @tenacity.retry(stop=stop)
        def wrapped_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.log(
                    retry_error_log_level,
                    f"重试 {func.__name__} 失败，错误信息：{str(e)}",
                )
                raise

        return wrapped_func

    return wrapper


@_retry()
def _post_request(
    url, data=None, json=None, files=None, headers={}, timeout=5
) -> requests.Response:
    return http_request.post_request(
        url, data=data, json=json, files=files, headers=headers, timeout=timeout
    )


def _log(response: requests.Response) -> bool:
    """检查发送状态"""
    # if response.status_code != 200:
    #     logger.error(f"发送消息失败，状态码：{response.status_code}")
    #     return False
    r_json = response.json()
    # 即使code为200，也需要检查success字段
    task = r_json.get("task", None)
    if task is not None:
        if not r_json["success"] or not task["successCount"] == task["totalCount"]:
            logger.error(f"发送消息失败，错误信息：{r_json['message']}")
            return False
        # 部分成功
        if task["successCount"] > 0 and task["successCount"] < task["totalCount"]:
            logger.warning(f"发送消息部分成功，成功数：{task['successCount']}")
            return True

    try:
        data = json.loads(response.request.body.decode("utf-8"))
    except UnicodeDecodeError:
        # 本地文件发送无法解码
        logger.info("发送图片成功")
        return True
    except json.JSONDecodeError:
        logger.error(f"发送消息失败，错误信息：{r_json['message']}")
        return False

    if isinstance(data, list):
        for item in data:
            logger.info(
                f"发送消息成功，发送给：{item['to']}，发送的内容：{item['data']}"
            )
    elif isinstance(data, dict):
        logger.info(f"发送消息成功，发送给：{data['to']}，发送的内容：{data['data']}")
    return True


class Sender:
    """v2 版本 api 消息发送类"""

    url = f"{config.wx_webhook_host}:{config.wx_webhook_port}/webhook/msg/v2"
    v1_url = f"{config.wx_webhook_host}:{config.wx_webhook_port}/webhook/msg"

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
        _log(_post_request(Sender.url, headers=headers, json=data))

    @staticmethod
    def send_msg_g(to_g_name: str, message: SendMessage) -> bool:
        """发送给群组"""
        headers = {"Content-Type": "application/json"}
        data = {
            "to": to_g_name,
            "isRoom": True,
            "data": {"type": message.type, "content": message.content},
        }
        _log(_post_request(Sender.url, headers=headers, json=data))

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
        _log(_post_request(Sender.url, headers=headers, json=data))

    # 给同一个群组发送多条消息
    @staticmethod
    def send_msgs_g(to_g_name: str, messages: SendMessageList) -> bool:
        headers = {"Content-Type": "application/json"}
        data = {"to": to_g_name, "isRoom": True, "data": []}
        for message in messages.messages:
            msg = {"type": message.type, "content": message.content}
            data["data"].append(msg)
        _log(_post_request(Sender.url, headers=headers, json=data))

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
        if to_p_names == []:
            return False
        headers = {"Content-Type": "application/json"}
        data = []
        for to_p_name in to_p_names:
            msg = {
                "to": to_p_name,
                "isRoom": False,
                "data": {"type": message.type, "content": message.content},
            }
            data.append(msg)
        _log(_post_request(Sender.url, headers=headers, json=data))

    @staticmethod
    def send_msg_gs(to_g_names: List[str], message: SendMessage) -> bool:
        """给多个群组发送一条消息"""
        if to_g_names == []:
            return False
        headers = {"Content-Type": "application/json"}
        data = []
        for to_g_name in to_g_names:
            msg = {
                "to": to_g_name,
                "isRoom": True,
                "data": {"type": message.type, "content": message.content},
            }
            data.append(msg)
        _log(_post_request(Sender.url, headers=headers, json=data))

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
        data = {"to": to_p_name, "isRoom": 0}
        files = {"content": open(file_path, "rb")}
        _log(_post_request(Sender.v1_url, data=data, files=files))

    @staticmethod
    def send_localfile_msg_g(to_g_name: str, file_path: str) -> bool:
        """发送本地文件给群组"""
        data = {"to": to_g_name, "isRoom": 1}
        files = {"content": open(file_path, "rb")}
        _log(_post_request(Sender.v1_url, data=data, files=files))

    @staticmethod
    def send_msg_to_admins(message: str) -> None:
        """发送消息给所有管理员"""
        if len(config.admin_list) == 0:
            logger.warning("管理员列表为空")
        else:
            Sender.send_msg_ps(
                config.admin_list, SendMessage(SendMessageType.TEXT, message)
            )
        if len(config.admin_group_list) == 0:
            logger.warning("管理员群列表为空")
        else:
            Sender.send_msg_gs(
                config.admin_group_list, SendMessage(SendMessageType.TEXT, message)
            )

    @staticmethod
    def send_msg_to_github_webhook_receivers(message: str) -> None:
        """发送消息给所有 GitHub Webhook 接收者"""
        if len(config.github_webhook_receiver_list) == 0:
            logger.warning("GitHub Webhook 接收者列表为空")
        else:
            Sender.send_msg_ps(
                config.github_webhook_receiver_list,
                SendMessage(SendMessageType.TEXT, message),
            )
        if len(config.github_webhook_receive_group_list) == 0:
            logger.warning("GitHub Webhook 接收群列表为空")
        else:
            Sender.send_msg_gs(
                config.github_webhook_receive_group_list,
                SendMessage(SendMessageType.TEXT, message),
            )


# class SenderV1:
#     """v1 版本 api 消息发送类"""

#     # url = f"{config.wx_webhook_host}:{config.wx_webhook_port}/webhook/msg"

#     # 发送文本消息
#     """
#     curl --location --request POST 'http://localhost:3001/webhook/msg' \
#     --header 'Content-Type: application/json' \
#     --data-raw '{
#         "to": "testUser",
#         "type": "text",
#         "content": "Hello World!"
#     }'
#     """

#     @staticmethod
#     def send_text_msg(to: SendTo, message: str) -> None:
#         """发送文本消息"""
#         # 群消息
#         if to.g_name != "":
#             message = f"@{to.p_name}\n{message}"
#             SenderV1.send_text_msg_g(to.g_name, message)
#         # 个人消息
#         else:
#             SenderV1.send_text_msg_p(to.p_name, message)

#     @staticmethod
#     def send_text_msg_p(to_p_name: str, message: str) -> None:
#         """发送文本消息给个人"""
#         url = "http://localhost:3001/webhook/msg"
#         headers = {"Content-Type": "application/json"}
#         data = {"to": to_p_name, "type": "text", "content": message}
#         _post_request(url, headers=headers, json=data)

#     @staticmethod
#     def send_text_msg_g(to_g_name: str, message: str) -> None:
#         """发送文本消息给群组"""
#         url = "http://localhost:3001/webhook/msg"
#         headers = {"Content-Type": "application/json"}
#         data = {"to": to_g_name, "isRoom": True, "type": "text", "content": message}
#         _post_request(url, headers=headers, json=data)

#     # 通过文件URL发送文件
#     """
#     curl --location --request POST 'http://localhost:3001/webhook/msg' \
#     --header 'Content-Type: application/json' \
#     --data-raw '{
#         "to": "testGroup",
#         "type": "fileUrl",
#         "content": "https://samplelib.com/lib/preview/mp3/sample-3s.mp3",
#         "isRoom": true
#     }'
#     """

#     @staticmethod
#     def send_urlfile_msg(to: SendTo, file_path: str) -> None:
#         """通过文件URL发送文件"""
#         if to.g_name != "":
#             SenderV1.send_urlfile_msg_g(to.g_name, file_path)
#         else:
#             SenderV1.send_urlfile_msg_p(to.p_name, file_path)

#     @staticmethod
#     def send_urlfile_msg_p(to_p_name: str, file_url: str) -> None:
#         """通过文件URL发送文件给个人"""
#         url = "http://localhost:3001/webhook/msg"
#         headers = {"Content-Type": "application/json"}
#         data = {"to": to_p_name, "type": "fileUrl", "content": file_url}
#         _post_request(url, headers=headers, json=data)

#     @staticmethod
#     def send_urlfile_msg_g(to_g_name: str, file_url: str) -> None:
#         """通过文件URL发送文件给群组"""
#         url = "http://localhost:3001/webhook/msg"
#         headers = {"Content-Type": "application/json"}
#         data = {"to": to_g_name, "isRoom": True, "type": "fileUrl", "content": file_url}
#         _post_request(url, headers=headers, json=data)

#     # 本地文件发送
#     """
#     curl --location --request POST 'http://localhost:3001/webhook/msg' \
#     --form 'to=testGroup' \
#     --form content=@"$HOME/demo.jpg" \
#     --form 'isRoom=1'
#     """

#     @staticmethod
#     def send_localfile_msg(to: SendTo, file_path: str) -> None:
#         """发送本地文件"""
#         if to.g_name != "":
#             SenderV1.send_localfile_msg_g(to.g_name, file_path)
#         else:
#             SenderV1.send_localfile_msg_p(to.p_name, file_path)

#     @staticmethod
#     def send_localfile_msg_p(to_p_name: str, file_path: str) -> None:
#         """发送本地文件给个人"""
#         url = "http://localhost:3001/webhook/msg"
#         data = {"to": to_p_name, "isRoom": 0}
#         files = {"content": open(file_path, "rb")}
#         _post_request(url, data=data, files=files)

#     @staticmethod
#     def send_localfile_msg_g(to_g_name: str, file_path: str) -> None:
#         """发送本地文件给群组"""
#         url = "http://localhost:3001/webhook/msg"
#         data = {"to": to_g_name, "isRoom": 1}
#         files = {"content": open(file_path, "rb")}
#         _post_request(url, data=data, files=files)
