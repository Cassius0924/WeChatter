from loguru import logger

from wechatter.models.github import GithubReleaseWebhook
from wechatter.sender import sender
from wechatter.webhook_handlers.hanlders import github_webhook_handler


@github_webhook_handler("release")
def handle_release(data: dict):
    payload = GithubReleaseWebhook(**data)
    if payload.action != "published":
        return
    logger.info(
        f"Release event on {payload.release.html_url} in repository {payload.repository.full_name}."
    )
    message = (
        "== GitHub Release 事件 ==\n"
        f"🚀 新的版本发布了！\n"
        f"📚 仓库：{payload.repository.full_name}\n"
        f"🏷️ 版本：{payload.release.tag_name}\n"
        f"🧑‍💻 提交者：{payload.sender.login}\n"
        f"🔗 查看详情：{payload.release.html_url}"
    )

    sender.mass_send_msg_to_github_webhook_receivers(message)
