from admin import send_msg_to_all_admin
from send_msg import send_text_msg


# 消息通知器
class Notifier:
    def __init__(self):
        pass

    @staticmethod
    def notify_received(to_user_name: str) -> None:
        msg = "收到命令请求"
        send_text_msg(msg, to_user_name)

    # 机器人登录登出通知，若是登录（登出）则发送登录（登出）消息给所有管理员
    @staticmethod
    def notify_logged_in() -> None:
        msg = "微信机器人启动成功"
        send_msg_to_all_admin(msg)

    @staticmethod
    def notify_logged_out() -> None:
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
