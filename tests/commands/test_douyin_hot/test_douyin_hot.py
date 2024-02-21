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

    def test_generate_douyin_hot_quoted_response_success(self):
        result = douyin_hot._generate_douyin_hot_quoted_response(
            self.r_json["word_list"]
        )
        true_result = '{"1": "https://www.douyin.com/search/%E8%91%A3%E5%AE%87%E8%BE%89%E5%AF%B9%E5%88%98%E5%BE%B7%E5%8D%8E%E8%AF%B4%E6%83%B3%E6%BC%94%E5%85%B5%E9%A9%AC%E4%BF%91", "2": "https://www.douyin.com/search/%E4%BB%8A%E5%B9%B4%E6%98%A5%E8%81%94%E6%98%AF%E8%87%AA%E5%B7%B1%E5%86%99%E7%9A%84", "3": "https://www.douyin.com/search/%E4%B8%AD%E5%9B%BD%E5%90%8C23%E5%9B%BD%E5%85%A8%E9%9D%A2%E4%BA%92%E5%85%8D%E7%AD%BE%E8%AF%81", "4": "https://www.douyin.com/search/%E6%9A%97%E5%A4%9C%E5%8F%98%E8%A3%85%E6%8C%91%E6%88%98", "5": "https://www.douyin.com/search/%E6%99%92%E5%87%BA%E4%BD%A0%E7%9A%84%E6%96%B0%E6%98%A5%E7%BA%A2", "6": "https://www.douyin.com/search/%E7%9B%B8%E4%BA%B2%E7%9B%B8%E7%88%B1%E6%8E%A5%E5%8A%9B%E6%8C%91%E6%88%98", "7": "https://www.douyin.com/search/%E8%AF%80%E5%88%AB%E4%B9%A6%E7%9A%84%E6%AD%A3%E7%A1%AE%E6%89%93%E5%BC%80%E6%96%B9%E5%BC%8F", "8": "https://www.douyin.com/search/2%E6%9C%88%E7%AC%AC%E4%B8%80%E5%A4%A9", "9": "https://www.douyin.com/search/%E5%8C%97%E4%BA%AC%E4%BA%A7%E6%9D%83%E4%BA%A4%E6%98%93%E6%89%80%E6%BE%84%E6%B8%85%E5%A3%B0%E6%98%8E", "10": "https://www.douyin.com/search/%E8%B4%B5%E5%B7%9E%E6%9C%89%E5%A4%9A%E9%92%9F%E7%88%B1%E5%8A%9E%E9%85%92%E5%B8%AD", "11": "https://www.douyin.com/search/%E5%90%84%E5%9C%B0%E4%BA%BA%E8%BF%99%E4%B9%88%E5%81%9A%E4%B8%80%E5%AE%9A%E6%9C%89%E5%8E%9F%E5%9B%A0", "12": "https://www.douyin.com/search/%E9%9F%A9%E5%9B%BD%E7%91%9C%E5%BD%93%E9%80%89%E5%8F%B0%E7%AB%8B%E6%B3%95%E6%9C%BA%E6%9E%84%E8%B4%9F%E8%B4%A3%E4%BA%BA", "13": "https://www.douyin.com/search/%E4%B8%80%E8%B5%B7%E8%B7%B3%E7%94%9C%E5%A6%B9%E6%89%8B%E5%8A%BF%E8%88%9E", "14": "https://www.douyin.com/search/%E4%B8%8A%E6%B5%B7%E6%A5%BC%E6%88%BF%E5%87%8C%E6%99%A8%E5%9D%8D%E5%A1%8C%20%E5%A4%9A%E6%96%B9%E5%9B%9E%E5%BA%94", "15": "https://www.douyin.com/search/%E5%88%98%E5%BE%B7%E5%8D%8E%E5%AE%81%E6%B5%A9%E7%BA%A2%E6%AF%AF%E5%85%88%E7%94%9F%E4%BB%8A%E6%99%9A%E7%9B%B4%E6%92%AD", "16": "https://www.douyin.com/search/%E6%B2%A1%E6%9C%89%E5%90%8C%E6%A1%8C%E6%88%91%E5%8F%AF%E6%80%8E%E4%B9%88%E5%8A%9E%E5%95%8A", "17": "https://www.douyin.com/search/%E6%B2%B3%E5%8C%97%E4%B8%80%E4%BF%9D%E5%AE%89%E9%98%BB%E6%AD%A2%E5%A5%94%E9%A9%B0%E5%8A%A0%E5%A1%9E%E8%A2%AB%E9%A1%B6%E6%92%9E", "18": "https://www.douyin.com/search/%E7%BD%91%E5%8F%8B%E8%BF%87%E5%B9%B4%E7%88%B1%E4%B8%8A%E7%BB%84%E5%85%BB%E7%94%9F%E5%B1%80%E4%BA%86", "19": "https://www.douyin.com/search/%E5%8F%AC%E9%9B%86%E5%85%A8%E6%8A%96%E9%9F%B3%E6%99%9A8%E6%89%BE%E4%B9%90%E5%AD%90", "20": "https://www.douyin.com/search/%E6%98%A5%E8%BF%90%E6%9C%9F%E9%97%B4%E5%A4%A9%E6%B0%94%E9%A2%84%E6%B5%8B"}'
        self.assertEqual(result, true_result)
