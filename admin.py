# 管理员管理
from send_msg import send_text_msg
from config import admin_list


# 给所有管理发消息
def send_msg_to_all_admin(messsage: str) -> None:
    if len(admin_list) == 0:
        print("管理员列表为空")
        return
    for admin in admin_list:
        send_text_msg(messsage, admin)
