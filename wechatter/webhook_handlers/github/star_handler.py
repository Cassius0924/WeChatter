from wechatter.webhook_handlers.hanlders import github_webhook_handler
from wechatter.models import GithubStarWebhook
from wechatter.sender import Sender


@github_webhook_handler("star")
def handle_star(data: dict):
    payload = GithubStarWebhook(**data)
    print(f"Star {payload.action} by {payload.sender.login}.")
    # Star +1 或 -1
    if payload.action == "created":
        message = (
            "==== GitHub Star 事件 ====\n"
            f"⭐️ {payload.repository.full_name} 的 Star 数量 +1 🆙！\n"
        )
        Sender.send_msg_to_github_webhook_receivers(message)
    else:
        message = (
            "==== GitHub Star 事件 ====\n"
            f"⭐️ {payload.repository.full_name} 的 Star 数量 -1 🔽！\n"
        )
        Sender.send_msg_to_github_webhook_receivers(message)
