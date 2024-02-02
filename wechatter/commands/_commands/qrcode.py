import os

import qrcode as qrc
from loguru import logger

import wechatter.utils.path_manager as pm
from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
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
        datetime_str = get_current_datetime()
        path = pm.get_abs_path(f"data/qrcodes/{datetime_str}.png")
        img = generate_qrcode(message)
        save_qrcode(img, path)
    except Exception as e:
        error_message = f"生成二维码失败，错误信息：{str(e)}"
        logger.error(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))
    else:
        Sender.send_localfile_msg(to, path)


def generate_qrcode(data: str):
    """生成二维码，返回二维码图像"""
    qr = qrc.QRCode(
        version=1,
        error_correction=qrc.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def save_qrcode(img, path: str) -> None:
    """保存二维码到指定路径"""
    if not os.access(os.path.dirname(path), os.W_OK):
        logger.error(f"保存 {path} 失败，权限不足")
        raise PermissionError(f"保存 {path} 失败，权限不足")
    try:
        img.save(path)
    except AttributeError:
        logger.error(f"保存 {path} 失败，二维码图像为空")
        raise AttributeError(f"保存 {path} 失败，二维码图像为空")
    except Exception:
        logger.error(f"保存 {path} 失败")
        raise Exception(f"保存 {path} 失败")


# FIXME: 目前不可用！发送后，二维码后缀名不对，导致微信识别成普通文件
def get_qrcode_url(data: str) -> str:
    """获取二维码的url"""
    return f"https://api.qrserver.com/v1/create-qr-code/?data={data}"
