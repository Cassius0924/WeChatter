from loguru import logger

ESSENTIAL_TOP_FIELDS = [
    "wechatter_port",
    "wx_webhook_base_api",
    "wx_webhook_recv_api_path",
    "wx_webhook_token",
    "bot_name",
    "need_mentioned",
    "github_webhook_enabled",
    "github_webhook_api_path",
    "message_forwarding_enabled",
    "message_forwarding_rule_list",
    "official_account_reminder_enabled",
    "official_account_reminder_rule_list",
    "all_task_cron_enabled",
    "task_cron_list",
    "discord_message_forwarding_enabled",
    "discord_message_forwarding_rule_list",
]


def validate_config(config):
    """
    验证配置，验证是否存在必要字段
    :param config: 配置文件
    """
    logger.info("正在验证配置文件...")

    # 顶层字段验证
    for field in ESSENTIAL_TOP_FIELDS:
        if field not in config:
            error_msg = f"配置参数错误：缺少必要字段 {field}"
            logger.critical(error_msg)
            raise ValueError(error_msg)

    # 公众号提醒配置
    # valid_types = ["text", "image"]
    # if config["official_account_reminder_type"] not in valid_types:
    #     error_msg = (
    #         f"配置参数错误：official_account_reminder_type 参数可选择为 {valid_types} "
    #     )
    #     logger.critical(error_msg)
    #     raise ValueError(error_msg)

    # 定时任务配置
    ess_fields = ["task", "cron", "commands"]
    for i, task_cron in enumerate(config["task_cron_list"]):
        # task_cron_list 字段验证
        for field in ess_fields:
            if field not in task_cron:
                error_msg = f"配置参数错误：task_cron_list[{i}] 缺少必要字段 {field}"
                logger.critical(error_msg)
                raise ValueError(error_msg)

            # cron 字段验证
            cron_ess_fields = ["hour", "minute", "second"]
            for field in cron_ess_fields:
                if field not in task_cron["cron"]:
                    error_msg = (
                        f"配置参数错误：task_cron_list[{i}].cron 缺少必要字段 {field}"
                    )
                    logger.critical(error_msg)
                    raise ValueError(error_msg)

            # commands 字段验证
            for i2, command in enumerate(task_cron["commands"]):
                commands_ess_fields = ["cmd"]
                for field in commands_ess_fields:
                    if field not in command:
                        error_msg = f"配置参数错误：task_cron_list[{i}].commands[{i2}] 缺少必要字段 {field}"
                        logger.critical(error_msg)
                        raise ValueError(error_msg)
    # 微信消息转发配置
    ess_fields = ["from_list"]
    for i, rule in enumerate(config["message_forwarding_rule_list"]):
        for field in ess_fields:
            if field not in rule:
                error_msg = f"配置参数错误：message_forwarding_rule_list[{i}] 缺少必要字段 {field}"
                logger.critical(error_msg)
                raise ValueError(error_msg)

    # Discord 消息转发配置
    ess_fields = ["from_list", "webhook_url"]
    for i, rule in enumerate(config["discord_message_forwarding_rule_list"]):
        for field in ess_fields:
            if field not in rule:
                error_msg = f"配置参数错误：discord_message_forwarding_rule_list[{i}] 缺少必要字段 {field}"
                logger.critical(error_msg)
                raise ValueError(error_msg)

    logger.info("配置文件验证通过！")
