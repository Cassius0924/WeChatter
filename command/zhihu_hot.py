# 知乎热搜命令
import requests


def get_zhihu_hot_str() -> str:
    hot_search_list = get_zhihu_hot_list()
    if len(hot_search_list) == 0:
        return "获取知乎热搜失败"
    hot_search_str = "✨=====知乎热搜=====✨\n"
    for i, hot_search in enumerate(hot_search_list["data"][:20]):
        hot_search_str += f"{i + 1}. {hot_search['target']['title']}\n"
    return hot_search_str


def get_zhihu_hot_list() -> list:
    # url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
    url = "https://api.zhihu.com/topstory/hot-list?limit=10&reverse_order=0"
    response = requests.get(url)

    if response.status_code == 200:
        hot_search_list = response.json()
        return hot_search_list
    print("获取知乎热搜失败")
    return []
