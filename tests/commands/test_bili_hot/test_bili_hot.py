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
