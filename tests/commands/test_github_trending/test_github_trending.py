import json
import unittest

from requests import Response

from wechatter.commands._commands import github_trending as gt
from wechatter.exceptions import Bs4ParsingError


class TestGithubTrendingCommand(unittest.TestCase):
    def setUp(self):
        with open(
            "tests/commands/test_github_trending/github_trending_response.html.test"
        ) as f:
            r_html = f.read()
        self.response = Response()
        self.response._content = r_html.encode("utf-8")
        with open("tests/commands/test_github_trending/github_trending_data.json") as f:
            self.gt_list = json.load(f)

    def test_parse_github_trending_response_success(self):
        result = gt._parse_github_trending_response(self.response)
        self.assertListEqual(result, self.gt_list)

    def test_parse_github_trending_response_failure(self):
        with self.assertRaises(Bs4ParsingError):
            gt._parse_github_trending_response(Response())

    def test_generate_github_trending_message_success(self):
        result = gt._generate_github_trending_message(self.gt_list)
        true_result = "✨=====GitHub Trending=====✨\n1.📦 danielmiessler / fabric\n   ⭐ 2,538 total (⭐1,139 today)\n   🔤 Python\n   📖 fabric is an open-source framework for augmenting humans using AI.\n2.📦 InkboxSoftware / excelCPU\n   ⭐ 2,507 total (⭐337 today)\n   🔤 Python\n   📖 16-bit CPU for Excel, and related files\n3.📦 f / awesome-chatgpt-prompts\n   ⭐ 98,933 total (⭐115 today)\n   🔤 HTML\n   📖 This repo includes ChatGPT prompt curation to use ChatGPT better.\n4.📦 all-in-aigc / aicover\n   ⭐ 973 total (⭐205 today)\n   🔤 TypeScript\n   📖 ai cover generator\n5.📦 facebookresearch / codellama\n   ⭐ 12,972 total (⭐197 today)\n   🔤 Python\n   📖 Inference code for CodeLlama models\n6.📦 webprodigies / plura-production\n   ⭐ 315 total (⭐43 today)\n   🔤 TypeScript\n   📖 No description.\n7.📦 ExOK / Celeste64\n   ⭐ 895 total (⭐170 today)\n   🔤 C#\n   📖 A game made by the Celeste developers in a week(ish, closer to 2)\n8.📦 haotian-liu / LLaVA\n   ⭐ 13,169 total (⭐155 today)\n   🔤 Python\n   📖 [NeurIPS'23 Oral] Visual Instruction Tuning (LLaVA) built towards GPT-4V level capabilities and beyond.\n9.📦 mlflow / mlflow\n   ⭐ 16,583 total (⭐127 today)\n   🔤 Python\n   📖 Open source platform for the machine learning lifecycle\n10.📦 PKU-YuanGroup / MoE-LLaVA\n   ⭐ 689 total (⭐219 today)\n   🔤 Python\n   📖 Mixture-of-Experts for Large Vision-Language Models\n"
        self.assertEqual(result, true_result)

    def test_generate_zhihu_hot_message_empty_list(self):
        result = gt._generate_github_trending_message([])
        self.assertEqual(result, "暂无 GitHub 趋势")

    def test_generate_github_trending_quoted_response_success(self):
        result = gt._generate_github_trending_quoted_response(self.gt_list)
        true_result = '{"1": "https://github.com/danielmiessler/fabric", "2": "https://github.com/InkboxSoftware/excelCPU", "3": "https://github.com/f/awesome-chatgpt-prompts", "4": "https://github.com/all-in-aigc/aicover", "5": "https://github.com/facebookresearch/codellama", "6": "https://github.com/webprodigies/plura-production", "7": "https://github.com/ExOK/Celeste64", "8": "https://github.com/haotian-liu/LLaVA", "9": "https://github.com/mlflow/mlflow", "10": "https://github.com/PKU-YuanGroup/MoE-LLaVA"}'
        self.assertEqual(result, true_result)
