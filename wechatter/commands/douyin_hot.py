from typing import List
import requests


def get_douyin_hot_str() -> str:
    hot_list = get_douyin_hot_list()
    if hot_list == []:
        return "获取抖音热搜失败"
    hot_str = "✨=====抖音热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_str += f"{i + 1}.  {hot_search.get('word')}\n"
    return hot_str


def get_douyin_hot_list() -> List:
    url = "https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print("获取抖音热搜失败")
        return []
    hot_dict = response.json()
    return hot_dict.get("word_list", [])
