from .hanlders import github_webhook_handlers

# 确保这些handler被导入，以便它们可以注册自己
from .github import (  # noqa: E402
    handle_ping,  # noqa: F401
    handle_issue,  # noqa: F401
    handle_issue_comment,  # noqa: F401
    handle_push,  # noqa: F401
    handle_pr,  # noqa: F401
    handle_pr_review,  # noqa: F401
    handle_star,  # noqa: F401
)
