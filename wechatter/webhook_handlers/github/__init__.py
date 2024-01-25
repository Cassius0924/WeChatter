# 确保这些handler被导入，以便它们可以注册自己
from .ping_handler import handle_ping  # noqa: F401
from .issue_handler import handle_issue  # noqa: F401
from .issue_comment_handler import handle_issue_comment  # noqa: F401
from .push_handler import handle_push  # noqa: F401
from .pr_handler import handle_pr  # noqa: F401
from .pr_review_handler import handle_pr_review  # noqa: F401
from .star_handler import handle_star  # noqa: F401
