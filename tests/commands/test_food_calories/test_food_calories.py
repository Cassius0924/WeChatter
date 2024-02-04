import json
import unittest

from requests import Response

from wechatter.commands._commands import food_calories
from wechatter.exceptions import Bs4ParsingError


class TestFoodCaloriesCommand(unittest.TestCase):
    def setUp(self):
        with open('tests/commands/test_food_calories/food_calories_response.html.test') as f:
            r_html = f.read()
        self.food_calories_response = Response()
        self.food_calories_response._content = r_html.encode('utf-8')
        with open("tests/commands/test_food_calories/one_food_response.html.test") as f:
            one_food_r_html = f.read()
        self.one_food_response = Response()
        self.one_food_response._content = one_food_r_html.encode('utf-8')
        with open('tests/commands/test_food_calories/food_href_list.json') as f:
            self.food_href_list = json.load(f)
        with open("tests/commands/test_food_calories/food_detail_list.json") as f:
            self.food_detail_list = json.load(f)
        with open("tests/commands/test_food_calories/one_food_detail.json") as f:
            self.one_food_detail = json.load(f)
        with open("tests/commands/test_food_calories/result") as f:
            self.result = f.read()

    def test_parse_food_href_list_response_success(self):
        result = food_calories.parse_food_href_list_response(self.food_calories_response)
        self.assertEqual(result, self.food_href_list)

    def test_parse_food_href_list_response_failure(self):
        with self.assertRaises(Bs4ParsingError):
            food_calories.parse_food_href_list_response(Response())

    def test_get_food_detail_list_success(self):
        result = food_calories.get_food_detail_list(self.food_href_list)
        self.assertEqual(result, self.food_detail_list)

    def test_get_food_detail_list_failure(self):
        with self.assertRaises(Exception):
            food_calories.get_food_detail_list([])

    def test_parse_food_detail_response_success(self):
        result = food_calories.parse_food_detail_response(self.one_food_response, "牛肉丸，又叫火锅牛肉丸子，火锅牛肉丸")
        self.assertEqual(result, self.one_food_detail)

    def test_parse_food_detail_response_failure(self):
        with self.assertRaises(Bs4ParsingError):
            food_calories.parse_food_detail_response(Response(), "牛肉丸，又叫火锅牛肉丸子，火锅牛肉丸")

    def test_generate_food_message_success(self):
        result = food_calories.generate_food_message(self.food_detail_list)
        rs = """
✨=====食物列表=====✨
1. 牛肉(肥瘦)，又叫肥牛
🍲热量(大卡):    125.00
🍞碳水(克):        2.00
🥓脂肪(克):        4.20
🍗蛋白质(克):    19.90
🥦纤维素(克):    一
2. 牛肉(精瘦)，又叫牛肉，瘦牛肉
🍲热量(大卡):    113.00
🍞碳水(克):        1.30
🥓脂肪(克):        2.50
🍗蛋白质(克):    21.30
🥦纤维素(克):    0.00
3. 牛腩，又叫牛肉（牛腩）、牛腩
🍲热量(大卡):    332.00
🍞碳水(克):        0.00
🥓脂肪(克):        29.30
🍗蛋白质(克):    17.10
🥦纤维素(克):    0.00
4. 肥牛卷，又叫肥牛、火锅牛肉卷、牛肉卷
🍲热量(大卡):    250.00
🍞碳水(克):        0.02
🥓脂肪(克):        18.73
🍗蛋白质(克):    19.06
🥦纤维素(克):    0.00
5. 牛肉丸，又叫火锅牛肉丸子，火锅牛肉丸
🍲热量(大卡):    115.00
🍞碳水(克):        9.00
🥓脂肪(克):        3.70
🍗蛋白质(克):    11.20
🥦纤维素(克):    0.00
🔵====含量(100克)====🔵
        """
        self.assertEqual(result, rs)

    def test_generate_food_message_failure(self):
        with self.assertRaises(Exception):
            food_calories.generate_food_message([])

    def test_get_url_encoding_success(self):
        result = food_calories.get_url_encoding("牛肉丸")
        self.assertEqual(result, "%E7%89%9B%E8%82%89%E4%B8%B8")
