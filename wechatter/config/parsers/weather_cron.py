from typing import List

from apscheduler.triggers.cron import CronTrigger

from wechatter.commands._commands.weather import get_weather_str
from wechatter.models.scheduler import CronTask
from wechatter.sender import sender


def parse_weather_cron_rule_list(
    weather_cron_rule_list: List,
) -> List[CronTask]:
    """
    解析天气定时任务规则
    :param weather_cron_rule_list: 天气定时任务规则
    :return cron_tasks: 天气定时任务列表
    """
    cron_tasks = []
    for rule in weather_cron_rule_list:
        cron = rule["cron"]
        tasks = rule["tasks"]
        trigger = CronTrigger(
            year=cron["year"],
            month=cron["month"],
            day=cron["day"],
            week=cron["week"],
            day_of_week=cron["day_of_week"],
            hour=cron["hour"],
            minute=cron["minute"],
            second=cron["second"],
            start_date=cron["start_date"],
            end_date=cron["end_date"],
            timezone=cron["timezone"],
        )

        def func():
            for task in tasks:
                message = get_weather_str(task["city"])
                if task["to_persons"]:
                    sender.mass_send_msg(task["to_persons"], message)
                if task["to_groups"]:
                    sender.mass_send_msg(task["to_groups"], message, is_group=True)

        cron_tasks.append(
            CronTask(
                func=func,
                trigger=trigger,
            )
        )
    return cron_tasks
