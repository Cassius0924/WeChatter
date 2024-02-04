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
        with open("tests/commands/test_food_calories/food_response.html.test") as f:
            food_r_html = f.read()
        self.food_response = Response()
        self.food_response._content = food_r_html.encode('utf-8')
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

    # def test_generate_food_message_success(self):
    #     result = food_calories.generate_food_message(self.food_calories)
    #     self.assertEqual(result, self.food_calories)
    #
    # def test_generate_food_message_failure(self):
    #     with self.assertRaises(Exception):
    #         food_calories.generate_food_message([])
