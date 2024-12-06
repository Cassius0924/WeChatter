import json
import unittest

from wechatter.commands._commands import idaily


class TestIdailyCommand(unittest.TestCase):
    def setUp(self):
        with open(
                "tests/commands/test_idaily/idaily_response.json"
        ) as f:
            self.tih_response = json.load(f)
            self.tih_list = self.tih_response

    def test_extract_idaily_data_success(self):
        result = idaily._extract_idaily_data(self.tih_response)
        self.assertListEqual(result, self.tih_list)

    def test_generate_idaily_message_empty_list(self):
        result = idaily._generate_idaily_message([])
        self.assertEqual(result, "暂无每日环球视野")
