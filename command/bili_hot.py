import requests

def get_bili_hot_str() -> str:
    hot_search_list = get_bili_hot_list()
    if len(hot_search_list) == 0:
        return "获取b站热搜失败"
    hot_search_str = "✨=====b站热搜=====✨\n"
    for i, hot_search in enumerate(hot_search_list["data"]["list"]):
        hot_search_str += f"{i + 1}. {hot_search['keyword']}\n"
    return hot_search_str


def get_bili_hot_list() -> list:
    url = "https://app.bilibili.com/x/v2/search/trending/ranking"
    response = requests.get(url)

    if response.status_code == 200:
        hot_search_list = response.json()
        return hot_search_list
    print("获取b站热搜失败")
    return []

