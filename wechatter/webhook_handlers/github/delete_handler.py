from loguru import logger

from wechatter.models.github import GithubDeleteWebhook
from wechatter.sender import sender
from wechatter.webhook_handlers.hanlders import github_webhook_handler


@github_webhook_handler("delete")
def handle_delete(data: dict):
    payload = GithubDeleteWebhook(**data)
    if payload.ref_type == "branch":
        logger.info(f"Branch {payload.ref} was deleted by {payload.sender.login}")
        message = (
            "==== GitHub Delete 事件 ====\n"
            f"🚮 有分支被删除了！\n"
            f"📚 仓库：{payload.repository.full_name}\n"
            f"🚮 删除了 {payload.ref} 分支\n"
            f"🧑‍💻 创建者：{payload.sender.login}\n"
            f"🔗 查看详情：{payload.repository.html_url}"
        )
        sender.mass_send_msg_to_github_webhook_receivers(message)
    elif payload.ref_type == "tag":
        logger.info(f"Tag {payload.ref} was deleted by {payload.sender.login}")
        message = (
            "==== GitHub Delete 事件 ====\n"
            f"🚮 有标签被删除了！\n"
            f"📚 仓库：{payload.repository.full_name}\n"
            f"🚮 删除了 {payload.ref} 标签\n"
            f"🧑‍💻 创建者：{payload.sender.login}\n"
            f"🔗 查看详情：{payload.repository.html_url}"
        )
        sender.mass_send_msg_to_github_webhook_receivers(message)
