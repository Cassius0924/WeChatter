from typing import List

import requests
from bs4 import BeautifulSoup
from loguru import logger

from wechatter.commands.handlers import command
from wechatter.exceptions import Bs4ParsingError
from wechatter.models.message import SendTo
from wechatter.sender import sender
from wechatter.utils import get_request


@command(
    command="github-trending",
    keys=["github趋势", "github-trending"],
    desc="获取 GitHub 趋势。",
)
def github_trending_command_handler(to: SendTo, message: str = "") -> None:
    try:
        result = get_github_trending_str()
    except Exception as e:
        error_message = f"获取GitHub趋势失败，错误信息: {str(e)}"
        logger.error(error_message)
        sender.send_msg(to, error_message)
    else:
        sender.send_msg(to, result)


def get_github_trending_str() -> str:
    response = get_request(url="https://github.com/trending", timeout=10)
    gt_list = _parse_github_trending_response(response)
    return _generate_github_trending_message(gt_list)


def _parse_github_trending_response(response: requests.Response) -> List:
    gt_list = []
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("article")
    if not articles:
        logger.error("GitHub 趋势列表为空")
        raise Bs4ParsingError("GitHub 趋势列表为空")
    for article in articles:
        gt_item = {}

        title = article.select_one("h2 a")
        if title:
            t = title["href"]
            if not isinstance(t, str):
                continue
            repo = t.split("/")
            if len(repo) >= 3:
                gt_item["author"] = repo[1].strip()
                gt_item["repo"] = repo[2].strip()
            else:
                continue

        desc = article.select_one("p")
        if desc:
            gt_item["comment"] = desc.text.strip()
        else:
            gt_item["comment"] = "No description."

        lang = article.select_one("span[itemprop='programmingLanguage']")
        if lang:
            gt_item["programmingLanguage"] = lang.text.strip()
        else:
            gt_item["programmingLanguage"] = ""

        star_total = article.select_one("a.Link--muted")
        if star_total:
            gt_item["star_total"] = star_total.get_text(strip=True)
        else:
            gt_item["star_total"] = ""

        star_today = article.select_one("div:nth-of-type(2) span:nth-of-type(3)")
        if star_today:
            gt_item["star_today"] = star_today.text.strip().replace("stars ", "")
        else:
            gt_item["star_today"] = ""

        if gt_item:
            gt_list.append(gt_item)

    if not gt_list:
        logger.error("GitHub 趋势列表返回值格式错误")
        raise Bs4ParsingError("GitHub 趋势列表返回值格式错误")

    return gt_list


def _generate_github_trending_message(gt_list: List) -> str:
    if not gt_list:
        return "暂无 GitHub 趋势"

    gt_str = "✨=====GitHub Trending=====✨\n"
    for i, trending in enumerate(gt_list[:10]):  # 只获取前10个趋势
        gt_str += (
            f"{i + 1}. 🏎️  {trending['author']} / {trending['repo']}\n"
            f"⭐  {trending['star_total']} total (⭐{trending['star_today']})\n"
            f"🔤  {trending['programmingLanguage']}\n"
            f"📖  {trending['comment']}\n"
        )

    return gt_str
