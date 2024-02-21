from loguru import logger

from wechatter.models.github import GithubStarWebhook
from wechatter.sender import sender
from wechatter.webhook_handlers.hanlders import github_webhook_handler


@github_webhook_handler("star")
def handle_star(data: dict):
    payload = GithubStarWebhook(**data)
    logger.info(f"Star {payload.action} by {payload.sender.login}.")
    if payload.action == "created":
        message = (
            "==== GitHub Star 事件 ====\n"
            f"⭐️ {payload.repository.full_name} 的 Star 数量 +1 🆙！\n"
        )
        sender.mass_send_msg_to_github_webhook_receivers(message)
    else:
        message = (
            "==== GitHub Star 事件 ====\n"
            f"⭐️ {payload.repository.full_name} 的 Star 数量 -1 🔽！\n"
        )
        sender.mass_send_msg_to_github_webhook_receivers(message)
