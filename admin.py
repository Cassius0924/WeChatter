# 管理员管理
from send_msg import Sender
from main import cr


# 给所有管理发消息
# TODO: 合并到Sender类中
def send_msg_to_all_admin(message: str) -> None:
    if len(cr.admin_list) == 0:
        print("管理员列表为空")
        return
    for admin in cr.admin_list:
        Sender.send_text_msg_p(admin, message)
