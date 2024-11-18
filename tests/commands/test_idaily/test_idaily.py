import json
import unittest

from wechatter.commands._commands import idaily


class TestIdailyCommand(unittest.TestCase):
    def setUp(self):
        with open(
                "tests/commands/test_idaily/idaily_response.json"
        ) as f:
            self.tih_response = json.load(f)
            self.tih_list = self.tih_response

    def test_extract_idaily_data_success(self):
        result = idaily._extract_idaily_data(self.tih_response)
        self.assertListEqual(result, self.tih_list)

    def test_generate_idaily_message_success(self):
        result = idaily._generate_idaily_message(self.tih_list)
        true_result = "✨=====每日环球视野=====✨\n今天的iDaily还没更新，现在为您呈现的是：\n🗓️ 时间: November 17, 2024\n1. 🌎 泰国庆祝天灯节\n    🌪️ 泰国民众放飞孔明灯庆祝「天灯节」（Yi Peng festival），清迈。「天灯节」是泰国北部地区的传统节日，历史可追溯至13世纪泰北兰纳王国时期，庆祝日期为每年泰国农历第12个月的满月日，人们会放飞孔明灯庆祝新一年即将开始。泰国旅游部数据显示2024年1至10月接待外国游客超过2900万人次，创造1.35万亿泰铢（约合393亿美元）旅游业收入，前5大游客来源国依次为中国、马来西亚、印度、韩国和俄罗斯。摄影师：Manan Vatsyayana\n2. 🌎 中美元首利马会晤\n    🌪️ 中国国家主席习近平与美国总统 Joe Biden 在 APEC 峰会期间举行会晤，秘鲁利马。11月16日，中美两国领导人就双边关系、人工智能治理、地区及国际局势议题举行1小时45分钟会谈。习近平就台湾问题、中国南海、经贸科技、网络安全、乌克兰危机、朝鲜半岛局势等重大问题阐明中方立场。Biden 强调美国的一个中国政策保持不变，对中国支持俄罗斯国防工业深表关切，对中国不公平的贸易政策表示担忧。双方一致认为应以慎重负责的态度发展军事领域的人工智能技术，应维持由人类控制核武器使用的决定。美国总统 Biden 将于2025年1月正式卸任。摄影师：Leah Millis\n3. 🌎 美日韩首脑三边会谈\n    🌪️ 美国总统 Joe Biden、日本首相石破茂与韩国总统尹锡悦在 APEC 峰会期间举行三方会晤，秘鲁利马。11月15日，美国总统 Biden 任内最后一次出席美日韩首脑峰会，三方就乌克兰、朝鲜、印太局势等议题举行约40分钟会晤并发表联合声明。三国声明强烈谴责俄罗斯和朝鲜加强军事合作，重申支持乌克兰自卫权，坚决反对中国南海地区的非法海洋权利主张和军事胁迫行为，呼吁和平解决台湾问题。三国宣布设立「美日韩合作秘书处」负责协调三方政策与行动。摄影师：iDaily Media' not found in '✨====每日环球视野====✨\n今天的iDaily还没更新，现在为您呈现的是：\n🗓️ 时间: November 17, 2024\n1. 🌎 泰国庆祝天灯节\n    🌪️ 泰国民众放飞孔明灯庆祝「天灯节」（Yi Peng festival），清迈。「天灯节」是泰国北部地区的传统节日，历史可追溯至13世纪泰北兰纳王国时期，庆祝日期为每年泰国农历第12个月的满月日，人们会放飞孔明灯庆祝新一年即将开始。泰国旅游部数据显示2024年1至10月接待外国游客超过2900万人次，创造1.35万亿泰铢（约合393亿美元）旅游业收入，前5大游客来源国依次为中国、马来西亚、印度、韩国和俄罗斯。摄影师：Manan Vatsyayana\n2. 🌎 中美元首利马会晤\n    🌪️ 中国国家主席习近平与美国总统 Joe Biden 在 APEC 峰会期间举行会晤，秘鲁利马。11月16日，中美两国领导人就双边关系、人工智能治理、地区及国际局势议题举行1小时45分钟会谈。习近平就台湾问题、中国南海、经贸科技、网络安全、乌克兰危机、朝鲜半岛局势等重大问题阐明中方立场。Biden 强调美国的一个中国政策保持不变，对中国支持俄罗斯国防工业深表关切，对中国不公平的贸易政策表示担忧。双方一致认为应以慎重负责的态度发展军事领域的人工智能技术，应维持由人类控制核武器使用的决定。美国总统 Biden 将于2025年1月正式卸任。摄影师：Leah Millis"
        self.assertIn(true_result, result)

    def test_generate_idaily_message_empty_list(self):
        result = idaily._generate_idaily_message([])
        self.assertEqual(result, "暂无每日环球视野")
