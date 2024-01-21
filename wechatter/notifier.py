# 消息通知器
from wechatter.sender.send_message import SendMessage, SendMessageType, SendTo
from wechatter.sender.sender import Sender


class Notifier:
    """消息通知器，用于发送非命令产生的消息"""

    def __init__(self):
        pass

    # TODO: 改成只在为API请求的命令时才调用
    @staticmethod
    def notify_received(to: SendTo) -> None:
        """通知收到命令请求"""
        msg = "收到命令请求"
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, msg))

    # 机器人登录登出通知，若是登录（登出）则发送登录（登出）消息给所有管理员
    @staticmethod
    def notify_logged_in() -> None:
        """通知登录成功"""
        msg = "微信机器人启动成功"
        Sender.send_msg_to_all_admin(msg)

    # FIXME: 登出消息发送不出去，因为发消息时候，机器人已经退出登录了
    @staticmethod
    def notify_logged_out() -> None:
        """通知已退出登录"""
        msg = "微信机器人已退出"
        Sender.send_msg_to_all_admin(msg)
