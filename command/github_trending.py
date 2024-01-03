import requests
from bs4 import BeautifulSoup


def get_github_trending_str() -> str:
    trending_list = get_github_trending_list()
    if not trending_list:
        return "获取GitHub趋势失败"

    trending_str = "✨=====GitHub Trending=====✨\n"
    for i, trending in enumerate(trending_list[:10]):  # 只获取前10个趋势
        trending_str += (
            f"{i + 1}. {trending['author']} / {trending['repo']}\n  ⭐ {trending['star_total']}total(⭐{trending['star_today']})\n  🔤{trending['programmingLanguage']}\n  📖{trending['comment']}\n"
        )
    return trending_str


def get_github_trending_list() -> list:
    url = "https://github.com/trending"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        trending_list = []
        articles = soup.select("article")
        for article in articles:

            title = article.select_one("h2 a")
            if title:
                repo = title["href"].split("/")
                if len(repo) >= 3:
                    trending_list.append(
                        {
                            "author": repo[1].strip(),
                            "repo": repo[2].strip(),
                        }
                    )

            comment = article.select_one("p")
            if comment:
                trending_list.append(
                    {
                        "comment": comment.text.strip(),
                    }
                )

            programmingLanguage = article.select_one("span[itemprop='programmingLanguage']")
            if programmingLanguage:
                trending_list.append(
                    {
                        "programmingLanguage": programmingLanguage.text.strip(),
                    }
                )

            star_total = article.select_one("div[1] a[0]")
            if star_total:
                trending_list.append(
                    {
                        "star_total": star_total.text.strip(),
                    }
                )

            star_today = article.select_one("div[1] span[2]")
            if star_today:
                trending_list.append(
                    {
                        "star_today": star_today.text.strip(),
                    }
                )


        return trending_list[:20]

    print("获取GitHub趋势失败")
    return []
