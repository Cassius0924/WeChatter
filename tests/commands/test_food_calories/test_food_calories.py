import unittest
import json

from requests import Response

from wechatter.commands._commands import food_calories
from wechatter.exceptions import Bs4ParsingError


class TestFoodCaloriesCommand(unittest.TestCase):
        def setUp(self):
            with open('tests/commands/test_food_calories/food_calories_response.html.test') as f:
                r_html = f.read()
            self.response = Response()
            self.response._content = r_html.encode('utf-8')
            with open('tests/commands/test_food_calories/food_href_list.json') as f:
                self.food_href_list = json.load(f)

        def test_parse_food_href_list_response_success(self):
            result = food_calories.parse_food_href_list_response(self.response)
            self.assertEqual(result, self.food_href_list)

        def test_parse_food_href_list_response_failure(self):
            with self.assertRaises(Bs4ParsingError):
                food_calories.parse_food_href_list_response(Response())

        def test_get_food_detail_list_success(self):
            result = food_calories.get_food_detail_list(self.food_href_list)
            self.assertEqual(result, self.food_calories)

        def test_get_food_detail_list_failure(self):
            with self.assertRaises(Exception):
                food_calories.get_food_detail_list([])

        def test_generate_food_message_success(self):
            result = food_calories.generate_food_message(self.food_calories)
            self.assertEqual(result, self.food_calories)

        def test_generate_food_message_failure(self):
            with self.assertRaises(Exception):
                food_calories.generate_food_message([])
