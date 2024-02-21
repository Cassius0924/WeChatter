import json
import unittest

from wechatter.commands._commands import weibo_hot


class TestWeiboHotCommand(unittest.TestCase):
    def setUp(self):
        with open("tests/commands/test_weibo_hot/weibo_hot_response.json") as f:
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
        self.assertEqual(result, "微博热搜列表为空")

    def test_generate_weibo_hot_quoted_response_success(self):
        result = weibo_hot._generate_weibo_hot_quoted_response(self.weibo_hot_list)
        true_result = '{"1": "https://s.weibo.com/weibo?q=%E5%B0%86%E4%B8%AD%E6%B3%95%E5%85%B3%E7%B3%BB%E6%89%93%E9%80%A0%E5%BE%97%E6%9B%B4%E5%8A%A0%E7%89%A2%E5%9B%BA%E5%92%8C%E5%AF%8C%E6%9C%89%E6%B4%BB%E5%8A%9B", "2": "https://s.weibo.com/weibo?q=%E9%9F%A9%E5%BA%9A%E9%9F%A9%E5%9B%BD%20%E6%8A%91%E9%83%81", "3": "https://s.weibo.com/weibo?q=6%E5%A4%A9%E7%8F%AD", "4": "https://s.weibo.com/weibo?q=%E4%BD%95%E4%BB%A5%E4%B8%AD%E5%9B%BD%E5%90%91%E6%B5%B7%E6%B3%89%E5%B7%9E", "5": "https://s.weibo.com/weibo?q=%E7%A5%9D%E4%BD%A0KFC%E7%A5%9D%E4%BD%A0%E5%BF%AB%E5%8F%91%E8%B4%A2", "6": "https://s.weibo.com/weibo?q=%E4%B8%A4%E4%B8%AA14%E5%B2%81%E7%9A%84%E4%B8%8A%E6%B5%B7%E5%A5%B3%E5%AD%A6%E7%94%9F%E7%9A%84%E9%87%87%E8%AE%BF", "7": "https://s.weibo.com/weibo?q=%E6%88%91%E5%9B%BD%E5%A5%B3%E6%80%A7HPV%E6%84%9F%E6%9F%93%E7%8E%87%E5%91%88%E5%8F%8C%E5%B3%B0%E5%88%86%E5%B8%83", "8": "https://s.weibo.com/weibo?q=%E6%94%AF%E4%BB%98%E5%AE%9D%E4%BA%94%E7%A6%8F", "9": "https://s.weibo.com/weibo?q=%E7%BD%91%E6%B0%91%E5%8F%91%E5%B8%83%E4%B8%AD%E5%AD%A6%E5%8F%91%E7%94%9F%E6%80%A7%E4%BE%B5%E8%99%9A%E5%81%87%E4%BF%A1%E6%81%AF%E8%A2%AB%E6%8B%98", "10": "https://s.weibo.com/weibo?q=%E7%94%B7%E5%AD%90%E4%B8%BE%E6%8A%A5%E7%BA%AA%E5%A7%94%E5%B9%B2%E9%83%A840%E5%88%86%E9%92%9F%E5%90%8E%E5%B0%B1%E8%A2%AB%E6%8A%93", "11": "https://s.weibo.com/weibo?q=9%E9%83%A8%E7%94%B5%E5%BD%B1%E5%AE%98%E5%AE%A32024%E6%98%A5%E8%8A%82%E6%A1%A3", "12": "https://s.weibo.com/weibo?q=%E8%82%89%E9%A9%AC%E5%B0%94", "13": "https://s.weibo.com/weibo?q=%E5%94%AF%E4%B8%80%E7%9A%84%E5%A7%90%E4%B8%81%E6%B3%BD%E4%BB%81", "14": "https://s.weibo.com/weibo?q=%E7%BD%91%E5%8F%8B%E7%A7%B0%E9%99%88%E7%89%A7%E9%A9%B0%E6%89%94%E4%BA%86%E7%B2%89%E4%B8%9D%E9%80%81%E7%9A%84%E7%A4%BC%E7%89%A9", "15": "https://s.weibo.com/weibo?q=%E5%AD%99%E7%BA%A2%E9%9B%B7%E5%9B%9E%E5%BA%94%E9%BB%84%E6%B8%A4%E5%BC%A0%E8%89%BA%E5%85%B4%E4%B8%8D%E5%B8%A6%E8%87%AA%E5%B7%B1%E7%8E%A9", "16": "https://s.weibo.com/weibo?q=%E9%95%BF%E5%A4%A7%E4%BA%86%E7%9C%8B%E5%B0%8F%E5%AD%A9%E7%BB%93%E5%A9%9A", "17": "https://s.weibo.com/weibo?q=%E5%A4%A9%E5%AE%98%E8%B5%90%E7%A6%8F%E7%BA%A2%E5%8C%85", "18": "https://s.weibo.com/weibo?q=%E6%9B%9D%E5%91%A8%E8%BF%85%E8%B5%B5%E4%B8%BD%E9%A2%96%E6%9D%A8%E7%B4%AB%E4%BA%89%E6%BC%94%E5%BC%A0%E8%89%BA%E8%B0%8B%E6%96%B0%E5%89%A7", "19": "https://s.weibo.com/weibo?q=%E5%AC%9B%E5%AC%9B%20%E6%9C%95%E5%87%BA%E4%B8%93%E8%BE%91%E5%95%A6", "20": "https://s.weibo.com/weibo?q=%E5%A4%AB%E5%A6%BB%E5%88%86%E5%B1%85%E5%9E%8B%E6%98%A5%E8%8A%82"}'
        self.assertEqual(result, true_result)
