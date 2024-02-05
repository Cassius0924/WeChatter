from fastapi import FastAPI

import wechatter.app.routers as routers
import wechatter.config as config
from wechatter.config.parsers import (
    parse_gasoline_price_cron_rule_list,
    parse_weather_cron_rule_list,
)
from wechatter.scheduler import Scheduler

app = FastAPI()

app.include_router(routers.wechat_router)

if config.github_webhook_enabled:
    app.include_router(routers.github_router)

# 定时任务
if config.weather_cron_enabled:
    cron_tasks = parse_weather_cron_rule_list(config.weather_cron_rule_list)
    Scheduler.add_cron_tasks(cron_tasks)

if config.gasoline_price_cron_enable:
    cron_tasks = parse_gasoline_price_cron_rule_list(
        config.gasoline_price_cron_rule_list
    )
    Scheduler.add_cron_tasks(cron_tasks)

if not Scheduler.is_cron_tasks_empty():
    scheduler = Scheduler()

    # 定时任务
    @app.on_event("startup")
    async def startup_event():
        scheduler.startup()

    @app.on_event("shutdown")
    async def shutdown_event():
        scheduler.shutdown()
