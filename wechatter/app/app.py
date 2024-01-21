from fastapi import FastAPI
import wechatter.app.routers as routers

app = FastAPI()

app.include_router(routers.wechat_router)
# app.include_router(routers.github_router)
