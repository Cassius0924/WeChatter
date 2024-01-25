from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from main import cr

from wechatter.webhook_handlers import github_webhook_handlers as handlers

router = APIRouter()


@router.post(cr.github_webhook_api_path)
async def recv_github_webhook(request: Request):
    """接收 GitHub Webhook"""
    data = await request.json()
    github_event = request.headers.get("X-GitHub-Event")

    handler = handlers.get(github_event)
    if handler is None:
        print(f"未支持的 GitHub event: {github_event}")
        return {"detail": "Unsupported GitHub event"}

    try:
        handler(data)
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(e)},
        )

    return {"detail": "Webhook received"}
