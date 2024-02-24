import os
from typing import List

from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from wechatter.commands import commands as COMMANDS
from wechatter.models.scheduler import CronTask
from wechatter.models.wechat import QuotedResponse
from wechatter.sender import sender

# 一般来说，与数据库有交互的命令都不支持定时任务
UNSUPPORTED_COMMANDS = [
    "gpt4",
    "gpt4-chats",
    "gpt4-continue",
    "gpt4-record",
    "gpt",
    "gpt-chats",
    "gpt-continue",
    "gpt-record",
    "todo",
    "todo-remove",
    "help",
]

SEND_FILE_COMMANDS = ["qrcode"]


def parse_task_cron_list(task_cron_list: List) -> List:
    """
    解析任务定时规则列表
    :param task_cron_list: 任务定时规则列表
    :return cron_tasks: 任务定时任务列表
    """

    cron_tasks = []
    if not task_cron_list:
        return cron_tasks
    for task_cron in task_cron_list:
        try:
            # 用[]获取的字段表示该字段必填
            desc = task_cron["task"]
            enabled = task_cron["enabled"]
            cron = task_cron["cron"]
            # 安全检查
            second = cron["second"]
            if not _safety_check_second(second):
                second = "*/5"
                logger.warning(
                    f"为了保护帐号的安全，WeChatter 不允许低于每5秒级的定时任务，已将秒级定时任务转换为每5秒级定时任务: {desc}"
                )
            cron_trigger = CronTrigger(
                # 用get方法获取的字段表示该字段可以不写
                year=cron.get("year", "*"),
                month=cron.get("month", "*"),
                day=cron.get("day", "*"),
                week=cron.get("week", "*"),
                day_of_week=cron.get("day_of_week", "*"),
                hour=cron["hour"],
                minute=cron["minute"],
                second=second,
                start_date=cron.get("start_date", None),
                end_date=cron.get("end_date", None),
                timezone=cron.get("timezone", "Asia/Shanghai"),
            )
            funcs = []
            commands = task_cron["commands"]
            for command in commands:
                cmd = command["cmd"]
                # 不支持的定时任务的命令
                if cmd in UNSUPPORTED_COMMANDS:
                    logger.error(f"[{desc}] 任务的命令不支持定时任务: {cmd}")
                    raise ValueError(f"[{desc}] 任务的命令不支持定时任务: {cmd}")
                args = tuple(command.get("args", []))
                to_person_list = command.get("to_person_list", [])
                to_group_list = command.get("to_group_list", [])

                if not to_group_list and not to_person_list:
                    logger.warning(
                        f"[{desc}] 任务的命令没有指定发送目标，跳过此命令: {cmd}"
                    )
                    continue

                # 用户配置的命令名错误
                if not COMMANDS.get(cmd):
                    logger.error(f"[{desc}] 任务的命令不存在: {cmd}")
                    raise ValueError(f"[{desc}] 任务的命令不存在: {cmd}")

                def _func(_cmd: str, *_args):
                    # 如果命令支持引用回复
                    if COMMANDS[_cmd]["is_quotable"]:
                        try:
                            message, q_response = COMMANDS[_cmd]["mainfunc"](*_args)
                        except TypeError as e:
                            # 如果用户配置的参数不正确
                            logger.error(f"[{desc}] 任务的命令参数不正确: {str(e)}")
                            raise TypeError(f"[{desc}] 任务的命令参数不正确: {str(e)}")
                        quoted_response = QuotedResponse(
                            command=_cmd,
                            response=q_response,
                        )
                    else:  # 不支持引用回复的命令
                        try:
                            message = COMMANDS[_cmd]["mainfunc"](*_args)
                        except TypeError as e:
                            logger.error(f"[{desc}] 任务的命令参数不正确: {str(e)}")
                            raise TypeError(f"[{desc}] 任务的命令参数不正确: {str(e)}")
                        quoted_response = None
                    # 判断一下是发送文本消息还是文件
                    type = "text"
                    if cmd in SEND_FILE_COMMANDS:
                        type = "localfile"
                    # 发送消息
                    if to_person_list:
                        sender.mass_send_msg(
                            to_person_list,
                            message,
                            is_group=False,
                            type=type,
                            quoted_response=quoted_response,
                        )
                    if to_group_list:
                        sender.mass_send_msg(
                            to_group_list,
                            message,
                            is_group=True,
                            type=type,
                            quoted_response=quoted_response,
                        )
                    # 删除发送的文件
                    if _cmd in SEND_FILE_COMMANDS:
                        if os.path.exists(message):
                            os.remove(message)
                    logger.info(f"[{desc}] 任务的命令执行成功: {_cmd}")

                funcs.append((_func, (cmd, *args)))
        except KeyError as e:
            if task_cron.get("task"):
                logger.error(f"[{task_cron['task']}] 定时任务规则缺少 {e.args[0]} 字段")
            else:
                logger.error("定时任务规则缺少 task 字段")
        except ValueError as e:
            logger.error(f"解析定时任务规则失败: {str(e)}")
        except Exception as e:
            if task_cron.get("task"):
                logger.error(f"[{task_cron['task']}] 定时任务规则解析失败: {str(e)}")
            else:
                logger.error(f"定时任务规则解析失败: {str(e)}")
        else:
            cron_task = CronTask(
                desc=desc,
                enabled=enabled,
                cron_trigger=cron_trigger,
                funcs=funcs,
            )
            cron_tasks.append(cron_task)

    return cron_tasks


def _safety_check_second(second: str) -> bool:
    """
    安全检查定时任务的秒级规则
    """
    if second == "*":
        return False
    dangerous_suffixes = ["/0", "/1", "/2", "/3", "/4"]
    for suffix in dangerous_suffixes:
        if second.endswith(suffix):
            return False
    return True
