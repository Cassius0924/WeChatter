# 翻译命令
from typing import List

import langid
import requests
from bs4 import BeautifulSoup, Tag
from g4f.Provider.Berlin import json

# 翻译语言字典（何种语言对应何种语言）
tran_lang_dict = {
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

langid_dict = {
    "zh": "chinese",
    "en": "english",
    "ru": "russian",
    "ja": "japanese",
    "fr": "french",
    "es": "spanish",
    "it": "italian",
    "de": "german",
}

lang_emoji_dict = {
    "chinese": "🇨🇳",
    "english": "🇺🇸",
    "russian": "🇷🇺",
    "japanese": "🇯🇵",
    "french": "🇫🇷",
    "spanish": "🇪🇸",
    "italian": "🇮🇹",
    "german": "🇩🇪",
}

model_dict = {
    "chinese": "zh-pinyin",
    "russian": "ru-wikipedia",
    "japanese": "ja-latin",
    "arabic": "ar-wikipedia",
    "ukrainian": "uk-slovnyk",
    "korean": "ko-romanization",
}


# 使用Reverso Context翻译（主要用于翻译单词或短语）
# API: https://context.reverso.net/translation/
# 示例：https://context.reverso.net/translation/english-chinese/Hello
# Curl: curl https://context.reverso.net/translation/chinese-english/你好 -H "User-Agent: Mozilla/5.0" -H "Content-Type: application/json; charset=UTF-8"
def tran_by_reverso_context(content: str, from_lang: str, to_lang: str) -> List:
    if not check_lang_support(from_lang, to_lang):
        return ["不支持的语言"]
    url = f"https://context.reverso.net/translation/{from_lang}-{to_lang}/{content}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json; charset=UTF-8",
    }
    response = requests.get(url, headers=headers)
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
        result = ["翻译失败"]
    if len(result) == 0:
        result = ["翻译失败"]
    return result


# 检查语言是否支持
def check_lang_support(from_lang: str, to_lang: str) -> bool:
    if from_lang in tran_lang_dict.keys():
        if to_lang in tran_lang_dict[from_lang]:
            return True
    return False


# 获取翻译字符串
def get_reverso_context_tran_str(content: str, from_lang: str, to_lang: str) -> str:
    result = tran_by_reverso_context(content, from_lang, to_lang)
    tran_direction_msg = (
        lang_emoji_dict.get(from_lang, "") + "->" + lang_emoji_dict.get(to_lang, "")
    )
    transliteration = get_transliteration(content, from_lang)
    msg = f'({tran_direction_msg}) "{content}" 翻译:\n'
    if transliteration != "":
        transliteration_msg = f"(🔈 注音) <{transliteration}>\n"
        msg += transliteration_msg
    for i, res in enumerate(result):
        if i >= 10:
            break
        msg += res + "\n"

    return msg


# 检测文本语言
def detect_lang(content: str) -> str:
    lang, _ = langid.classify(content)
    return langid_dict.get(lang, "")


# 获取音译注音
# API: https://lang-utils-api.reverso.net/transliteration
# 示例: https://lang-utils-api.reverso.net/transliteration/?text=你好&model=zh-pinyin
def get_transliteration(content: str, lang: str) -> str:
    if not check_model_by_lang(lang):
        return ""
    model = model_dict.get(lang, "")
    url = f"https://lang-utils-api.reverso.net/transliteration/?text={content}&model={model}"
    headers = {"User-Agent": "Mozilla/5.0", "Accpet": "application/json"}
    response = requests.get(url, headers=headers)
    result = ""
    try:
        data = json.loads(response.text)
        result = data.get("transliteration", "")
    except Exception as e:
        print(e)
        return ""
    return result


# 检查音译注音模型是否支持
def check_model_by_lang(lang: str) -> bool:
    if lang in model_dict.keys():
        return True
    return False
