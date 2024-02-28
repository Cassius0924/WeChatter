from typing import Dict, List


def parse_official_account_reminder_rule_list(rule_list: List) -> Dict:
    """
    :param rule_list: 公众号文章提醒规则列表
    :return: 公众号文章提醒规则
    """
    reminder_rule = {}
    for rule in rule_list:
        for oa_name in rule["oa_name_list"]:
            if oa_name not in reminder_rule:
                reminder_rule[oa_name] = {"to_person_list": [], "to_group_list": []}
            reminder_rule[oa_name]["to_person_list"].extend(
                rule.get("to_person_list", [])
            )
            reminder_rule[oa_name]["to_group_list"].extend(
                rule.get("to_group_list", [])
            )
    return reminder_rule
