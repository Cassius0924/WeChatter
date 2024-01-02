import requests

def get_weibo_hot_str() -> str:
    hot_search_list = get_weibo_hot_list()
    if len(hot_search_list) == 0:
        return "获取微博热搜失败"
    hot_search_str = "✨=====微博热搜=====✨\n"
    # for i, hot_search in enumerate(hot_search_list["data"]["cards"][0]["card_group"][:20]):
    #     hot_search_str += f"{i + 1}. {hot_search['desc']}\n"
    for i, hot_search in enumerate(hot_search_list["data"]["realtime"][:20]):
        hot_search_str += f"{i + 1}. {hot_search['word_scheme']}\n"
    return hot_search_str

def get_weibo_hot_list() -> list:
    # url = "https://m.weibo.cn/api/container/getIndex?containerid=106003%26filter_type%3Drealtimehot"
    url = "https://weibo.com/ajax/side/hotSearch"
    response = requests.get(url)

    if response.status_code == 200:
        hot_search_list = response.json()
        return hot_search_list
    print("获取微博热搜失败")
    return []
