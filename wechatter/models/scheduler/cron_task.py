from apscheduler.triggers.cron import CronTrigger
from typing import Callable


class CronTask:
    def __init__(self, func: Callable, trigger: CronTrigger):
        self.func = func
        self.trigger = trigger
