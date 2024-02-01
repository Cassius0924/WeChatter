from typing import List, Dict
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender


@command(
    command="food-calories",
    keys=["食物热量", "food-calories", "热量", "calories", "卡路里"],
    desc="获取食物热量。",
    value=150,
)
def food_calories_command_handler(to: SendTo, message: str = "") -> None:
    try:
        response = get_food_str(message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))
    except Exception as e:
        error_message = f"获取食物热量失败，错误信息：{e}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_food_str(message: str) -> str:
    food_list = get_food_href_list(message)
    if not food_list:
        return "获取食物列表失败"

    food_str = "✨=====食物列表=====✨\n🔵====含量(100克)====🔵\n"
    for i, food in enumerate(food_list[:5]):
        food_name = food.get("name")
        food_all_name = food.get("all_name")
        food_href = food.get("href")
        food_detail = get_food_list_html(food_name, food_href)

        food_str += f"{i + 1}. {food_all_name}\n{food_detail}\n"

    return food_str


def get_food_list_html(name: str, href: str) -> str:
    response: requests.Response

    keyword = get_URL_encoding(name)  # 获取URL编码

    try:
        url = f"https://www.boohee.com{href}"
        headers = {
            'referer': f'https://www.boohee.com/food/search?keyword={keyword}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        }

        response = requests.get(url, headers=headers)
    except Exception as e:
        raise Exception(f"获取食物列表失败，错误信息：{e}")

    get_food_det = get_food_detail(response.text)
    if not get_food_det:
        raise Exception("获取食物列表失败")

    food_detail = ""
    # # name
    energy = get_food_det[2]["name"]
    carbohydrate = get_food_det[3]["name"]
    fat = get_food_det[4]["name"]
    protein = get_food_det[5]["name"]
    dietary_fiber = get_food_det[6]["name"]
    # calcium = get_food_det[16]["name"]
    # iron = get_food_det[17]["name"]
    # zinc = get_food_det[18]["name"]
    #
    # # value
    Energy = get_food_det[2]["value"]
    Carbohydrate = get_food_det[3]["value"]
    Fat = get_food_det[4]["value"]
    Protein = get_food_det[5]["value"]
    Dietary_fiber = get_food_det[6]["value"]
    # Calcium = get_food_det[16]["value"]
    # Iron = get_food_det[17]["value"]
    # Zinc = get_food_det[18]["value"]
    #
    food_detail += f"✅{energy:<10}{Energy}\n✅{carbohydrate:<10}{Carbohydrate}\n✅{fat:<10}{Fat}\n✅{protein:<10}{Protein}\n✅{dietary_fiber:<10}{Dietary_fiber}\n"

    return food_detail


def get_food_detail(response: str) -> list:
    soup = BeautifulSoup(response, "html.parser")
    food_detail = []
    articles = soup.find_all("dd")
    for article in articles:
        food_detail_item = {}

        name = article.select_one("span.dt").text.strip()
        if name:
            food_detail_item["name"] = name
        value = article.select_one("span.dd").text.strip()
        if value:
            food_detail_item["value"] = value

        if food_detail_item:
            food_detail.append(food_detail_item)

    if not food_detail:
        raise Exception("解析食物列表失败")

    return food_detail


def get_URL_encoding(message: str) -> str:
    url_encoding = quote(message)
    return url_encoding


def get_food_href_list(message: str) -> List[Dict[str, str]]:
    try:
        url = f"https://www.boohee.com/food/search?keyword={message}"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        }
        response = requests.get(url, timeout=10, headers=headers)
    except Exception as e:
        raise Exception(f"获取食物链接失败，错误信息：{e}")

    soup = BeautifulSoup(response.text, "html.parser")
    href_list = []
    articles = soup.select("div.text-box")
    for article in articles:
        href_list_item = {}

        name = article.select_one("a").text.strip()
        if name:
            href_list_item["name"] = name.split("，")[0]
            href_list_item["all_name"] = name
        href = article.a["href"]
        if href:
            href_list_item["href"] = href

        if href_list_item:
            href_list.append(href_list_item)

    if not href_list:
        raise Exception("解析食物链接失败")

    return href_list
