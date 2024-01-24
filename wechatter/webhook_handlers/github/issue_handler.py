from wechatter.models import GithubIssueWebhook
from wechatter.webhook_handlers.hanlders import github_webhook_handler
from wechatter.sender.sender import Sender


@github_webhook_handler("issues")
def handle_issue(data: dict):
    payload = GithubIssueWebhook(**data)
    print(
        f"Issue {payload.issue.number} was {payload.action} by {payload.issue.user.login}."
    )
    message = (
        "==== GitHub Issue 事件 ====\n"
        f"📢 有问题被 {payload.action.capitalize()} ！\n"
        f"仓库：{payload.repository.full_name}\n"
        f"标题：{payload.issue.title}\n"
        f"创建者：{payload.issue.user.login}\n"
        f"查看详情：{payload.issue.html_url}"
    )
    Sender.send_msg_to_github_webhook_receivers(message)
