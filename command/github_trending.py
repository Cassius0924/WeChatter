import requests
from bs4 import BeautifulSoup

def get_github_trending_str() -> str:
    trending_list = get_github_trending()
    if len(trending_list) == 0:
        return "获取GitHub趋势失败"
    trending_str = "✨=====GitHub Trending=====✨\n"
    for i, trending in enumerate(trending_list[:20]):  # 只获取前20个趋势
        trending_str += f"{i + 1}. {trending}\n"
    return trending_str

def get_github_trending() -> list:
    url = "https://github.com/trending"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        trending_repos = soup.find_all('h1', class_='h3 lh-condensed')

        trending_list = []
        for repo in trending_repos:
            repo_info = repo.find('a')
            repo_name = repo_info.get('href').strip('/')
            trending_list.append(repo_name)

        return trending_list

    print("获取GitHub趋势失败")
    return []
