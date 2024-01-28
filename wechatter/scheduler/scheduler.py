from typing import List

from apscheduler.schedulers.background import BackgroundScheduler
from wechatter.models.scheduler import CronTask

CRON_TASKS: List[CronTask] = []


class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    @staticmethod
    def add_cron_task(cron_task: CronTask):
        """添加定时任务"""
        CRON_TASKS.append(cron_task)

    @staticmethod
    def add_cron_tasks(cron_tasks: List[CronTask]):
        """添加定时任务"""
        CRON_TASKS.extend(cron_tasks)

    def startup(self):
        """启动定时任务"""
        for ct in CRON_TASKS:
            self.scheduler.add_job(ct.func, ct.trigger)
        self.scheduler.start()
        print("定时任务已启动")

    def shutdown(self):
        """停止定时任务"""
        self.scheduler.shutdown()
        print("定时任务已停止")
