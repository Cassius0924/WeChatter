import requests
from bs4 import BeautifulSoup


def get_pai_post_str() -> str:
    pai_post_list = get_pai_post_list()
    if pai_post_list == []:
        return "获取少数派早报失败"

    pai_post_str = "✨=====派早报=====✨\n"
    for i, pai_post in enumerate(pai_post_list):
        pai_post_str += f"{i + 1}. {pai_post.get('title')}\n"
    return pai_post_str


def get_pai_post_list() -> list:
    response: requests.Response
    try:
        url = "https://sspai.com/"
        response = requests.get(url, timeout=10)
    except Exception:
        print("请求少数派早报失败")
        return []

    if response.status_code != 200:
        print("获取少数派早报失败")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    pai_post_list = []
    articles = soup.select("div.pai_abstract")
    for article in articles:
        pai_post_item = {}

        title = article.select_one("a div")
        if title:
            pai_post_item["title"] = title.text.strip()
        else:
            pai_post_item["title"] = "No description."

        if pai_post_item:
            pai_post_list.append(pai_post_item)

    return pai_post_list
