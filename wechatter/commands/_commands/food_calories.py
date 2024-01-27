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
    if food_list == []:
        return "获取食物列表失败"
    food_str = "✨=====食物列表=====✨\n"
    for i, food in enumerate(food_list[:10]):
        food_id = food.get('foodId')
        food_details = get_food_details(food_id)
        food_str += f"{i + 1}.  {food.get('name')}\n{food_details}\n\n"
    return food_str


def get_food_list(message: str) -> List:
    url = (
        f"https://www.mxnzp.com/api/food_heat/food/search?keyword={message}&page=1&app_id=pprqn2hfekkrr8k8&app_secret=nVFcuE6htNjhtGIkJURrS2qQm8L3HUCR")
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print("获取食物列表失败")
        return []
    food_list = response.json()
    return food_list.get("data", {}).get("list", {})


def get_food_details(food_id: str) -> str:
    if not food_id:
        return "获取食物id失败"

    # 初始值
    calory = protein = fat = carbohydrate = natrium = zinc = iron = calcium = gi_value = gi_label = gl_value = gl_label = health_tips = health_suggest = ""

    url = (
        f"https://www.mxnzp.com/api/food_heat/food/details?foodId={food_id}&app_id=pprqn2hfekkrr8k8&app_secret=nVFcuE6htNjhtGIkJURrS2qQm8L3HUCR")
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print("获取食物详情失败")
        return ""

    food_details = response.json()
    food = food_details.get("data", {})

    # 如果某个键存在，用实际值替代初始值
    calory = food.get('calory', calory)
    protein = food.get('protein', protein)
    fat = food.get('fat', fat)
    carbohydrate = food.get('carbohydrate', carbohydrate)
    natrium = food.get('natrium', natrium)
    zinc = food.get('zinc', zinc)
    iron = food.get('iron', iron)
    calcium = food.get('calcium', calcium)
    gi_value = food.get('glycemicInfoData', {}).get('gi', {}).get('value', gi_value)
    gi_label = food.get('glycemicInfoData', {}).get('gi', {}).get('label', gi_label)
    gl_value = food.get('glycemicInfoData', {}).get('gl', {}).get('value', gl_value)
    gl_label = food.get('glycemicInfoData', {}).get('gl', {}).get('label', gl_label)
    health_tips = food.get('healthTips', health_tips)
    health_suggest = food.get('healthSuggest', health_suggest)

    # 格式化输出字符串
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
