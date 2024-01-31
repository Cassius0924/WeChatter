# URL转二维码命令
import qrcode

import wechatter.utils.path_manager as pm
from wechatter.commands.handlers import command
from wechatter.models.message import SendTo
from wechatter.sender import Sender
from wechatter.utils.time import get_current_datetime


@command(
    command="qrcode",
    keys=["二维码", "qrcode"],
    desc="将文本或链接转换为二维码。",
    value=90,
)
def qrcode_command_handler(to: SendTo, message: str = "") -> None:
    # 获取二维码
    try:
        response = generate_qrcode(message)
        Sender.send_localfile_msg(to, response)
    except Exception as e:
        error_message = f"生成二维码失败，错误信息：{e}"
        print(error_message)
        Sender.send_text_msg(to, error_message)


def generate_qrcode(data: str) -> str:
    """生成二维码，返回二维码的保存路径"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # 保存到 data/qrcodes/ 目录下
    datetime_str = get_current_datetime()
    path = pm.get_abs_path(f"data/qrcodes/{datetime_str}.png")
    try:
        img.save(path)
    except Exception as e:
        raise f"保存二维码失败：{e}"
    return path


# FIXME: 目前不可用！发送后，二维码后缀名不对，导致微信识别成普通文件
def get_qrcode_url(data: str) -> str:
    """获取二维码的url"""
    return f"https://api.qrserver.com/v1/create-qr-code/?data={data}"
