from loguru import logger

from wechatter.models.github import GithubForkWebhook
from wechatter.sender import Sender
from wechatter.webhook_handlers.hanlders import github_webhook_handler


@github_webhook_handler("fork")
def handle_fork(data: dict):
    payload = GithubForkWebhook(**data)
    logger.info(
        f"A new fork by {payload.sender.login} to {payload.repository.full_name}"
    )
    message = (
        "==== GitHub Fork 事件 ====\n"
        f"🍴 {payload.repository.full_name} 有新的 Fork！🆙\n"
    )
    Sender.send_msg_to_github_webhook_receivers(message)
