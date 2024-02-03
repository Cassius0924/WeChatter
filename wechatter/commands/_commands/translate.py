from typing import Dict, List

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
)
def word_command_handler(to: SendTo, message: str = "") -> None:
    from_lang = _detect_lang(message)
    to_lang = "chinese"

    # 自动翻译 en -> zh, zh -> en, other -> zh --if not--> en
    if from_lang == "":
        error_message = "翻译失败，无法检测文本语言"
        logger.error(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))
        return

    from_lang, to_lang = _auto_translate(from_lang, to_lang)

    # 获取翻译
    try:
        result = get_reverso_context_tran_str(message, from_lang, to_lang)
    except Exception as e:
        error_message = f"翻译失败，错误信息: {str(e)}"
        logger.error(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))
    else:
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, result))


# 翻译语言字典（何种语言对应何种语言）
# fmt: off
TRAN_LANG_DICT = {
    "chinese": ["english", "spanish", "french"],
    "english": [
        "chinese", "spanish", "french", "japanese",
        "italian", "russian", "german"
    ],
    "spanish": [
        "chinese", "english", "french", "japanese",
        "italian", "russian", "german",
    ],
    "french": [
        "chinese", "english", "spanish", "japanese",
        "italian", "russian", "german",
    ],
    "japanese": ["english", "spanish", "french", "russian", "german"],
    "russian": ["english", "spanish", "french", "japanese", "italian", "german"],
}

LANGID_DICT = {
    "zh": "chinese", "en": "english", "ru": "russian", "ja": "japanese",
    "fr": "french", "es": "spanish", "it": "italian", "de": "german",
}

LANG_EMOJI_DICT = {
    "chinese": "🇨🇳", "english": "🇺🇸", "russian": "🇷🇺", "japanese": "🇯🇵",
    "french": "🇫🇷", "spanish": "🇪🇸", "italian": "🇮🇹", "german": "🇩🇪",
}

MODEL_DICT = {
    "chinese": "zh-pinyin", "russian": "ru-wikipedia", "japanese": "ja-latin",
    "arabic": "ar-wikipedia", "ukrainian": "uk-slovnyk", "korean": "ko-romanization",
}


# fmt: on


# 获取翻译字符串
def get_reverso_context_tran_str(content: str, from_lang: str, to_lang: str) -> str:
    if not _check_lang_support(from_lang, to_lang):
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
    word_list = _parse_reverso_context_response(response)

    transliteration = ""
    if _check_model_by_lang(from_lang):
        model = MODEL_DICT.get(from_lang, "")

        # 获取音译注音
        # API: https://lang-utils-api.reverso.net/transliteration
        # 示例: https://lang-utils-api.reverso.net/transliteration/?text=你好&model=zh-pinyin
        r_json = get_request_json(
            url=f"https://lang-utils-api.reverso.net/transliteration/?text={content}&model={model}",
            timeout=10,
        )
        transliteration = _extract_transliteration_data(r_json)
    else:
        logger.info(f"不支持的语言音译：{from_lang}")

    message = _generate_translate_message(
        content, from_lang, to_lang, word_list, transliteration
    )
    return message


def _extract_transliteration_data(r_json: Dict) -> str:
    try:
        transliteration = r_json["transliteration"]
    except (KeyError, TypeError) as e:
        logger.error("解析音译注音失败")
        raise RuntimeError("解析音译注音失败") from e
    return transliteration


def _generate_translate_message(
    content: str, from_lang: str, to_lang: str, word_list: List, transliteration: str
) -> str:
    tran_direction_msg = (
        LANG_EMOJI_DICT.get(from_lang, "") + "->" + LANG_EMOJI_DICT.get(to_lang, "")
    )
    msg = f'({tran_direction_msg}) "{content}" 翻译:\n'
    if transliteration != "":
        transliteration_msg = f"(🔈 注音) <{transliteration}>\n"
        msg += transliteration_msg
    for word in word_list[:10]:
        msg += word + "\n"
    return msg


def _auto_translate(from_lang: str, to_lang: str) -> (str, str):
    # 自动翻译 en -> zh, zh -> en, other -> zh --if not--> en
    if from_lang == "chinese":
        to_lang = "english"
    elif from_lang != "english" and not _check_lang_support(from_lang, "chinese"):
        to_lang = "english"
    return from_lang, to_lang


def _parse_reverso_context_response(response: requests.Response) -> List:
    soup = BeautifulSoup(response.text, "html.parser")
    translations_content_div = soup.find(id="translations-content")
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
def _check_model_by_lang(lang: str) -> bool:
    if lang in MODEL_DICT.keys():
        return True
    return False


# 检查语言是否支持
def _check_lang_support(from_lang: str, to_lang: str) -> bool:
    if from_lang in TRAN_LANG_DICT.keys():
        if to_lang in TRAN_LANG_DICT[from_lang]:
            return True
    return False


# 检测文本语言
def _detect_lang(content: str) -> str:
    lang, _ = langid.classify(content)
    return LANGID_DICT.get(lang, "")
