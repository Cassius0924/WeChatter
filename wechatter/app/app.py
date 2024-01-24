from fastapi import FastAPI

import wechatter.app.routers as routers
from main import cr

app = FastAPI()

app.include_router(routers.wechat_router)

if cr.github_webhook_enabled:
    app.include_router(routers.github_router)
