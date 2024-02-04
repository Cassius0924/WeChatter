import unittest

from requests import Response

from wechatter.commands._commands import gasoline_price
from wechatter.exceptions import Bs4ParsingError


class TestGasolinePriceCommand(unittest.TestCase):

    def setUp(self):
        with open("tests/commands/test_gasoline_price/gasoline_price_response_html.test") as f:
            r_html = f.read()
        self.response = Response()
        self.response._content = r_html.encode('utf-8')
        with open("tests/commands/test_gasoline_price/gasoline_price_data") as f:
            self.gasoline_price = f.read()

    def test_get_gasoline_price_str_success(self):
        result = gasoline_price.get_gasoline_price_str('广州')
        self.assertIn('✨广州石化92汽油指导价✨', result)

    def test_get_gasoline_price_str_failure(self):
        with self.assertRaises(KeyError):
            gasoline_price.get_gasoline_price_str('广州市')

    def test_parse_gasoline_price_response_success(self):
        result = gasoline_price._parse_gasoline_price_response(self.response)
        self.assertIn('广州中国石化92号汽油最新指导价格为', result)

    def test_parse_gasoline_price_response_failure(self):
        with self.assertRaises(Bs4ParsingError):
            gasoline_price._parse_gasoline_price_response(Response())

    def test_get_city_id_success(self):
        result = gasoline_price._get_city_id('广州')
        self.assertEqual(result, '440100')

    def test_get_city_id_failure(self):
        with self.assertRaises(KeyError):
            gasoline_price._get_city_id('广州市')

    def test_generate_gasoline_price_message_success(self):
        result = gasoline_price._generate_gasoline_price_message(self.gasoline_price, '广州')
        self.assertIn('✨广州石化92汽油指导价✨', result)
