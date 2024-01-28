# 天气命令
import json
from typing import List

import requests
from bs4 import BeautifulSoup
from requests import Response

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender
from wechatter.utils.path_manager import PathManager
from wechatter.utils.time import get_current_hour, get_current_minute, get_current_ymd


@command(
    command="weather",
    keys=["weather", "天气", "天气预报", "几度"],
    desc="获取天气预报",
    value=160,
)
def weather_command_handler(to: SendTo, message: str = "") -> None:
    response = get_weather_str(message)
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, response))


# class WeatherTip:
#     def __init__(self, priority, condition, tip):
#         self.priority = priority
#         self.condition = condition
#         self.tip = tip
#
#     def __lt__(self, other):
#         return self.priority < other.priority
#
#
# weather_tips = [
#     WeatherTip(20, "tornado", "龙卷风来临，请立即寻找避难所！"),
#     WeatherTip(19, "hurricane", "飓风来临，请尽快找一个安全的地方避难！"),
#     WeatherTip(18, "blizzard", "暴风雪来临，尽量避免出门，注意保暖！"),
#     WeatherTip(17, "thunderstorm", "雷雨天气，尽量待在室内，避免接触金属物品！"),
#     WeatherTip(16, "heavy_rain", "大雨来临，出行请带伞，注意防滑！"),
#     WeatherTip(15, "heavy_snow", "大雪纷飞，出行请注意路滑，穿暖和！"),
#     WeatherTip(14, "hail", "冰雹天气，尽量避免出门，保护好车辆！"),
#     WeatherTip(13, "frost", "霜冻天气，早晚出行请注意路面可能滑！"),
#     WeatherTip(12, "fog", "雾天行驶，请开启雾灯，保持安全距离！"),
#     WeatherTip(11, "sleet", "雨夹雪天气，出行请注意防滑，穿暖和！"),
#     WeatherTip(10, "rain", "今天有雨，记得带伞！"),
#     WeatherTip(9, "snow", "今天有雪，记得ç©¿暖和！"),
#     WeatherTip(8, "high_temperature", "高温天气，注意防暑，多喝水！"),
#     WeatherTip(7, "low_temperature", "低温天气，注意保暖！"),
#     WeatherTip(6, "wind", "风大，注意防风保暖！"),
#     WeatherTip(5, "cloudy", "多云天气，适合出门散步！"),
#     WeatherTip(4, "partly_cloudy", "局部多云，今天的天气还不错！"),
#     WeatherTip(3, "clear_night", "夜晚天空晴朗，适合观星！"),
#     WeatherTip(2, "sunny", "阳光明媚，出门请带好太阳镜和防晒霜！"),
#     WeatherTip(1, "fair", "天气晴朗，是出门活动的好时机！"),
# ]

# windDY = ["无持续风向", "东北风", "东风", "东南风", "南风", "西南风", "西风", "西北风", "北风", "旋转风"]
#
# windJB = ["<3级", "3-4级", "4-5级", "5-6级", "6-7级", "7-8级", "8-9级", "9-10级", "10-11级", "11-12级"]

qxbm = {
    0: "晴",
    1: "多云",
    2: "阴",
    3: "阵雨",
    4: "雷阵雨",
    5: "雷阵雨伴有冰雹",
    6: "雨夹雪",
    7: "小雨",
    8: "中雨",
    9: "大雨",
    "00": "晴",
    "01": "多云",
    "02": "阴",
    "03": "阵雨",
    "04": "雷阵雨",
    "05": "雷阵雨伴有冰雹",
    "06": "雨夹雪",
    "07": "小雨",
    "08": "中雨",
    "09": "大雨",
    10: "暴雨",
    11: "大暴雨",
    12: "特大暴雨",
    13: "阵雪",
    14: "小雪",
    15: "中雪",
    16: "大雪",
    17: "暴雪",
    18: "雾",
    19: "冻雨",
    20: "沙尘暴",
    21: "小到中雨",
    22: "中到大雨",
    23: "大到暴雨",
    24: "暴雨到大暴雨",
    25: "大暴雨到特大暴雨",
    26: "小到中雪",
    27: "中到大雪",
    28: "大到暴雪",
    29: "浮尘",
    30: "扬沙",
    31: "强沙尘暴",
    53: "霾",
    99: "无",
    32: "浓雾",
    49: "强浓雾",
    54: "中度霾",
    55: "重度霾",
    56: "严重霾",
    57: "大雾",
    58: "特强浓雾",
    97: "雨",
    98: "雪",
    301: "雨",
    302: "雪",
}

time_emojis = {
    0: "🕛",
    1: "🕐",
    2: "🕑",
    3: "🕒",
    4: "🕓",
    5: "🕔",
    6: "🕕",
    7: "🕖",
    8: "🕗",
    9: "🕘",
    10: "🕙",
    11: "🕚",
    12: "🕛",
    13: "🕐",
    14: "🕑",
    15: "🕒",
    16: "🕓",
    17: "🕔",
    18: "🕕",
    19: "🕖",
    20: "🕗",
    21: "🕘",
    22: "🕙",
    23: "🕚",
    24: "🕛",
    25: "🕐",
    26: "🕑",
    27: "🕒",
    28: "🕓",
    29: "🕔",
}


def _get_city_id(city_name: str) -> int:
    """
    获取城市代码
    :param city: 城市名
    :return: 城市代码
    """
    # 读取JSON
    with open(
        PathManager.get_abs_path("assets/weather_china/city_ids.json"),
        "r",
        encoding="utf-8",
    ) as f:
        try:
            city_ids = json.load(f)
        except Exception:
            print("读取城市代码失败")
            return -1
    # 遍历JSON
    if city_name in city_ids.keys():
        return city_ids[city_name]
    return -1


def _get_hourly_weather(city_id: int) -> dict:
    response: Response
    try:
        url = f"http://www.weather.com.cn/weather1dn/{city_id}.shtml"
        response = requests.get(url)
        response.encoding = "utf-8"
    except Exception:
        print("获取天气失败")
        return {}

    if response.status_code != 200:
        print("获取天气失败")
        return {}
    soup = BeautifulSoup(response.text, "html.parser")
    weather_chart_div = soup.find("div", class_="todayRight")
    # 获取hour3data
    data = weather_chart_div.find("script").string
    hour3data = json.loads(data.split("var hour3data=")[1].split(";")[0])
    event_day = json.loads(data.split("var eventDay =")[1].split(";")[0])
    event_night = json.loads(data.split("var eventNight =")[1].split(";")[0])
    temp = {"max": event_day, "min": event_night}
    sun_rise = json.loads(data.split("var sunup =")[1].split(";")[0])
    sun_set = json.loads(data.split("var sunset =")[1].split(";")[0])
    sun_time = {"sun_rise": sun_rise, "sun_set": sun_set}
    helper_div = soup.find("div", class_="weather_shzs")
    dls = helper_div.find("div", class_="lv").find_all("dl")
    uv = dls[0].find("em").string
    air = dls.pop().find("em").string

    return {
        "weather": hour3data,
        "temp": temp,
        "sun_time": sun_time,
        "uv": uv,
        "air": air,
    }


def _get_current_weather(city_id: int) -> dict:
    # 获取当前天气
    response: Response
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "http://www.weather.com.cn/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    }
    try:
        url = f"http://d1.weather.com.cn/sk_2d/{city_id}.html"
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"
    except Exception:
        print("获取天气失败")
        return {}

    if response.status_code != 200:
        print("获取天气失败")
        return {}
    return json.loads(response.text.split("=")[1])


def _get_sun_time(sunset: List, sunrise: List) -> dict:
    # 计算当前时间的总分钟数
    now_all_m = get_current_hour() * 60 + get_current_minute()

    # 计算日出和日落的总分钟数
    rise_all_m = int(sunrise[0].split(":")[0]) * 60 + int(sunrise[0].split(":")[1])
    set_all_m = int(sunset[0].split(":")[0]) * 60 + int(sunset[0].split(":")[1])

    # 根据当前时间判断日出和日落的时间
    if rise_all_m > now_all_m:
        return {
            "sun_set_name": "今日日落",
            "sun_set": sunset[0],
            "sun_rise_name": "今日日出",
            "sun_rise": sunrise[0],
        }
    elif now_all_m >= rise_all_m and set_all_m > now_all_m:
        return {
            "sun_set_name": "今日日落",
            "sun_set": sunset[0],
            "sun_rise_name": "明日日出",
            "sun_rise": sunrise[1],
        }
    else:
        return {
            "sun_set_name": "明日日落",
            "sun_set": sunset[1],
            "sun_rise_name": "明日日出",
            "sun_rise": sunrise[1],
        }


def _get_future_weather(h_data: List, now_h: int, hours: int) -> List:
    """
    获取未来几小时的天气
    :param h_data: 逐小时天气
    :param now_h: 当前小时
    :param hours: 未来几小时
    :return: 未来几小时的天气
    """
    now_date = get_current_ymd()
    now_datetime = ""
    # now_h 补前导零
    if now_h < 10:
        now_datetime = now_date + "0" + str(now_h)
    else:
        now_datetime = now_date + str(now_h)
    future_weather_list = []
    count = 0
    for hourly_data in h_data:
        for hour in hourly_data:
            if hour["jf"] > now_datetime:
                future_weather_list.append(hour)
                count += 1
                if count == hours:
                    return future_weather_list
    return future_weather_list


def get_weather_str(city_name: str) -> str:
    city_id = _get_city_id(city_name)
    if city_id == -1:
        return "城市名错误"
    _h_data = _get_hourly_weather(city_id)
    c_data = _get_current_weather(city_id)
    h = int(c_data["time"].split(":")[0])
    h_data = _h_data["weather"]
    temp = _h_data["temp"]
    date = c_data["date"].replace("(", " ")[:-1]
    sun_time = _get_sun_time(
        _h_data["sun_time"]["sun_set"], _h_data["sun_time"]["sun_rise"]
    )
    future_weather = _get_future_weather(h_data, h, 5)
    future_str = ""
    for index, hour in enumerate(future_weather):
        future_str += f"{qxbm[hour['ja']]}{hour['jb']}° "
    # TODO: TIP 设计
    message = (
        f"🏙️ {c_data['cityname']} 📅 {date}\n"
        f"🌡️ 温度: {temp['min'][1]}°C ~ {temp['max'][1]}°C\n"
        f"🌤️ 天气: {c_data['weather']}（{time_emojis[h]}当前{c_data['temp']}°C）\n"
        f"📈 逐时: {future_str}\n"
        f"☀️ {sun_time['sun_rise_name']}: {sun_time['sun_rise']} {sun_time['sun_set_name']}: {sun_time['sun_set']}\n"
        f"💨 {c_data['WS']} 😷{_h_data['air']} 💧{c_data['SD']} 🌞{_h_data['uv']}\n"
        # f"💡 会下雨，记得带伞！💡\n"
    )
    return message
