import json
import unittest

from requests import Response

from wechatter.commands._commands import weather
from wechatter.exceptions import Bs4ParsingError


class TestWeatherCommand(unittest.TestCase):
    def setUp(self):
        with open("tests/commands/test_weather/c_data.json") as f:
            self.c_data = json.load(f)
        with open("tests/commands/test_weather/c_weather.js") as f:
            self.c_weather = f.read()
        with open("tests/commands/test_weather/hourly_data.json") as f:
            self.hourly_data = json.load(f)
        with open("tests/commands/test_weather/hourly_weather.html.test") as f:
            self.hourly_weather_html = f.read()
        self.hourly_response = Response()
        self.hourly_response._content = self.hourly_weather_html.encode("utf-8")

    def test_get_city_id_success(self):
        result = weather._get_city_id("上海")
        self.assertEqual(result, "101020100")
        result = weather._get_city_id("天河")
        self.assertEqual(result, "101280109")

    def test_get_city_id_key_error(self):
        with self.assertRaises(KeyError):
            weather._get_city_id("加利福尼亚")

    def test_parse_hourly_weather_response_success(self):
        result = weather._parse_hourly_weather_response(self.hourly_response)
        self.assertDictEqual(result, self.hourly_data)

    def test_parse_hourly_weather_response_bs4_parsing_error(self):
        response = Response()
        response._content = (
            "<html><body><div class='todayRight'></div></body></html>".encode("utf-8")
        )
        with self.assertRaises(Bs4ParsingError):
            weather._parse_hourly_weather_response(response)

    def test_parse_hourly_weather_response_index_error(self):
        response = Response()
        response._content = self.hourly_response.text.replace(
            "var hour3data=", "var hour"
        ).encode("utf-8")
        with self.assertRaises(IndexError):
            weather._parse_hourly_weather_response(response)

    def test_parse_hourly_weather_response_json_decode_error(self):
        response = Response()
        response._content = self.hourly_response.text.replace(
            "var hour3data=[", "var hour3data="
        ).encode("utf-8")
        with self.assertRaises(json.JSONDecodeError):
            weather._parse_hourly_weather_response(response)

    def test_parse_c_weather_success(self):
        result = weather._parse_c_weather(self.c_weather)
        self.assertDictEqual(result, self.c_data)

    def test_parse_c_weather_json_decode_error(self):
        with self.assertRaises(json.JSONDecodeError):
            weather._parse_c_weather("var dataSK={")

    def test_parse_c_weather_index_error(self):
        with self.assertRaises(IndexError):
            weather._parse_c_weather("var dataSK")

    def test_generate_weather_message_success(self):
        future_weather_list = weather._get_future_weather(
            self.hourly_data["weather"], "2024020216", 5
        )
        result = weather._generate_weather_message(
            self.c_data, self.hourly_data, future_weather_list
        )
        print(result)
        true_result1 = "🏙️ 广州 📅 02月02日 星期五\n🌡️ 温度: 19°C ~ 26°C\n🌤️ 天气: 多云（🕓当前26.4°C）\n📈 逐时: 阴25° 阴24° 阴23° 阴21° 阴20° \n☀️ 明日日出: 07:06 今日日落: 18:14\n💨 1级 😷较差 💧60% 🌞最弱\n"
        true_result2 = "🏙️ 广州 📅 02月02日 星期五\n🌡️ 温度: 19°C ~ 26°C\n🌤️ 天气: 多云（🕓当前26.4°C）\n📈 逐时: 阴25° 阴24° 阴23° 阴21° 阴20° \n☀️ 明日日出: 07:06 明日日落: 18:15\n💨 1级 😷较差 💧60% 🌞最弱\n"
        self.assertEqual(result, true_result1)
        self.assertEqual(result, true_result2)

    def test_get_future_weather_success(self):
        result = weather._get_future_weather(
            self.hourly_data["weather"], "2024020212", 5
        )
        true_result = [ { "ja": "02", "jb": "25", "jc": "0", "jd": "4", "je": "77", "jf": "2024020213", }, { "ja": "02", "jb": "25", "jc": "0", "jd": "4", "je": "76", "jf": "2024020214", }, { "ja": "02", "jb": "25", "jc": "0", "jd": "4", "je": "76", "jf": "2024020215", }, { "ja": "02", "jb": "25", "jc": "0", "jd": "4", "je": "76", "jf": "2024020216", }, { "ja": "02", "jb": "25", "jc": "0", "jd": "4", "je": "76", "jf": "2024020217", }, ]  # fmt: skip
        self.assertListEqual(result, true_result)
        result = weather._get_future_weather(
            self.hourly_data["weather"], "2024020212", 1
        )
        true_result = [ { "ja": "02", "jb": "25", "jc": "0", "jd": "4", "je": "77", "jf": "2024020213", } ]  # fmt: skip
        self.assertListEqual(result, true_result)

    def test_get_future_weather_empty_list(self):
        result = weather._get_future_weather([], "2024020223", 5)
        self.assertListEqual(result, [])
