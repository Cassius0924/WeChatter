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
    try:
        response = get_github_trending_str()
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))
    except Exception as e:
        error_message = f"获取GitHub趋势失败，错误信息: {str(e)}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_github_trending_str() -> str:
    try:
        response = get_github_trending_response()
        trending_list = parse_github_trending_response(response)
    except Exception as e:
        raise Exception(f"解析GitHub趋势列表失败, 错误信息: {str(e)}")

    if not trending_list:
        raise Exception("GitHub趋势列表为空")

    trending_str = "✨=====GitHub Trending=====✨\n"
    for i, trending in enumerate(trending_list[:10]):  # 只获取前10个趋势
        trending_str += (
            f"{i + 1}. 🏎️  {trending['author']} / {trending['repo']}\n"
            f"⭐  {trending['star_total']} total (⭐{trending['star_today']})\n"
            f"🔤  {trending['programmingLanguage']}\n"
            f"📖  {trending['comment']}\n"
        )

    return trending_str


def parse_github_trending_response(response: requests.Response) -> List:
    trending_list = []
    soup = BeautifulSoup(response.text, "html.parser")
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


def get_github_trending_response() -> requests.Response:
    response: requests.Response
    try:
        url = "https://github.com/trending"
        response = requests.get(url, timeout=10)
    except Exception as e:
        raise Exception(f"请求GitHub趋势失败, 错误信息: {str(e)}")

    if response.status_code != 200:
        raise Exception(f"GitHub趋势返回非200状态码, 状态码: {response.status_code}")

    return response
