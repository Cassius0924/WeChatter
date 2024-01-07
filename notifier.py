# 消息通知器
from admin import send_msg_to_all_admin
from send_msg import SendMessage, SendMessageType, SendTo, Sender


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
        send_msg_to_all_admin(msg)

    # FIXME: 登出消息发送不出去，因为发消息时候，机器人已经退出登录了
    @staticmethod
    def notify_logged_out() -> None:
        """通知已退出登录"""
        msg = "微信机器人已退出"
        send_msg_to_all_admin(msg)

    # TODO: 是否需要将下面的代码合并进来？
    # @staticmethod
    # def send_msg_to_all_admin(messsage: str) -> None:
    #     if len(admin_list) == 0:
    #         print("管理员列表为空")
    #         return
    #     for admin in admin_list:
    #         send_text_msg(messsage, admin)
