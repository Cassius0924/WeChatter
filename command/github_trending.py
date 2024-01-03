import requests
from bs4 import BeautifulSoup

def get_github_trending_str() -> str:
    trending_list = get_github_trending_list()
    if len(trending_list) == 0:
        return "获取GitHub趋势失败"
    trending_str = "✨=====GitHub Trending=====✨\n"
    for i, trending in enumerate(trending_list[:10]):  # 只获取前10个趋势
        trending_str += f"{i + 1}. {trending}\n"
    return trending_str

def get_github_trending_list() -> list:
    url = "https://github.com/trending"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        trending_list = []
        articles = soup.select('article')
        for article in articles:
            title = article.select_one('h2 a')
            if title:
                trending_list.append(title.text.strip())# 去除首尾空格

        return trending_list[:10]

    print("获取GitHub趋势失败")
    return []
