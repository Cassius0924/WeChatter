from typing import List

from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger

from wechatter.models.scheduler import CronTask


class Scheduler:
    def __init__(self, cron_task_list: List[CronTask] = None):
        self.scheduler = BackgroundScheduler()
        self.cron_task_list = cron_task_list

    def startup(self):
        """
        启动定时任务
        """
        if not self.cron_task_list:
            logger.info("定时任务为空，不启动定时任务")
            return
        for cron_task in self.cron_task_list:
            if cron_task.enabled:
                for func, args in cron_task.funcs:
                    self.scheduler.add_job(func, cron_task.cron_trigger, args=args)
                logger.info(f"定时任务已添加: {cron_task.desc}")
        self.scheduler.start()
        logger.info("定时任务已启动")

    def shutdown(self):
        """
        停止定时任务
        """
        self.scheduler.shutdown()
        logger.info("定时任务已停止")
