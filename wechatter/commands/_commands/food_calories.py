from typing import List

import requests
import json

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
    try:
        response = get_food_str(message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))
    except Exception as e:
        error_message = f"获取食物热量失败，错误信息：{e}"
        print(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


def get_food_str(message: str) -> str:
    food_list = get_food_namelist(message)
    if not food_list:
        return "获取食物列表失败"

    food_str = "✨=====食物列表=====✨\n"
    for i, food in enumerate(food_list[:5]):

        food_name = food_list[i][2]
        Another_name = food_list[i][3]
        English_name = food_list[i][4]
        Edible = food_list[i][5]
        Water = food_list[i][6]

        # 处理 Energy 字段
        Energy = food_list[i][7]
        energy_kj = float(''.join(c for c in Energy if c.isdigit() or c == '.'))  # 提取数字部分并转换为浮点数
        energy_kcal = energy_kj / 4.184  # 转换为大卡
        energy_str = f"{energy_kcal:.2f}大卡"  # 格式化为字符串

        Protein = food_list[i][8]
        Fat = food_list[i][9]
        Carbohydrate = food_list[i][12]
        Dietary_fiber = food_list[i][13]
        food_str += f"{i + 1}. {food_name}\n✅能量:{energy_str}\n✅俗名:{Another_name:<12}✅英文名:{English_name}\n✅可食部分:{Edible:<10}✅水分:{Water}\n✅蛋白质:{Protein:<11}✅脂肪:{Fat}\n✅碳水化合物:{Carbohydrate:<9}✅膳食纤维:{Dietary_fiber}\n\n"


def get_food_namelist(message: str) -> List:
    url = "https://nlc.chinanutri.cn/fq/FoodInfoQueryAction!queryFoodInfoList.do"

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }
    # categoryOne:一级分类，categoryTwo:二级分类，foodName:食物名称，pageNum:页码，field:排序字段，flag:排序方式

    data = {
        'categoryOne': '0',
        'categoryTwo': '0',
        'foodName': message,
        'pageNum': '1',
        'field': '0',
        'flag': '0'
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        return []

    try:
        text = response.text
        data = json.loads(text)
        food_list = data["list"]
        return food_list
    except Exception as e:
        print(f"解析食物列表失败, 错误信息: {str(e)}")
        return []
