import unittest
from wechatter.commands._commands import translate
import requests


class TestTranslateCommand(unittest.TestCase):

    def setUp(self):
        with open('tests/commands/test_translate/reverso_context_response.html') as f:
            self.r_html = f.read()
        self.transliteration_json = {"text": "你好", "transliteration": "nǐ hǎo"}

    def test_detect_lang(self):
        content = "hello"
        result = translate._detect_lang(content)
        self.assertEqual(result, "english")
        content = "你好"
        result = translate._detect_lang(content)
        self.assertEqual(result, "chinese")
        content = "こんにちは"
        result = translate._detect_lang(content)
        self.assertEqual(result, "japanese")
        content = "Привет"
        result = translate._detect_lang(content)
        self.assertEqual(result, "russian")

    def test_check_lang_support(self):
        from_lang = "english"
        to_lang = "chinese"
        result = translate._check_lang_support(from_lang, to_lang)
        self.assertTrue(result)
        from_lang = "english"
        to_lang = "russian"
        result = translate._check_lang_support(from_lang, to_lang)
        self.assertTrue(result)
        from_lang = "chinese"
        to_lang = "russian"
        result = translate._check_lang_support(from_lang, to_lang)
        self.assertFalse(result)

    def test_check_model_by_lang(self):
        lang = "chinese"
        result = translate._check_model_by_lang(lang)
        self.assertTrue(result)
        lang = "russian"
        result = translate._check_model_by_lang(lang)
        self.assertTrue(result)
        lang = "english"
        result = translate._check_model_by_lang(lang)
        self.assertFalse(result)

    def test_auto_translate(self):
        from_lang = "chinese"
        to_lang = "english"
        result = translate._auto_translate(from_lang, to_lang)
        self.assertEqual(result, ("chinese", "english"))
        from_lang = "english"
        to_lang = "chinese"
        result = translate._auto_translate(from_lang, to_lang)
        self.assertEqual(result, ("english", "chinese"))
        from_lang = "russian"
        to_lang = "chinese"
        result = translate._auto_translate(from_lang, to_lang)
        self.assertEqual(result, ("russian", "english"))
        from_lang = "japanese"
        to_lang = "chinese"
        result = translate._auto_translate(from_lang, to_lang)
        self.assertEqual(result, ("japanese", "english"))
        from_lang = "chinese"
        to_lang = "russian"
        result = translate._auto_translate(from_lang, to_lang)
        self.assertEqual(result, ("chinese", "english"))

    def test_parse_reverso_context_response_success(self):
        response = requests.Response()
        response._content = self.r_html.encode()
        result = translate._parse_reverso_context_response(response)
        true_result = ['你好', '您好', '喂', '嗨', '哈罗', '哈啰', '好', '你们好', '嘿', '打个招呼', '哈喽', '有人',
                       '有人吗', '晚上好', 'Hello']
        self.assertListEqual(result, true_result)

    def test_parse_reverso_context_response_value_error(self):
        response = requests.Response()
        response._content = b"error"
        with self.assertRaises(ValueError):
            translate._parse_reverso_context_response(response)

    def test_extract_transliteration_data_success(self):
        result = translate._extract_transliteration_data(self.transliteration_json)
        self.assertEqual(result, "nǐ hǎo")

    def test_extract_transliteration_data_runtime_error(self):
        with self.assertRaises(RuntimeError):
            translate._extract_transliteration_data({})
        with self.assertRaises(RuntimeError):
            translate._extract_transliteration_data("text")

    def test_generate_translate_message(self):
        word_list = ["你好", "您好"]
        result = translate._generate_translate_message(content="hello", from_lang="english", to_lang="chinese",
                                                       word_list=word_list, transliteration="nǐ hǎo", )
        true_result = "(🇺🇸->🇨🇳) \"hello\" 翻译:\n(🔈 注音) <nǐ hǎo>\n你好\n您好\n"
        self.assertEqual(result, true_result)
