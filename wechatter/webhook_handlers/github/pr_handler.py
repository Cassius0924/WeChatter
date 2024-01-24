from wechatter.webhook_handlers.hanlders import github_webhook_handler
from wechatter.models import GithubPrWebhook
from wechatter.sender import Sender


@github_webhook_handler("pull_request")
def handle_pr(data: dict):
    payload = GithubPrWebhook(**data)
    print(
        f"Pull Request {payload.pull_request.number} was {payload.action} by {payload.pull_request.user.login}."
    )
    message = (
        "==== GitHub Pull Request 事件 ====\n"
        f"⬇️ 有 PR 被 {payload.action.capitalize()} ！\n"
        f"仓库：{payload.repository.full_name}\n"
        f"标题：{payload.pull_request.title}\n"
        f"创建者：{payload.pull_request.user.login}\n"
        f"查看详情：{payload.pull_request.html_url}"
    )
    Sender.send_msg_to_github_webhook_receivers(message)
