from typing import List
import requests


def get_douyin_hot_str() -> str:
    hot_list = get_douyin_hot_list()
    if hot_list == []:
        return "获取抖音热搜失败"
    hot_str = "✨=====抖音热搜=====✨\n"
    for i, hot_search in enumerate(hot_list[:20]):
        hot_str += f"{i + 1}.  {hot_search.get('word')}\n"
    return hot_str


def get_douyin_hot_list() -> List:
    # url = "https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/?reflow_source=reflow_page&web_id=7320147385195562523&device_id=7320147385195562523&msToken=FmBVSfj564dcrkJbxohUGZiGSE6fw62Q65ZPE__0DJgSc2fC72tLeVPNnDJQNue0jLa1PwmpgrNGL4KclXaTdGgnpPHXDXYNLWpK-YDRL9-oSsA1weeUhhClzuoq-g%3D%3D&a_bogus=YyUDXchBMsm1qDfeawkz9yvm-1E0YW5IgZEF2UUzGULg"
    url = "https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print("获取抖音热搜失败")
        return []
    hot_dict = response.json()
    return hot_dict.get("word_list", [])


# def get_douyin_hot_list() -> list:
#     url = "https://www.douyin.com/discover"
#     response = requests.get(url)
#     #
#     # if response.status_code == 200:
#     #     soup = BeautifulSoup(response.text, "html.parser")
#
#     if response.status_code != 200:
#         print(f"请求失败，状态码：{response.status_code}，响应内容：{response.text}")
#         return []
#
#     try:
#         soup = BeautifulSoup(response.text, "html.parser")
#     except Exception as e:
#         print(f"解析HTML失败，错误信息：{e}")
#         return []
#
#         hot_list = []
#         hot_items = soup.select("ul.hotChangableList li.WW9U4EAc div.VOZdGLLy")
#         for hot_item in hot_items:
#             hot = {}  # Create an empty dictionary for each hot item
#
#             title = hot_item.select_one("div.h0x1L5tb a.hY8lWHgA h3")
#             if title:
#                 hot["title"] = title.text.strip()
#             else:
#                 hot["title"] = "No title"
#
#             hot_value = hot_item.select_one("div.xiPUg0i8 span.R_6SmOx4")
#             if hot_value:
#                 hot["hot_value"] = hot_value.text.strip()
#             else:
#                 hot["hot_value"] = "No value"
#
#             if hot:  # Check if the dictionary is not empty before appending
#                 hot_list.append(hot)
#
#         return hot_list[:10]
#
#     print("获取抖音热搜失败")
#     return []


# 好像有反爬虫
# def get_douyin_hot_list() -> list:
#     url = "https://tophub.today/n/K7GdaMgdQy"
#     response = requests.get(url)
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # this will raise an exception if the status code is not 200
#     except HTTPError as http_err:
#         if http_err.response.status_code == 503:
#             print("The server is temporarily unavailable. Please try again later.")
#         else:
#             print(f"An HTTP error occurred: {http_err}")
#         return []
#     except RequestException as req_err:
#         print(f"A network error occurred: {req_err}")
#         return []
#
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, "html.parser")
#
#         hot_list = []
#         hot_items = soup.select("div.jc-c table.table tbody tr")
#         for hot_item in hot_items:
#             hot = {}  # Create an empty dictionary for each hot item
#
#             title = hot_item.select_one("td.al a")
#             if title:
#                 hot["title"] = title.text.strip()
#
#             hot_value = hot_item.select_one("td:nth-of-type(3)")
#             if hot_value:
#                 hot["hot_value"] = hot_value.text.strip()
#
#             if hot:  # Check if the dictionary is not empty before appending
#                 hot_list.append(hot)
#
#         return hot_list[:20]
#
#     print("获取抖音热搜失败")
#     return []
