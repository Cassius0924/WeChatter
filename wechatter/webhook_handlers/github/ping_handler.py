from loguru import logger

from wechatter.models.github import GithubPingWebhook
from wechatter.sender import Sender
from wechatter.webhook_handlers.hanlders import github_webhook_handler


@github_webhook_handler("ping")
def handle_ping(data: dict):
    payload = GithubPingWebhook(**data)
    logger.info(f"Ping from {payload.repository.full_name}.")
    message = (
        "==== GitHub Ping 事件 ====\n"
        "❇️ 有 Ping 事件！\n"
        f"📝 ZEN：{payload.zen}\n"
        f"📚 仓库：{payload.repository.full_name}\n"
        f"🧑‍💻 触发者：{payload.sender.login}\n"
    )
    Sender.send_msg_to_github_webhook_receivers(message)
