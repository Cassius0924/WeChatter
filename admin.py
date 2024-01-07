# 管理员管理
from send_msg import SendMessage, SendMessageType, Sender
from main import cr


# 给所有管理发消息
# TODO: 合并到Sender类中
def send_msg_to_all_admin(message: str) -> None:
    if len(cr.admin_list) == 0:
        print("管理员列表为空")
        return
    Sender.send_msg_ps(cr.admin_list, SendMessage(SendMessageType.TEXT, message))
    if len(cr.admin_group_list) == 0:
        print("管理员群列表为空")
        return
    Sender.send_msg_gs(cr.admin_group_list, SendMessage(SendMessageType.TEXT, message))

