from fastapi import FastAPI

import wechatter.app.routers as routers
import wechatter.config as config
from wechatter.scheduler import Scheduler
from wechatter.config.parsers import parse_weather_cron_rules

app = FastAPI()

app.include_router(routers.wechat_router)

if config.github_webhook_enabled:
    app.include_router(routers.github_router)


if config.weather_cron_enabled:
    cron_tasks = parse_weather_cron_rules(config.weather_cron_rules)

    Scheduler.add_cron_tasks(cron_tasks)

    scheduler = Scheduler()

    # 定时任务
    @app.on_event("startup")
    async def startup_event():
        scheduler.startup()

    @app.on_event("shutdown")
    async def shutdown_event():
        scheduler.shutdown()
