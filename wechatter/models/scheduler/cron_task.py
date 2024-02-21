from typing import Callable, List

from apscheduler.triggers.cron import CronTrigger
from pydantic import BaseModel, ConfigDict


class CronTask(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    enabled: bool
    desc: str
    cron_trigger: CronTrigger
    funcs: List[Callable]
