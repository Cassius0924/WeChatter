import unittest
import json
from wechatter.commands._commands import weibo_hot


class TestWeiboHotCommand(unittest.TestCase):

    def setUp(self):
        with open('tests/commands/test_weibo_hot/weibo_hot_response.json') as f:
            self.r_json = json.load(f)
            self.weibo_hot_list = self.r_json["data"]["cards"][0]["card_group"][:20]

    def test_extract_weibo_hot_data_success(self):
        result = weibo_hot._extract_weibo_hot_data(self.r_json)
        self.assertEqual(result, self.weibo_hot_list)

    def test_extract_weibo_hot_data_failure(self):
        with self.assertRaises(Exception):
            weibo_hot._extract_weibo_hot_data({})

    def test_generate_weibo_hot_message_success(self):
        result = weibo_hot._generate_weibo_hot_message(self.weibo_hot_list)
        true_result = "1. 将中法关系打造得更加牢固和富有活力\n2. 韩庚韩国 抑郁\n3. 6天班\n4. 何以中国向海泉州\n5. 祝你KFC祝你快发财\n6. 两个14岁的上海女学生的采访\n7. 我国女性HPV感染率呈双峰分布\n8. 支付宝五福\n9. 网民发布中学发生性侵虚假信息被拘\n10. 男子举报纪委干部40分钟后就被抓\n11. 9部电影官宣2024春节档\n12. 肉马尔\n13. 唯一的姐丁泽仁\n14. 网友称陈牧驰扔了粉丝送的礼物\n15. 孙红雷回应黄渤张艺兴不带自己玩\n16. 长大了看小孩结婚\n17. 天官赐福红包\n18. 曝周迅赵丽颖杨紫争演张艺谋新剧\n19. 嬛嬛 朕出专辑啦\n20. 夫妻分居型春节"
        self.assertIn(true_result, result)

    def test_generate_weibo_hot_message_empty_list(self):
        result = weibo_hot._generate_weibo_hot_message([])
        self.assertEqual(result, '微博热搜列表为空')
