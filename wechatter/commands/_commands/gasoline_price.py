import requests
from bs4 import BeautifulSoup
from loguru import logger

import wechatter.utils.path_manager as pm
from wechatter.commands.handlers import command
from wechatter.exceptions import Bs4ParsingError
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender
from wechatter.utils import get_request, load_json


@command(
    command="gasoline_price",
    keys=["汽油", "gasoline_price", "汽油价格", "中石化"],
    desc="获取汽油价格。",
)
def gasoline_price_command_handler(to: SendTo, message: str = "") -> None:
    try:
        result = get_gasoline_price_str(message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, result))
    except Exception as e:
        error_message = f"获取汽油价格失败，错误信息：{e}"
        logger.error(error_message)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, error_message))


# TODO：查询其他类型的油价，如95，97柴油等，例子：查询95号汽油只需改成{city_id}_4_1.html
# TODO: 现在查询的是中国石油化工,添加查询中国石油天然气，只需改成{city_id}_2_2.html
# 封装起来，方便定时任务调用
def get_gasoline_price_str(city_name: str) -> str:
    """
    获取城市的汽油价格
    :param city_name: 城市名
    :return: 汽油价格
    """
    if city_name == "":
        return "请输入城市名，如：广州"
    else:
        city_id = _get_city_id(city_name)
        if not city_id:
            raise KeyError(f"未找到城市 {city_name}。")

        response = get_request(
            url=f"https://www.icauto.com.cn/oil/price_{city_id}_2_1.html"
        )
        gasoline_price = _parse_gasoline_price_response(response)
        return _generate_gasoline_price_message(gasoline_price, city_name)


def _parse_gasoline_price_response(response: requests.Response) -> str:
    """
    解析汽油价格响应
    :param response: 响应
    :return: 汽油价格
    """
    soup = BeautifulSoup(response.text, 'html.parser')
    article_body_div = soup.select_one("div.articlebody")

    if article_body_div:
        # 找到div内的第二个p元素
        second_p_element = article_body_div.find_all('p')[1]

        if second_p_element:
            # 提取第二个p元素的文本内容
            text_content = second_p_element.get_text()
            desired_text = text_content.split('，若需要计算')[0]

        else:
            logger.error("找不到第二个p元素")
            raise Bs4ParsingError("找不到第二个p元素")
    else:
        logger.error("找不到class等于'articlebody'的div")
        raise Bs4ParsingError("找不到class等于'articlebody'的div")
    return desired_text


CITY_IDS_PATH = pm.get_abs_path("assets/gasoline_price_china/city_ids.json")


def _get_city_id(city_name: str) -> str:
    """
    获取城市代码
    :param city_name: 城市名
    :return: 城市代码
    """
    city_ids = load_json(CITY_IDS_PATH)

    if city_name not in city_ids.keys():
        logger.error(f"未找到城市 {city_name}。")
        raise KeyError(f"未找到城市 {city_name}。")
    return city_ids[city_name]


def _generate_gasoline_price_message(gasoline_price: str, message: str) -> str:
    return f"✨{message}石化92汽油指导价✨\n\n{gasoline_price}\n\n油价数据仅供参考,实际在售油价可能有小幅偏差。"
