import unittest
import json
from wechatter.commands._commands import zhihu_hot

class TestZhihuHotCommand(unittest.TestCase):
    def test_extract_zhihu_hot_data_success(self):
        with open('tests/commands/test_zhihu_hot/zhihu_hot_response.json') as f:
            r_json = json.load(f)
        result = zhihu_hot.extract_zhihu_hot_data(r_json)
        self.assertIsInstance(result, list)

    def test_extract_zhihu_hot_data_failure(self):
        with self.assertRaises(Exception):
            zhihu_hot.extract_zhihu_hot_data({})

    def test_generate_zhihu_hot_message_success(self):
        with open('tests/commands/test_zhihu_hot/zhihu_hot_response.json') as f:
            hot_list = json.load(f)['data']
        result = zhihu_hot.generate_zhihu_hot_message(hot_list)
        self.assertIn('✨=====知乎热搜=====✨', result)

    def test_generate_zhihu_hot_message_empty_list(self):
        result = zhihu_hot.generate_zhihu_hot_message([])
        self.assertEqual(result, '暂无知乎热搜')