import json
import unittest

from requests import Response

from wechatter.commands._commands import pai_post
from wechatter.exceptions import Bs4ParsingError


class TestPaiPostCommand(unittest.TestCase):
    def setUp(self):
        with open("tests/commands/test_pai_post/pai_post_response.html.test") as f:
            r_html = f.read()
        self.response = Response()
        self.response._content = r_html.encode("utf-8")
        with open("tests/commands/test_pai_post/pai_post_data.json") as f:
            self.pai_post_list = json.load(f)

    def test_parse_pai_post_response_success(self):
        result = pai_post._parse_pai_post_response(self.response)
        self.assertListEqual(result, self.pai_post_list)

    def test_parse_pai_post_response_failure(self):
        with self.assertRaises(Bs4ParsingError):
            pai_post._parse_pai_post_response(Response())

    def test_generate_pai_post_message_success(self):
        result = pai_post._generate_pai_post_message(self.pai_post_list)
        true_result = "1. HMD Global 社交账户改名\n2. 第三方社区「Linux 中国」停止运营\n3. 微软为 Apple Vision Pro 推出 Microsoft 365 套件\n4. Hulu 开始打击账户密码共享\n5. Apple Vision Pro 新闻 N 则\n6. Apple 延长与高通的基带合作协议\n7. Adobe 将停止更新 Adobe XD\n8. 环球音乐集团计划将从 TikTok 收回歌曲版权\n9. 全球 2023 第四季度智能手机出货量有所回升\n10. ICANN 将正式推出内网域名 .internal\n11. 索尼召开 State of Play 新作发布会"
        self.assertIn(true_result, result)

    def test_generate_zhihu_hot_message_empty_list(self):
        result = pai_post._generate_pai_post_message([])
        self.assertEqual(result, "暂无少数派早报")

    def test_generate_pai_post_quoted_response_success(self):
        result = pai_post._generate_pai_post_quoted_response(self.pai_post_list)
        true_result = '{"1": "https://sspai.com/post/86250", "2": "https://sspai.com/post/86250", "3": "https://sspai.com/post/86250", "4": "https://sspai.com/post/86250", "5": "https://sspai.com/post/86250", "6": "https://sspai.com/post/86222", "7": "https://sspai.com/post/86222", "8": "https://sspai.com/post/86222", "9": "https://sspai.com/post/86222", "10": "https://sspai.com/post/86222", "11": "https://sspai.com/post/86222"}'
        self.assertEqual(result, true_result)
