from typing import Callable

from apscheduler.triggers.cron import CronTrigger


class CronTask:
    def __init__(self, func: Callable, trigger: CronTrigger):
        self.func = func
        self.trigger = trigger
