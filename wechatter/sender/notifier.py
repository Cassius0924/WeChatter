# 消息通知器
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender


def notify_received(to: SendTo) -> None:
    """通知收到命令请求"""
    msg = "收到命令请求"
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, msg))


def notify_logged_in() -> None:
    """通知登录成功"""
    msg = "微信机器人启动成功"
    Sender.send_msg_to_admins(msg)


def notify_logged_out() -> None:
    """通知已退出登录"""
    msg = "微信机器人已退出"
    Sender.send_msg_to_admins(msg)
