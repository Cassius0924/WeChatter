from wechatter.webhook_handlers.hanlders import github_webhook_handler
from wechatter.models import GithubPrReviewWebhook
from wechatter.sender import Sender


@github_webhook_handler("pull_request_review")
def handle_pr_review(data: dict):
    payload = GithubPrReviewWebhook(**data)
    print(f"Pull Request Review {payload.review.state} by {payload.review.user.login}.")
    message = (
        "==== GitHub Pull Request Review 事件 ====\n"
        f"⬇️ 有 PR Review 被 {payload.review.state.capitalize()} ！\n"
        f"仓库：{payload.repository.full_name}\n"
        f"标题：{payload.pull_request.title}\n"
        f"创建者：{payload.pull_request.user.login}\n"
        f"查看详情：{payload.pull_request.html_url}"
    )
    Sender.send_msg_to_github_webhook_receivers(message)
