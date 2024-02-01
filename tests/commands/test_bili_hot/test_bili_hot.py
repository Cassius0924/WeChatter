import unittest
import json
from wechatter.commands._commands import bili_hot

class TestBiliHotCommand(unittest.TestCase):
    def test_extract_bili_hot_data_success(self):
        with open('tests/commands/test_bili_hot/bili_hot_response.json') as f:
            r_json = json.load(f)
        result = bili_hot.extract_bili_hot_data(r_json)
        self.assertIsInstance(result, list)

    def test_extract_bili_hot_data_failure(self):
        with self.assertRaises(Exception):
            bili_hot.extract_bili_hot_data({})

    def test_generate_bili_hot_message_success(self):
        with open('tests/commands/test_bili_hot/bili_hot_response.json') as f:
            hot_list = json.load(f)['data']['list']
        result = bili_hot.generate_bili_hot_message(hot_list)
        self.assertIn('✨=====Bilibili热搜=====✨', result)

    def test_generate_bili_hot_message_empty_list(self):
        result = bili_hot.generate_bili_hot_message([])
        self.assertEqual(result, '暂无Bilibili热搜')