from typing import List

import langid
import requests
from bs4 import BeautifulSoup, Tag
from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender
from wechatter.utils import get_request, get_request_json


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
        error_message = "翻译失败，无法检测文本语言"
        logger.error(error_message)
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
        error_message = f"翻译失败，错误信息: {e}"
        logger.error(error_message)
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
    if not check_lang_support(from_lang, to_lang):
        logger.error(f"不支持的语言翻译：{from_lang} -> {to_lang}")
        raise ValueError(f"不支持的语言翻译：{from_lang} -> {to_lang}")

    # 使用Reverso Context翻译（主要用于翻译单词或短语）
    # API: https://context.reverso.net/translation/
    # 示例：https://context.reverso.net/translation/english-chinese/Hello
    # Curl: curl https://context.reverso.net/translation/chinese-english/你好 -H "User-Agent: Mozilla/5.0" -H "Content-Type: application/json; charset=UTF-8"
    response = get_request(
        url=f"https://context.reverso.net/translation/{from_lang}-{to_lang}/{content}",
        timeout=10,
    )
    result = parse_reverso_context_response(response)

    if not check_model_by_lang(from_lang):
        logger.error(f"不支持的语言音译：{from_lang}")
        raise ValueError(f"不支持的语言音译：{from_lang}")
    model = MODEL_DICT.get(from_lang, "")

    # 获取音译注音
    # API: https://lang-utils-api.reverso.net/transliteration
    # 示例: https://lang-utils-api.reverso.net/transliteration/?text=你好&model=zh-pinyin
    r_json = get_request_json(
        url=f"https://lang-utils-api.reverso.net/transliteration/?text={content}&model={model}",
        timeout=10,
    )
    # 加上默认值，注音非必要
    transliteration = r_json.get("transliteration", "")

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


def parse_reverso_context_response(response: requests.Response) -> List:
    soup = BeautifulSoup(response.text, "html.parser")
    translations_content_div = soup.find(id="translations-content")
    result = []
    if translations_content_div and isinstance(translations_content_div, Tag):
        result = [
            i.string
            for i in translations_content_div.find_all("span", class_="display-term")
        ]
    else:
        logger.error("单词或短语翻译失败，请输入正确的单词或短语（不支持句子翻译）")
        raise ValueError("单词或短语翻译失败，请输入正确的单词或短语（不支持句子翻译）")

    if len(result) == 0:
        result = ["无翻译结果"]
    return result


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
