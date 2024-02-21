# 消息通知器
from typing import TYPE_CHECKING

from wechatter.sender import sender

if TYPE_CHECKING:
    from wechatter.models.wechat import SendTo


def notify_received(to: "SendTo") -> None:
    """
    通知收到命令请求
    """
    msg = "收到命令请求"
    sender.send_msg(to, msg)


# 机器人登录登出通知，若是登录（登出）则发送登录（登出）消息给所有管理员
def notify_logged_in() -> None:
    """
    通知登录成功
    """
    msg = "微信机器人启动成功"
    sender.mass_send_msg_to_admins(msg)


# FIXME: 登出消息发送不出去，因为发消息时候，机器人已经退出登录了
def notify_logged_out() -> None:
    """
    通知已退出登录
    """
    msg = "微信机器人已退出"
    sender.mass_send_msg_to_admins(msg)
