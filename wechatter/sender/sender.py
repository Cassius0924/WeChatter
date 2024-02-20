import json
from functools import singledispatch
from typing import List, Union

import requests
import tenacity
from loguru import logger

import wechatter.config as config
import wechatter.utils.http_request as http_request
from wechatter.models.wechat import QuotedResponse, SendTo
from wechatter.sender.quotable import make_quotable


# 对retry装饰器重新包装，增加日志输出
def _retry(
    stop=tenacity.stop_after_attempt(3),
    retry_error_log_level="ERROR",
):
    def retry_wrapper(func):
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

    return retry_wrapper


# TODO: 改成装饰器
def _logging(func):
    def logging_wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        r_json = response.json()
        # https://github.com/danni-cool/wechatbot-webhook?tab=readme-ov-file#%E8%BF%94%E5%9B%9E%E5%80%BC-response-%E7%BB%93%E6%9E%84
        if r_json["message"].startswith("Message"):
            pass
        elif r_json["message"].startswith("Some"):
            logger.error("发送消息失败，参数校验不通过")
        elif r_json["message"].startswith("All"):
            logger.error("发送消息失败，所有消息均发送失败")
            return
        elif r_json["message"].startswith("Part"):
            logger.warning("发送消息失败，部分消息发送成功")
            return

        if "task" not in r_json:
            return

        try:
            data = json.loads(response.request.body.decode("utf-8"))
        except UnicodeDecodeError:
            # 本地文件发送无法解码
            # logger.info("发送图片成功")
            return
        except json.JSONDecodeError as e:
            logger.error(f"发送消息失败，错误信息：{str(e)}")
            return

        if isinstance(data, list):
            for item in data:
                logger.info(
                    f"发送消息成功，发送给：{item['to']}，发送的内容：{item['data']}"
                )
        elif isinstance(data, dict):
            logger.info(
                f"发送消息成功，发送给：{data['to']}，发送的内容：{data['data']}"
            )

    return logging_wrapper


@_logging
@_retry()
def _post_request(
    url, data=None, json=None, files=None, headers={}, timeout=5
) -> requests.Response:
    return http_request.post_request(
        url, data=data, json=json, files=files, headers=headers, timeout=timeout
    )


def _log(response: requests.Response) -> bool:
    """
    检查发送状态
    """

    r_json = response.json()
    # https://github.com/danni-cool/wechatbot-webhook?tab=readme-ov-file#%E8%BF%94%E5%9B%9E%E5%80%BC-response-%E7%BB%93%E6%9E%84
    if r_json["message"].startswith("Message"):
        pass
    elif r_json["message"].startswith("Some"):
        logger.error("发送消息失败，参数校验不通过")
    elif r_json["message"].startswith("All"):
        logger.error("发送消息失败，所有消息均发送失败")
        return False
    elif r_json["message"].startswith("Part"):
        logger.warning("发送消息失败，部分消息发送成功")
        return False

    if "task" not in r_json:
        return False

    try:
        data = json.loads(response.request.body.decode("utf-8"))
    except UnicodeDecodeError:
        # 本地文件发送无法解码
        # logger.info("发送图片成功")
        return True
    except json.JSONDecodeError as e:
        logger.error(f"发送消息失败，错误信息：{str(e)}")
        return False

    if isinstance(data, list):
        for item in data:
            logger.info(
                f"发送消息成功，发送给：{item['to']}，发送的内容：{item['data']}"
            )
    elif isinstance(data, dict):
        logger.info(f"发送消息成功，发送给：{data['to']}，发送的内容：{data['data']}")
    return True


URL = f"{config.wx_webhook_base_api}/webhook/msg/v2"
V1_URL = f"{config.wx_webhook_base_api}/webhook/msg"


def _validate(fn):
    """
    验证接收者和消息内容是否为空
    """

    def wrapper(n, m, *args, **kwargs):
        if not n:
            logger.error("发送消息失败，接收者为空")
            return
        if not m:
            logger.error("发送消息失败，消息内容为空")
            return

        return fn(n, m, *args, **kwargs)

    return wrapper


@singledispatch
def send_msg(
    to: Union[str, SendTo],
    message: str,
    is_group: bool = False,
    type: str = "text",
    quoted_response: QuotedResponse = None,
):
    """
    发送消息

    当传入的第一个参数是字符串时，is_group 默认为 False。
    当传入的第一个参数是 SendTo 对象时，is_group 默认为 True。

    当 quoted_response 不为 None 时，该消息为可引用消息。表示该消息被
    引用回复后，会触发进一步的消息互动。

    :param to: 接收对象的名字或SendTo对象
    :param message: 消息内容
    :param is_group: 是否为群组（默认值根据 to 的类型而定）
    :param type: 消息类型，可选 text、fileUrl（默认值为 text）
    :param quoted_response: 被引用后的回复消息（默认值为 None）
    """
    pass


@send_msg.register(str)
@_validate
def _send_msg1(
    name: str,
    message: str,
    is_group: bool = False,
    type: str = "text",
    quoted_response: QuotedResponse = None,
):
    """
    发送消息
    :param name: 接收者
    :param message: 消息内容
    :param is_group: 是否为群组（默认为个人，False）
    :param type: 消息类型（text、fileUrl）
    :param quoted_response: 被引用后的回复消息（默认值为 None）
    """
    if quoted_response:
        message = make_quotable(message=message, quoted_response=quoted_response)
    data = {
        "to": name,
        "isRoom": is_group,
        "data": {"type": type, "content": message},
    }
    _post_request(URL, json=data)


@send_msg.register(SendTo)
def _send_msg2(
    to: SendTo,
    message: str,
    is_group: bool = True,
    type: str = "text",
    quoted_response: QuotedResponse = None,
):
    """
    发送消息
    :param to: SendTo 对象
    :param message: 消息内容
    :param is_group: 是否为群组（默认为群组，True）
    :param type: 消息类型（text、fileUrl）
    :param quoted_response: 被引用后的回复消息（默认值为 None）
    """
    if not is_group:
        return _send_msg1(
            to.p_name,
            message,
            is_group=False,
            type=type,
            quoted_response=quoted_response,
        )

    if to.group:
        return _send_msg1(
            to.g_name,
            message,
            is_group=True,
            type=type,
            quoted_response=quoted_response,
        )
    elif to.person:
        return _send_msg1(
            to.p_name,
            message,
            is_group=False,
            type=type,
            quoted_response=quoted_response,
        )
    else:
        logger.error("发送消息失败，接收者为空")


@singledispatch
def send_msg_list(
    to: Union[str, SendTo],
    message_list: List[str],
    is_group: bool = False,
    type: str = "text",
):
    """
    发送多条消息，消息类型相同
    :param to: 接收者
    :param message_list: 消息内容列表
    :param is_group: 是否为群组
    :param type: 消息类型（text、fileUrl）
    """
    pass


@send_msg_list.register(str)
@_validate
def _send_msg_list1(
    name: str,
    message_list: List[str],
    is_group: bool = False,
    type: str = "text",
):
    """
    发送多条消息，消息类型相同
    :param name: 接收者
    :param message_list: 消息内容列表
    :param is_group: 是否为群组
    :param type: 消息类型（text、fileUrl）
    """
    data = {"to": name, "isRoom": is_group, "data": []}
    for message in message_list:
        data["data"].append({"type": type, "content": message})
    _post_request(URL, json=data)


@send_msg_list.register(SendTo)
def _send_msg_list2(
    to: SendTo, message_list: List[str], is_group: bool = True, type: str = "text"
):
    """
    发送多条消息，消息类型相同
    :param to: SendTo 对象
    :param message_list: 消息内容列表
    :param is_group: 是否为群组
    :param type: 消息类型（text、fileUrl）
    """
    if not is_group:
        return _send_msg_list1(to.p_name, message_list, is_group=False, type=type)

    if to.group:
        return _send_msg_list1(to.g_name, message_list, is_group=True, type=type)
    elif to.person:
        return _send_msg_list1(to.p_name, message_list, is_group=False, type=type)
    else:
        logger.error("发送消息失败，接收者为空")


@_validate
def mass_send_msg(
    name_list: List[str],
    message: str,
    is_group: bool = False,
    type: str = "text",
    quoted_response: QuotedResponse = None,
):
    """
    群发消息，给多个人发送一条消息
    :param name_list: 接收者列表
    :param message: 消息内容
    :param is_group: 是否为群组
    :param type: 消息类型（text、fileUrl）
    :param quoted_response: 被引用后的回复消息（默认值为 None）
    """
    if quoted_response:
        message = make_quotable(message=message, quoted_response=quoted_response)
    data = []
    for name in name_list:
        data.append(
            {
                "to": name,
                "isRoom": is_group,
                "data": {"type": type, "content": message},
            }
        )
    _post_request(URL, json=data)


@singledispatch
def send_localfile_msg():
    """
    发送本地文件
    :param name: 接收者
    :param file_path: 文件路径
    :param is_group: 是否为群组
    """
    pass


@send_localfile_msg.register(str)
@_validate
def _send_localfile_msg1(name: str, file_path: str, is_group: bool = False):
    """
    发送本地文件
    :param name: 接收者
    :param file_path: 文件路径
    :param is_group: 是否为群组
    """
    data = {"to": name, "isRoom": int(is_group)}
    files = {"content": open(file_path, "rb")}
    _post_request(V1_URL, data=data, files=files)


@send_localfile_msg.register(SendTo)
def _send_localfile_msg2(to: SendTo, file_path: str, is_group: bool = True):
    """
    发送本地文件
    :param to: SendTo 对象
    :param file_path: 文件路径
    :param is_group: 是否为群组
    """
    if not is_group:
        return _send_localfile_msg1(to.p_name, file_path, is_group=False)

    if to.group:
        return _send_localfile_msg1(to.g_name, file_path, is_group=True)
    elif to.person:
        return _send_localfile_msg1(to.p_name, file_path, is_group=False)
    else:
        logger.error("发送消息失败，接收者为空")


def mass_send_msg_to_admins(
    message: str, type: str = "text", quoted_response: QuotedResponse = None
):
    """
    群发消息给所有管理员
    :param message: 消息内容
    :param type: 消息类型（text、fileUrl）
    :param quoted_response: 被引用后的回复消息（默认值为 None）
    """
    if quoted_response:
        message = make_quotable(message=message, quoted_response=quoted_response)
    if len(config.admin_list) == 0:
        logger.warning("管理员列表为空")
    else:
        mass_send_msg(config.admin_list, message, type=type)
    if len(config.admin_group_list) == 0:
        logger.warning("管理员群列表为空")
    else:
        mass_send_msg(config.admin_group_list, message, is_group=True, type=type)


def mass_send_msg_to_github_webhook_receivers(
    message: str, type: str = "text", quoted_response: QuotedResponse = None
):
    """
    群发消息给所有 GitHub Webhook 接收者
    :param message: 消息内容
    :param type: 消息类型（text、fileUrl）
    :param quoted_response: 被引用后的回复消息（默认值为 None）
    """
    if quoted_response:
        message = make_quotable(message=message, quoted_response=quoted_response)
    if len(config.github_webhook_receiver_list) == 0:
        logger.warning("GitHub Webhook 接收者列表为空")
    else:
        mass_send_msg(
            config.github_webhook_receiver_list,
            message,
            is_group=False,
            type=type,
        )
    if len(config.github_webhook_receive_group_list) == 0:
        logger.warning("GitHub Webhook 接收群列表为空")
    else:
        mass_send_msg(
            config.github_webhook_receive_group_list,
            message,
            is_group=True,
            type=type,
        )
