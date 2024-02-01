import unittest
import json
from wechatter.commands._commands import douyin_hot

class TestDouyinHotCommand(unittest.TestCase):
    def test_extract_douyin_hot_data_success(self):
        with open('tests/commands/test_douyin_hot/douyin_hot_response.json') as f:
            r_json = json.load(f)
        result = douyin_hot.extract_douyin_hot_data(r_json)
        self.assertIsInstance(result, list)

    def test_extract_douyin_hot_data_failure(self):
        with self.assertRaises(Exception):
            douyin_hot.extract_douyin_hot_data({})

    def test_generate_douyin_hot_message_success(self):
        with open('tests/commands/test_douyin_hot/douyin_hot_response.json') as f:
            hot_list = json.load(f)['word_list']
        result = douyin_hot.generate_douyin_hot_message(hot_list)
        self.assertIn('✨=====抖音热搜=====✨', result)

    def test_generate_douyin_hot_message_empty_list(self):
        result = douyin_hot.generate_douyin_hot_message([])
        self.assertEqual(result, '暂无抖音热搜')