from wechatter.models import GithubIssueCommentWebhook
from wechatter.webhook_handlers.hanlders import github_webhook_handler
from wechatter.sender.sender import Sender


@github_webhook_handler("issue_comment")
def handle_issue_comment(data: dict):
    payload = GithubIssueCommentWebhook(**data)
    print(
        f"Comment {payload.comment.id} was {payload.action} by {payload.comment.user.login}."
    )
    content = ""
    if len(content) > 20:
        content = payload.comment.body[:20] + "..."
    else:
        content = payload.comment.body
    message = (
        "==== GitHub Comment 事件 ====\n"
        f"💬 有评论被 {payload.action.capitalize()} ！\n"
        f"仓库：{payload.repository.full_name}\n"
        f"创建者：{payload.issue.user.login}\n"
        f"标题：{payload.issue.title}\n"
        f"内容：{content}\n"
        f"查看详情：{payload.issue.html_url}"
    )
    Sender.send_msg_to_github_webhook_receivers(message)
