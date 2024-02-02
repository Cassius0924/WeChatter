import unittest
from wechatter.commands._commands import people_daily


class TestPeopleDailyCommand(unittest.TestCase):
    def test_get_people_daily_url_success(self):
        result = people_daily.get_people_daily_url("2024010901")
        self.assertEqual(result, "http://paper.people.com.cn/rmrb/images/2024-01/09/01/rmrb2024010901.pdf")

    def test_get_people_daily_value_error(self):
        with self.assertRaises(ValueError):
            people_daily.get_people_daily_url("20240109011")
        with self.assertRaises(ValueError):
            people_daily.get_people_daily_url("20240109")
