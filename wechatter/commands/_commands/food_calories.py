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

    food_str = "✨=====食物列表=====✨\n"
    for i, food in enumerate(food_list[:5]):
        food_name = food.get("name")
        food_href = food.get("href")
        food_detail = get_food_list_html(food_name, food_href)

        food_str += f"{i + 1}. {food_name}\n{food_detail}\n\n"


def get_food_list_html(name: str, href: str) -> str:
    response: requests.Response

    keyword = get_URL_encoding(name)  # 获取URL编码
    href = get_food_href_list(href)  # 获取食物链接

    try:
        url = f"https://www.boohee.com{href}"
        headers = {
            'referer': f'https://www.boohee.com/food/search?keyword={keyword}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        }

        response = requests.get(url, headers=headers)
    except Exception as e:
        raise Exception(f"获取食物列表失败，错误信息：{e}")

    food_all_deatil = get_food_detail(response.text)
    if not food_all_deatil:
        raise Exception("获取食物列表失败")

    food_detail = ""
    # name
    energy = food_all_deatil[2]["name"]
    carbohydrate = food_all_deatil[3]["name"]
    fat = food_all_deatil[4]["name"]
    protein = food_all_deatil[5]["name"]
    dietary_fiber = food_all_deatil[6]["name"]
    calcium = food_all_deatil[16]["name"]
    iron = food_all_deatil[17]["name"]
    zinc = food_all_deatil[18]["name"]

    # value
    Energy = food_all_deatil[2]["value"]
    Carbohydrate = food_all_deatil[3]["value"]
    Fat = food_all_deatil[4]["value"]
    Protein = food_all_deatil[5]["value"]
    Dietary_fiber = food_all_deatil[6]["value"]
    Calcium = food_all_deatil[16]["value"]
    Iron = food_all_deatil[17]["value"]
    Zinc = food_all_deatil[18]["value"]

    food_detail += f"✅{energy:<10}{Energy}\n✅{carbohydrate:<10}{Carbohydrate}\n✅{fat:<10}{Fat}\n✅{protein:<10}{Protein}\n✅{dietary_fiber:<10}{Dietary_fiber}\n✅{calcium:<10}{Calcium}\n✅{iron:<10}{Iron}\n✅{zinc:<10}{Zinc}\n"

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
            'authority': 'www.boohee.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': 'Hm_lvt_7263598dfd4db0dc29539a51f116b23a=1706356236; acw_tc=0b68a81617067204120465900e927fd6fbf44399a30eebaf658011ec9947f3; _mboohee_session=a2lsRSt1djJCL3ppNDRmdU53bUovSHpvbVBSaCswMTFwME5nSTZXWGJQbExMR1dqV1ozTkJxMTBHRXl4ZmpjMDZkUHd6NE9CUUF6MW9ZMW1ZSUgyR0hQbElHcm1xQXVzNXFwRDVGQjlpVWpJd0RlODZmWGNsMlpRWC8wYkxVbitFaHZ0WVA2VDc3aUp4bGdSZkx6dnN3PT0tLTUxdDVvbWxVcUVGMFhESnB6VzZJS2c9PQ^%^3D^%^3D--adf27b85cfd243fb59157fff7a23794f47d05460; Hm_lpvt_7263598dfd4db0dc29539a51f116b23a=1706720434',
            'referer': 'https://www.boohee.com/food',
            'sec-ch-ua': '^\^"Not A(Brand^\^";v=^\^"99^\^", ^\^"Microsoft Edge^\^";v=^\^"121^\^", ^\^"Chromium^\^";v=^\^"121^\^""',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '^\^"Windows^\^"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
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
        href = article.a["href"]
        if href:
            href_list_item["href"] = href

        if href_list_item:
            href_list.append(href_list_item)

    if not href_list:
        raise Exception("解析食物链接失败")

    return href_list
