import unittest
import json
from wechatter.commands._commands import weibo_hot

class TestWeiboHotCommand(unittest.TestCase):
    def test_extract_weibo_hot_data_success(self):
        with open('tests/commands/test_weibo_hot/weibo_hot_response.json') as f:
            r_json = json.load(f)
        result = weibo_hot.extract_weibo_hot_data(r_json)
        self.assertIsInstance(result, list)

    def test_extract_weibo_hot_data_failure(self):
        with self.assertRaises(Exception):
            weibo_hot.extract_weibo_hot_data({})

    def test_generate_weibo_hot_message_success(self):
        with open('tests/commands/test_weibo_hot/weibo_hot_response.json') as f:
            hot_list = json.load(f)['data']['cards'][0]['card_group'][:20]
        result = weibo_hot.generate_weibo_hot_message(hot_list)
        self.assertIn('✨=====微博热搜=====✨', result)

    def test_generate_weibo_hot_message_empty_list(self):
        result = weibo_hot.generate_weibo_hot_message([])
        self.assertEqual(result, '微博热搜列表为空')