from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from loguru import logger

import wechatter.config as config
from wechatter.webhook_handlers import github_webhook_handlers as handlers

router = APIRouter()


@router.post(config.github_webhook_api_path)
async def recv_github_webhook(request: Request):
    """接收 GitHub Webhook"""
    data = await request.json()
    github_event = request.headers.get("X-GitHub-Event")

    handler = handlers.get(github_event)
    if handler is None:
        logger.warning(f"未支持的 GitHub event: {github_event}")
        return {"detail": "Unsupported GitHub event"}

    try:
        handler(data)
    except ValueError as e:
        logger.error(f"GitHub Webhook 处理失败: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": str(e)}
        )

    return {"detail": "Webhook received"}
