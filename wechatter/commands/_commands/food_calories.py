from typing import Dict, List
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

from wechatter.commands.handlers import command
from wechatter.exceptions import Bs4ParsingError
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender
from wechatter.utils import get_request


@command(
    command="food-calories",
    keys=["食物热量", "food-calories", "热量", "calories", "卡路里"],
    desc="获取食物热量。",
)
def food_calories_command_handler(to: SendTo, message: str = "") -> None:
    try:
        response = get_request(
            url=f"https://www.boohee.com/food/search?keyword={message}"
        )
        food_href_list = parse_food_href_list_response(response)
        food_detail_list = get_food_detail_list(food_href_list)
        result = generate_food_message(food_detail_list)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, result))
    except Exception as e:
        error_message = f"获取食物热量失败，错误信息：{e}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_food_detail_list(food_href_list: List) -> List:
    food_detail_list = []
    for i, food in enumerate(food_href_list[:5]):
        food_name = food.get("name")
        food_all_name = food.get("all_name")
        food_href = food.get("href")
        keyword = get_url_encoding(food_name)  # 获取URL编码
        headers = {
            "referer": f"https://www.boohee.com/food/search?keyword={keyword}",
        }
        food_response = get_request(
            url=f"https://www.boohee.com{food_href}", headers=headers
        )
        food_detail = parse_food_detail_response(food_response, food_all_name)
        food_detail_list.append(food_detail)
    return food_detail_list


def generate_food_message(food_detail_list: List) -> str:
    food_str = "✨=====食物列表=====✨\n"

    for i, food_detail in enumerate(food_detail_list):
        energy = food_detail["热量(大卡)"]
        carbohydrate = food_detail["碳水化合物(克)"]
        fat = food_detail["脂肪(克)"]
        protein = food_detail["蛋白质(克)"]
        dietary_fiber = food_detail["纤维素(克)"]
        food_all_name = food_detail["food_all_name"]
        food_str += (
            f"{i + 1}. {food_all_name}\n"
            f"    🍲热量(大卡):    {energy}\n"
            f"    🍞碳水(克):        {carbohydrate}\n"
            f"    🥓脂肪(克):        {fat}\n"
            f"    🍗蛋白质(克):    {protein}\n"
            f"    🥦纤维素(克):    {dietary_fiber}\n"
        )
    food_str += "🔵====含量(100克)====🔵"

    return food_str


# 这里也是 parse部分
def parse_food_detail_response(response: requests.Response, food_all_name: str) -> Dict:
    soup = BeautifulSoup(response.text, "html.parser")
    food_detail = {}
    articles = soup.find_all("dd")
    for article in articles:
        name = article.select_one("span.dt").text.strip()
        value = article.select_one("span.dd").text.strip()
        if name and value:
            food_detail[name] = value
    if not food_detail:
        raise Bs4ParsingError("解析食物列表失败")

    food_detail["food_all_name"] = food_all_name
    return food_detail


def parse_food_href_list_response(response: requests.Response) -> List:
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
        raise Bs4ParsingError("解析食物详情链接失败")

    return href_list


def get_url_encoding(message: str) -> str:
    url_encoding = quote(message)
    return url_encoding
