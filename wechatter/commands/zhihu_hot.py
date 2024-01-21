# 知乎热搜命令
from typing import List

import requests


def get_zhihu_hot_str() -> str:
    hot_list = get_zhihu_hot_list()
    if len(hot_list) == 0:
        return "获取知乎热搜失败"
    hot_search_str = "✨=====知乎热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_search_str += f"{i + 1}. {hot_search.get('target', {}).get('title', '')}\n"
    return hot_search_str


def get_zhihu_hot_list() -> List:
    response: requests.Response
    try:
        # url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
        url = "https://api.zhihu.com/topstory/hot-list?limit=10"
        response = requests.get(url, timeout=10)
    except Exception:
        print("请求知乎热搜失败")
        return []

    if response.status_code != 200:
        print("获取知乎热搜失败")
        return []
    hot_dict = response.json()
    return hot_dict.get("data", [])
