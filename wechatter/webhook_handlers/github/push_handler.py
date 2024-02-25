from loguru import logger

from wechatter.models.github import GithubPushWebhook
from wechatter.sender import sender
from wechatter.webhook_handlers.hanlders import github_webhook_handler


@github_webhook_handler("push")
def handle_push(data: dict):
    payload = GithubPushWebhook(**data)
    logger.info(
        f"Push event on {payload.ref} in repository {payload.repository.full_name}."
    )
    branch_url = payload.repository.html_url + "/tree/" + payload.ref.split("/")[-1]
    # 用 h5 的 a 标签，用于在微信中打开（经测试微信会吞掉 href 里的链接），下面方法失效
    # branch_url = '<a href=" https://github.com/Cassius0924 ">查看详情</a>'
    message = (
        "== GitHub Push 事件 ==\n"
        "🚀 新的代码已经推送到了仓库！\n"
        f"📚 仓库：{payload.repository.full_name}\n"
        f"🌱 分支：{payload.ref}\n"
        f"🧑‍💻 提交者：{payload.pusher.name}\n"
    )
    if len(payload.commits) != 0:
        # 最后一个commit的message
        message += f"📃 提交信息：{payload.commits.pop().message}\n"
    message += f"🔗 查看详情：{branch_url}"

    sender.mass_send_msg_to_github_webhook_receivers(message)
