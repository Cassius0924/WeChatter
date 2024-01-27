import time
from typing import List

import requests

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
    food_list = get_food_list(message)
    if not food_list:
        return "获取食物列表失败"

    food_str = "✨=====食物列表=====✨\n"
    for i, food in enumerate(food_list[:10]):
        food_id = food.get('foodId')
        food_details = get_food_details(food_id)
        food_str += f"{i + 1}.  {food.get('name')}\n{food_details}\n\n"
        time.sleep(0.2)
    return food_str


def get_food_list(message: str) -> List:
    url = (
        f"https://www.mxnzp.com/api/food_heat/food/search?keyword={message}&page=1&app_id=pprqn2hfekkrr8k8&app_secret=nVFcuE6htNjhtGIkJURrS2qQm8L3HUCR")
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print("获取食物列表失败")
        return []
    food_list = response.json()
    return food_list.get("data", {}).get("list", [])


def get_food_value(food, key, default_value=""):
    return food.get(key, default_value)

def get_food_details(food_id: str) -> str:
    if not food_id:
        return "获取食物id失败"

    url = f"https://www.mxnzp.com/api/food_heat/food/details?foodId={food_id}&app_id=pprqn2hfekkrr8k8&app_secret=nVFcuE6htNjhtGIkJURrS2qQm8L3HUCR"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print("获取食物详情失败")
        return ""

    food_details = response.json()
    food = food_details.get("data", {})

    calory = get_food_value(food, 'calory', "")
    protein = get_food_value(food, 'protein', "")
    fat = get_food_value(food, 'fat', "")
    carbohydrate = get_food_value(food, 'carbohydrate', "")
    natrium = get_food_value(food, 'natrium', "")
    zinc = get_food_value(food, 'zinc', "")
    iron = get_food_value(food, 'iron', "")
    calcium = get_food_value(food, 'calcium', "")
    gi_value = get_food_value(food.get('glycemicInfoData', {}).get('gi', {}), 'value', "")
    gi_label = get_food_value(food.get('glycemicInfoData', {}).get('gi', {}), 'label', "")
    gl_value = get_food_value(food.get('glycemicInfoData', {}).get('gl', {}), 'value', "")
    gl_label = get_food_value(food.get('glycemicInfoData', {}).get('gl', {}), 'label', "")
    health_tips = get_food_value(food, 'healthTips', "")
    health_suggest = get_food_value(food, 'healthSuggest', "")

    food_str = (
        f"热量:{calory}卡路里    蛋白质:{protein}g\n"
        f"脂肪:{fat}g    碳水化合物:{carbohydrate}g\n"
        f"钠值:{natrium}mg    锌值:{zinc}mg\n"
        f"铁值:{iron}mg    钙值:{calcium}mg\n"
        f"gi值:{gi_value}({gi_label})    gl值:{gl_value}({gl_label})\n"
        f"{health_tips}({health_suggest})"
    )

    # food_str = f"热量:{food.get('calory')}卡路里    蛋白质:{food.get('protein')}g\n脂肪:{food.get('fat')}g    碳水化合物:{food.get('carbohydrate')}g\n钠值:{food.get('natrium')}mg    锌值:{food.get('zinc')}mg\n铁值:{food.get('iron')}mg    钙值:{food.get('calcium')}mg\ngi值:{food.get('glycemicInfoData').get('gi').get('value')}({food.get('glycemicInfoData').get('gi').get('label')})    gl值:{food.get('glycemicInfoData').get('gl').get('value')}({food.get('glycemicInfoData').get('gi').get('label')})\n{food.get('healthTips')}({food.get('healthSuggest')})"
    return food_str
