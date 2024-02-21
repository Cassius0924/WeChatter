import json
import unittest

from wechatter.commands._commands import bili_hot


class TestBiliHotCommand(unittest.TestCase):
    def setUp(self):
        with open("tests/commands/test_bili_hot/bili_hot_response.json") as f:
            self.r_json = json.load(f)
            self.bili_hot_list = self.r_json["data"]["list"]

    def test_extract_bili_hot_data_success(self):
        result = bili_hot._extract_bili_hot_data(self.r_json)
        self.assertListEqual(result, self.bili_hot_list)

    def test_extract_bili_hot_data_failure(self):
        with self.assertRaises(Exception):
            bili_hot._extract_bili_hot_data({})

    def test_generate_bili_hot_message_success(self):
        result = bili_hot._generate_bili_hot_message(self.r_json["data"]["list"])
        true_result = "1. 复旦教师杀害学院书记被判死缓\n2. 免费领取心魔\n3. 扎克伯格道歉\n4. 易烊千玺当选中国影协理事\n5. kei和marin分手\n6. 上海禁止网约车在浦东机场运营\n7. 中国豆浆机在韩国热销\n8. 何同学工作室首次公开\n9. 官方称确定国花时机未成熟\n10. Aimer参演原神新春会\n11. 总台龙年春晚动画宣传片\n12. 只解冻刘德华太保守了\n13. 烟花引发住宅起火致老人去世\n14. 750万人在等尊严死\n15. 坠亡姐弟生母被送医院\n16. 不绵之夜\n17. 清华宣布脑机接口重大突破\n18. Uzi 使用替身攻击\n19. 捡雪吃患病连烧八天\n20. 幻塔EVA联动明日香登场"
        self.assertIn(true_result, result)

    def test_generate_bili_hot_message_empty_list(self):
        result = bili_hot._generate_bili_hot_message([])
        self.assertEqual(result, "暂无Bilibili热搜")

    def test_generate_bili_hot_quoted_response_success(self):
        result = bili_hot._generate_bili_hot_quoted_response(
            self.r_json["data"]["list"]
        )
        true_result = '{"1": "https://search.bilibili.com/all?keyword=%E5%A4%8D%E6%97%A6%E6%95%99%E5%B8%88%E6%9D%80%E5%AE%B3%E5%AD%A6%E9%99%A2%E4%B9%A6%E8%AE%B0%E8%A2%AB%E5%88%A4%E6%AD%BB%E7%BC%93", "2": "https://search.bilibili.com/all?keyword=%E5%85%8D%E8%B4%B9%E9%A2%86%E5%8F%96%E5%BF%83%E9%AD%94", "3": "https://search.bilibili.com/all?keyword=%E6%89%8E%E5%85%8B%E4%BC%AF%E6%A0%BC%E9%81%93%E6%AD%89", "4": "https://search.bilibili.com/all?keyword=%E6%98%93%E7%83%8A%E5%8D%83%E7%8E%BA%E5%BD%93%E9%80%89%E4%B8%AD%E5%9B%BD%E5%BD%B1%E5%8D%8F%E7%90%86%E4%BA%8B", "5": "https://search.bilibili.com/all?keyword=kei%E5%92%8Cmarin%E5%88%86%E6%89%8B", "6": "https://search.bilibili.com/all?keyword=%E4%B8%8A%E6%B5%B7%E7%A6%81%E6%AD%A2%E7%BD%91%E7%BA%A6%E8%BD%A6%E5%9C%A8%E6%B5%A6%E4%B8%9C%E6%9C%BA%E5%9C%BA%E8%BF%90%E8%90%A5", "7": "https://search.bilibili.com/all?keyword=%E4%B8%AD%E5%9B%BD%E8%B1%86%E6%B5%86%E6%9C%BA%E5%9C%A8%E9%9F%A9%E5%9B%BD%E7%83%AD%E9%94%80", "8": "https://search.bilibili.com/all?keyword=%E4%BD%95%E5%90%8C%E5%AD%A6%E5%B7%A5%E4%BD%9C%E5%AE%A4%E9%A6%96%E6%AC%A1%E5%85%AC%E5%BC%80", "9": "https://search.bilibili.com/all?keyword=%E5%AE%98%E6%96%B9%E7%A7%B0%E7%A1%AE%E5%AE%9A%E5%9B%BD%E8%8A%B1%E6%97%B6%E6%9C%BA%E6%9C%AA%E6%88%90%E7%86%9F", "10": "https://search.bilibili.com/all?keyword=Aimer%E5%8F%82%E6%BC%94%E5%8E%9F%E7%A5%9E%E6%96%B0%E6%98%A5%E4%BC%9A", "11": "https://search.bilibili.com/all?keyword=%E6%80%BB%E5%8F%B0%E9%BE%99%E5%B9%B4%E6%98%A5%E6%99%9A%E5%8A%A8%E7%94%BB%E5%AE%A3%E4%BC%A0%E7%89%87", "12": "https://search.bilibili.com/all?keyword=%E5%8F%AA%E8%A7%A3%E5%86%BB%E5%88%98%E5%BE%B7%E5%8D%8E%E5%A4%AA%E4%BF%9D%E5%AE%88%E4%BA%86", "13": "https://search.bilibili.com/all?keyword=%E7%83%9F%E8%8A%B1%E5%BC%95%E5%8F%91%E4%BD%8F%E5%AE%85%E8%B5%B7%E7%81%AB%E8%87%B4%E8%80%81%E4%BA%BA%E5%8E%BB%E4%B8%96", "14": "https://search.bilibili.com/all?keyword=750%E4%B8%87%E4%BA%BA%E5%9C%A8%E7%AD%89%E5%B0%8A%E4%B8%A5%E6%AD%BB", "15": "https://search.bilibili.com/all?keyword=%E5%9D%A0%E4%BA%A1%E5%A7%90%E5%BC%9F%E7%94%9F%E6%AF%8D%E8%A2%AB%E9%80%81%E5%8C%BB%E9%99%A2", "16": "https://search.bilibili.com/all?keyword=%E4%B8%8D%E7%BB%B5%E4%B9%8B%E5%A4%9C", "17": "https://search.bilibili.com/all?keyword=%E6%B8%85%E5%8D%8E%E5%AE%A3%E5%B8%83%E8%84%91%E6%9C%BA%E6%8E%A5%E5%8F%A3%E9%87%8D%E5%A4%A7%E7%AA%81%E7%A0%B4", "18": "https://search.bilibili.com/all?keyword=Uzi%20%E4%BD%BF%E7%94%A8%E6%9B%BF%E8%BA%AB%E6%94%BB%E5%87%BB", "19": "https://search.bilibili.com/all?keyword=%E6%8D%A1%E9%9B%AA%E5%90%83%E6%82%A3%E7%97%85%E8%BF%9E%E7%83%A7%E5%85%AB%E5%A4%A9", "20": "https://search.bilibili.com/all?keyword=%E5%B9%BB%E5%A1%94EVA%E8%81%94%E5%8A%A8%E6%98%8E%E6%97%A5%E9%A6%99%E7%99%BB%E5%9C%BA"}'
        self.assertEqual(result, true_result)
