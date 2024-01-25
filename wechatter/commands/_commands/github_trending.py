from typing import List

import requests
from bs4 import BeautifulSoup

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender


@command(
    command="github-trending",
    keys=["GitHub趋势", "github-trending"],
    desc="获取GitHub趋势。",
    value=60,
)
def github_trending_command_handler(to: SendTo, message: str = "") -> None:
    response = get_github_trending_str()
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))


def get_github_trending_str() -> str:
    trending_list = get_github_trending_list()
    if trending_list == []:
        return "获取GitHub趋势失败"

    trending_str = "✨=====GitHub Trending=====✨\n"
    for i, trending in enumerate(trending_list[:10]):  # 只获取前10个趋势
        trending_str += f"{i + 1}. 🏎️  {trending['author']} / {trending['repo']}\n    ⭐  {trending['star_total']} total (⭐{trending['star_today']})\n    🔤  {trending['programmingLanguage']}\n    📖  {trending['comment']}\n"
    return trending_str


def get_github_trending_list() -> List:
    response: requests.Response
    try:
        url = "https://github.com/trending"
        response = requests.get(url, timeout=10)
    except Exception:
        print("请求GitHub趋势失败")
        return []

    if response.status_code != 200:
        print("获取GitHub趋势失败")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    trending_list = []
    articles = soup.select("article")
    for article in articles:
        trending_item = {}

        title = article.select_one("h2 a")
        if title:
            t = title["href"]
            if not isinstance(t, str):
                continue
            repo = t.split("/")
            if len(repo) >= 3:
                trending_item["author"] = repo[1].strip()
                trending_item["repo"] = repo[2].strip()
            else:
                continue

        desc = article.select_one("p")
        if desc:
            trending_item["comment"] = desc.text.strip()
        else:
            trending_item["comment"] = "No description."

        lang = article.select_one("span[itemprop='programmingLanguage']")
        if lang:
            trending_item["programmingLanguage"] = lang.text.strip()
        else:
            trending_item["programmingLanguage"] = ""

        star_total = article.select_one("a.Link--muted")
        if star_total:
            trending_item["star_total"] = star_total.get_text(strip=True)
        else:
            trending_item["star_total"] = ""

        star_today = article.select_one("div:nth-of-type(2) span:nth-of-type(3)")
        if star_today:
            trending_item["star_today"] = star_today.text.strip().replace("stars ", "")
        else:
            trending_item["star_today"] = ""

        if trending_item:
            trending_list.append(trending_item)

    return trending_list
