github_webhook_handlers = {}
"""
'储存所有的 GitHub 事件 Handler
"""


def github_webhook_handler(event: str):
    """
    注册 GitHub 事件 Handler 的装饰器
    """

    def decorator(func):
        github_webhook_handlers[event] = func
        return func

    return decorator
