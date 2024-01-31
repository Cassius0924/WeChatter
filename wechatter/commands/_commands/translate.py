# 翻译命令
import json
from typing import Dict, List

import langid
import requests
from bs4 import BeautifulSoup, Tag

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender


@command(
    command="word",
    keys=["word", "单词"],
    desc="翻译单词或短语。",
    value=120,
)
def word_command_handler(to: SendTo, message: str = "") -> None:
    to_lang = "chinese"
    # 检测文本语言
    from_lang = detect_lang(message)

    # 自动翻译 en -> zh, zh -> en, other -> zh --if not--> en
    if from_lang == "":
        error_message = "无法识别语言"
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))
        return
    if from_lang == "chinese":
        to_lang = "english"
    elif from_lang != "english" and not check_lang_support(from_lang, "chinese"):
        to_lang = "english"

    # 获取翻译
    try:
        response = get_reverso_context_tran_str(message, from_lang, to_lang)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))
    except Exception as e:
        error_message = f"翻译失败，错误信息：{e}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


# 翻译语言字典（何种语言对应何种语言）
TRAN_LANG_DICT = {
    "chinese": ["english", "spanish", "french"],
    "english": [
        "chinese",
        "spanish",
        "french",
        "japanese",
        "italian",
        "russian",
        "german",
    ],
    "spanish": [
        "chinese",
        "english",
        "french",
        "japanese",
        "italian",
        "russian",
        "german",
    ],
    "french": [
        "chinese",
        "english",
        "spanish",
        "japanese",
        "italian",
        "russian",
        "german",
    ],
    "japanese": ["english", "spanish", "french", "russian", "german"],
    "russian": ["english", "spanish", "french", "japanese", "italian", "german"],
}

LANGID_DICT = {
    "zh": "chinese",
    "en": "english",
    "ru": "russian",
    "ja": "japanese",
    "fr": "french",
    "es": "spanish",
    "it": "italian",
    "de": "german",
}

LANG_EMOJI_DICT = {
    "chinese": "🇨🇳",
    "english": "🇺🇸",
    "russian": "🇷🇺",
    "japanese": "🇯🇵",
    "french": "🇫🇷",
    "spanish": "🇪🇸",
    "italian": "🇮🇹",
    "german": "🇩🇪",
}

MODEL_DICT = {
    "chinese": "zh-pinyin",
    "russian": "ru-wikipedia",
    "japanese": "ja-latin",
    "arabic": "ar-wikipedia",
    "ukrainian": "uk-slovnyk",
    "korean": "ko-romanization",
}


# 获取翻译字符串
def get_reverso_context_tran_str(content: str, from_lang: str, to_lang: str) -> str:
    try:
        response = get_reverso_context_response(content, from_lang, to_lang)
        result = parse_reverso_context_response(response)
    except Exception as e:
        raise Exception(e)

    try:
        # 加上默认值，注音非必要
        transliteration = get_transliteration_response_json(content, from_lang).get(
            "transliteration", ""
        )
    except Exception as e:
        raise Exception(e)

    tran_direction_msg = (
        LANG_EMOJI_DICT.get(from_lang, "") + "->" + LANG_EMOJI_DICT.get(to_lang, "")
    )
    msg = f'({tran_direction_msg}) "{content}" 翻译:\n'
    if transliteration != "":
        transliteration_msg = f"(🔈 注音) <{transliteration}>\n"
        msg += transliteration_msg
    for res in result[:10]:
        msg += res + "\n"
    return msg


# 使用Reverso Context翻译（主要用于翻译单词或短语）
# API: https://context.reverso.net/translation/
# 示例：https://context.reverso.net/translation/english-chinese/Hello
# Curl: curl https://context.reverso.net/translation/chinese-english/你好 -H "User-Agent: Mozilla/5.0" -H "Content-Type: application/json; charset=UTF-8"
def get_reverso_context_response(
    content: str, from_lang: str, to_lang: str
) -> requests.Response:
    if not check_lang_support(from_lang, to_lang):
        raise Exception(f"不支持的语言翻译：{from_lang} -> {to_lang}")

    try:
        url = f"https://context.reverso.net/translation/{from_lang}-{to_lang}/{content}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json; charset=UTF-8",
        }
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        raise Exception(f"请求Reverso Context API失败，错误信息：{e}")

    if response.status_code != 200:
        raise Exception(f"Reverso Context API返回非200状态码：{response.status_code}")

    return response


def parse_reverso_context_response(response: requests.Response) -> List:
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    translations_content_div = soup.find(id="translations-content")
    result = []
    if translations_content_div and isinstance(translations_content_div, Tag):
        result = [
            i.string
            for i in translations_content_div.find_all("span", class_="display-term")
        ]
    else:
        raise Exception("单词或短语翻译失败，请输入正确的单词或短语（不支持句子翻译）")

    if len(result) == 0:
        result = ["无翻译结果"]
    return result


# 获取音译注音
# API: https://lang-utils-api.reverso.net/transliteration
# 示例: https://lang-utils-api.reverso.net/transliteration/?text=你好&model=zh-pinyin
def get_transliteration_response_json(content: str, lang: str) -> Dict:
    if not check_model_by_lang(lang):
        return ""
    model = MODEL_DICT.get(lang, "")
    try:
        url = f"https://lang-utils-api.reverso.net/transliteration/?text={content}&model={model}"
        headers = {"User-Agent": "Mozilla/5.0", "Accpet": "application/json"}
        response = requests.get(url, headers=headers)
    except Exception as e:
        raise Exception(f"请求音译注音API失败，错误信息：{e}")

    if response.status_code != 200:
        raise Exception(f"音译注音API返回非200状态码：{response.status_code}")

    try:
        return json.loads(response.text)
    except Exception as e:
        raise Exception(f"解析音译注音API失败，错误信息：{e}")


# 检查音译注音模型是否支持
def check_model_by_lang(lang: str) -> bool:
    if lang in MODEL_DICT.keys():
        return True
    return False


# 检查语言是否支持
def check_lang_support(from_lang: str, to_lang: str) -> bool:
    if from_lang in TRAN_LANG_DICT.keys():
        if to_lang in TRAN_LANG_DICT[from_lang]:
            return True
    return False


# 检测文本语言
def detect_lang(content: str) -> str:
    lang, _ = langid.classify(content)
    return LANGID_DICT.get(lang, "")
