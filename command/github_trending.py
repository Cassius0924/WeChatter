import requests
from bs4 import BeautifulSoup

def get_github_trending_str() -> str:
    trending_list = get_github_trending_list()
    if not trending_list:
        return "获取GitHub趋势失败"

    trending_str = "✨=====GitHub Trending=====✨\n"
    for i, trending in enumerate(trending_list[:10]):  # 只获取前10个趋势
        trending_str += f"{i + 1}. {trending['author']} / {trending['repo']} {trending['svg']}\n"
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
                repo = title['href'].split('/')
                if len(repo) >= 3:
                    svg = article.select_one('svg') # 提取SVG内容
                    if svg:
                        svg_content = svg.prettify() # 获取SVG的完整内容
                        trending_list.append({
                            'author': repo[1].strip(),
                            'repo': repo[2].strip(),
                            'svg': svg_content
                        })

        return trending_list[:20]

    print("获取GitHub趋势失败")
    return []

# 调用函数并打印结果
print(get_github_trending_str())
