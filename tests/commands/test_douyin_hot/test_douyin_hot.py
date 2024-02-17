import json
import unittest

from wechatter.commands._commands import douyin_hot


class TestDouyinHotCommand(unittest.TestCase):
    def setUp(self):
        with open("tests/commands/test_douyin_hot/douyin_hot_response.json") as f:
            self.r_json = json.load(f)
            self.douyin_hot_list = self.r_json["word_list"]

    def test_extract_douyin_hot_data_success(self):
        result = douyin_hot._extract_douyin_hot_data(self.r_json)
        self.assertListEqual(result, self.douyin_hot_list)

    def test_extract_douyin_hot_data_failure(self):
        with self.assertRaises(Exception):
            douyin_hot._extract_douyin_hot_data({})

    def test_generate_douyin_hot_message_success(self):
        result = douyin_hot._generate_douyin_hot_message(self.r_json["word_list"])
        true_result = "1.  董宇辉对刘德华说想演兵马俑\n2.  今年春联是自己写的\n3.  中国同23国全面互免签证\n4.  暗夜变装挑战\n5.  晒出你的新春红\n6.  相亲相爱接力挑战\n7.  诀别书的正确打开方式\n8.  2月第一天\n9.  北京产权交易所澄清声明\n10.  贵州有多钟爱办酒席\n11.  各地人这么做一定有原因\n12.  韩国瑜当选台立法机构负责人\n13.  一起跳甜妹手势舞\n14.  上海楼房凌晨坍塌 多方回应\n15.  刘德华宁浩红毯先生今晚直播\n16.  没有同桌我可怎么办啊\n17.  河北一保安阻止奔驰加塞被顶撞\n18.  网友过年爱上组养生局了\n19.  召集全抖音晚8找乐子\n20.  春运期间天气预测"
        self.assertIn(true_result, result)

    def test_generate_douyin_hot_message_empty_list(self):
        result = douyin_hot._generate_douyin_hot_message([])
        self.assertEqual(result, "暂无抖音热搜")
