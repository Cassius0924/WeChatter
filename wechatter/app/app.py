import wechatter.app.routers as routers
import wechatter.config as config
from fastapi import FastAPI

app = FastAPI()

app.include_router(routers.wechat_router)

if config.github_webhook_enabled:
    app.include_router(routers.github_router)
