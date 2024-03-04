from typing import Dict, List, Tuple


def parse_discord_message_forwarding_rule_list(rule_list: List) -> Tuple[Dict, Dict]:
    """
    解析消息转发规则列表
    :param rule_list: 消息转发规则列表
    :return: 转发规则元组，第一个元素为全局转发规则，第二个元素为特定转发规则
    """
    all_message_rule = {
        "is_none": True,
        "from_list_exclude": [],
        "webhook_url": "",
    }
    specific_message_rules = {}
    for rule in rule_list:
        if "%ALL" in rule["from_list"]:
            all_message_rule["is_none"] = False
            all_message_rule["from_list_exclude"].extend(
                rule.get("from_list_exclude", [])
            )
            all_message_rule["webhook_url"] = rule["webhook_url"]
        else:
            for from_name in rule["from_list"]:
                if from_name not in specific_message_rules:
                    specific_message_rules[from_name] = {
                        "webhook_url": [],
                    }
                specific_message_rules[from_name]["webhook_url"] = rule["webhook_url"]
    return all_message_rule, specific_message_rules
