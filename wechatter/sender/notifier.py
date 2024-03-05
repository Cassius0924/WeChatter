# 消息通知器
from typing import TYPE_CHECKING

from loguru import logger

from wechatter.config import config
from wechatter.sender import sender
from wechatter.utils import get_request, join_urls

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
    logger.info(msg)
    sender.mass_send_msg_to_admins(msg)
    if config.get("bark_url"):
        url = join_urls(
            config["bark_url"],
            f"WeChatter/🟢 微信机器人（{config['bot_name']}）登录成功",
        )
        get_request(url)


def notify_logged_out() -> None:
    """
    通知已退出登录
    """
    msg = "微信机器人已退出"
    logger.info(msg)
    # bark 提醒
    if config.get("bark_url"):
        url = join_urls(
            config["bark_url"],
            f"WeChatter/🔴 微信机器人（{config['bot_name']}）已退出登录?copy={config['wx_webhook_base_api']}/login?token={config['wx_webhook_token']}",
        )
        get_request(url)
