from typing import List

from apscheduler.triggers.cron import CronTrigger

from wechatter.commands._commands.gasoline_price import get_gasoline_price_str
from wechatter.models.message import SendMessage, SendMessageType
from wechatter.models.scheduler import CronTask
from wechatter.sender import Sender


def parse_gasoline_price_cron_rule_list(
        gasoline_price_cron_rule_list: List,
) -> List[CronTask]:
    """
    解析汽油价格定时任务规则
    :param gasoline_price_cron_rule_list: 汽油价格定时任务规则
    :return cron_tasks: 汽油价格定时任务列表
    """
    cron_tasks = []
    for rule in gasoline_price_cron_rule_list:
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
                to_persons = task["to_persons"]
                to_groups = task["to_groups"]
                send_message = SendMessage(
                    type=SendMessageType.TEXT,
                    content=get_gasoline_price_str(task["city"])
                )
                Sender.send_msg_ps(to_p_names=to_persons, message=send_message)
                Sender.send_msg_gs(to_g_names=to_groups, message=send_message)

        cron_tasks.append(
            CronTask(
                func=func,
                trigger=trigger,
            )
        )
    return cron_tasks
