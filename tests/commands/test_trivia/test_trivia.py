import json
import unittest

from requests import Response

from wechatter.commands._commands import trivia
from wechatter.exceptions import Bs4ParsingError


class TestTriviaCommand(unittest.TestCase):
    def setUp(self):
        with open("tests/commands/test_trivia/trivia_response.html.test") as f:
            r_html = f.read()
        self.response = Response()
        self.response._content = r_html.encode("utf-8")
        with open("tests/commands/test_trivia/trivia_data.json") as f:
            self.trivia_list = json.load(f)

    def test_parse_trivia_response_success(self):
        result = trivia._parse_trivia_response(self.response)
        self.assertListEqual(result, self.trivia_list)

    def test_parse_trivia_response_failure(self):
        with self.assertRaises(Bs4ParsingError):
            trivia._parse_trivia_response(Response())

    def test_generate_trivia_message_success(self):
        result = trivia._generate_trivia_message(self.trivia_list, 666)
        true_result = "✨=====冷知识=====✨"
        self.assertIn(true_result, result)

    def test_generate_trivia_message_empty_list(self):
        result = trivia._generate_trivia_message([], 666)
        self.assertEqual(result, "获取冷知识失败")
