from typing import List

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender


@command(
    command="food-calories",
    keys=["食物热量", "food-calories", "热量", "calories", "卡路里"],
    desc="获取食物热量。",
    value=51,
)
def food_calories_command_handler(to: SendTo, message: str = "") -> None:
    response = get_food_str(message)
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))


def get_food_str(message: str) -> str:
    food_list = get_food_namelist(message)
    if not food_list:
        return "获取食物列表失败"

    food_str = "✨=====食物列表=====✨\n"
    for i, food in enumerate(food_list):
        food_str += f"{i + 1}. {food.get('title')}\n"


def get_food_namelist(message: str) -> List:
    # 设置 Chrome 为无头浏览器
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 创建浏览器对象
    driver = webdriver.Chrome(options=chrome_options)
    try:
        url = f"https://nlc.chinanutri.cn/fq/foodlist_{message}_0_0_0_0_1.htm"
        driver.get(url)

        # 等待页面加载完成（可以根据实际情况调整等待时间）
        driver.implicitly_wait(10)

        # 获取加载后的页面HTML
        html = driver.page_source

        # 关闭浏览器
        driver.quit()
    except Exception:
        print("请求食物列表失败")
        return []

