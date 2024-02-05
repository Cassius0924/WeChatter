from typing import Dict, List
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from loguru import logger

from wechatter.commands.handlers import command
from wechatter.exceptions import Bs4ParsingError
from wechatter.models.message import SendTo
from wechatter.sender import sender
from wechatter.utils import get_request


@command(
    command="food-calories",
    keys=["食物热量", "food-calories", "热量", "calories", "卡路里"],
    desc="获取食物热量。",
)
def food_calories_command_handler(to: SendTo, message: str = "") -> None:
    try:
        result = get_food_calories_str(message)
    except Exception as e:
        error_message = f"获取食物热量失败，错误信息：{str(e)}"
        logger.error(error_message)
        sender.send_msg(to, error_message)
    else:
        sender.send_msg(to, result)


def get_food_calories_str(message: str) -> str:
    if not message:
        return "查询失败，请输入食物名称"
    response = get_request(url=f"https://www.boohee.com/food/search?keyword={message}")
    food_href_list = _parse_food_href_list_response(response)
    food_detail_list = _get_food_detail_list(food_href_list)
    result = _generate_food_message(food_detail_list)
    return result


def _get_food_detail_list(food_href_list: List) -> List:
    """
    获取食物详情列表
    :param food_href_list: 食物详情链接列表
    :return: 食物详情列表
    """
    food_detail_list = []
    for i, food in enumerate(food_href_list[:5]):
        food_name = food.get("name")
        food_all_name = food.get("all_name")
        food_href = food.get("href")
        keyword = _get_url_encoding(food_name)  # 获取URL编码
        headers = {
            "referer": f"https://www.boohee.com/food/search?keyword={keyword}",
        }
        food_response = get_request(
            url=f"https://www.boohee.com{food_href}", headers=headers
        )
        if not food_response:
            logger.error(f"获取食物详情失败，食物名称：{food_name}")
            raise ValueError(f"获取食物详情失败，食物名称：{food_name}")
        food_detail = _parse_food_detail_response(food_response, food_all_name)
        food_detail_list.append(food_detail)
    if not food_detail_list:
        logger.error("获取食物详情失败,为空列表")
        raise ValueError("获取食物详情失败,为空列表")
    return food_detail_list


def _generate_food_message(food_detail_list: List) -> str:
    """
    生成食物信息
    :param food_detail_list: 食物详情列表
    :return: 食物信息
    """
    if not food_detail_list:
        logger.error("食物详情列表为空")
        raise ValueError("食物详情列表为空")
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
def _parse_food_detail_response(
    response: requests.Response, food_all_name: str
) -> Dict:
    """
    解析食物详情
    :param response: 请求响应
    :param food_all_name: 食物全名
    :return: 食物详情
    """
    soup = BeautifulSoup(response.text, "html.parser")
    food_detail = {}
    articles = soup.find_all("dd")
    for article in articles:
        name = article.select_one("span.dt").text.strip()
        value = article.select_one("span.dd").text.strip()
        if name and value:
            food_detail[name] = value
    if not food_detail:
        logger.error("解析食物列表失败")
        raise Bs4ParsingError("解析食物列表失败")

    food_detail["food_all_name"] = food_all_name
    return food_detail


def _parse_food_href_list_response(response: requests.Response) -> List:
    """
    解析食物详情链接列表
    :param response: 请求响应
    :return: 食物详情链接列表
    """
    soup = BeautifulSoup(response.text, "html.parser")
    href_list = []
    articles = soup.select("div.text-box")
    if not articles:
        logger.error("解析食物详情链接失败")
        raise Bs4ParsingError("解析食物详情链接失败")
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
        logger.error("解析食物详情链接失败")
        raise Bs4ParsingError("解析食物详情链接失败")

    return href_list


def _get_url_encoding(message: str) -> str:
    """
    获取URL编码
    :param message: 消息
    :return: URL编码
    """
    url_encoding = quote(message)
    return url_encoding
