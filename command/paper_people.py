import os
from typing import Optional

import requests

from utils.path import get_abs_path
from utils.time import get_current_ymd


def has_downloaded_paper_pdf(date_version: str) -> bool:
    """判断是否已经下载了人民日报pdf到本地"""
    yearmonthday = date_version[:8] if date_version.isdigit() and len(date_version) == 10 else ""
    version = date_version[8:] if date_version.isdigit() and len(date_version) == 10 else ""

    save_path = get_abs_path(f"data/paper_people_pdf/{yearmonthday}{version}.pdf")
    return os.path.exists(save_path)


def download_paper_pdf(url: str, save_path: str) -> None:
    """下载人民日报pdf到本地"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
            print(f"下载成功，保存路径为{save_path}")
        else:
            print(f"下载失败，状态码为{response.status_code}")
    except Exception as e:
        print(f"下载失败，错误为{e}")


def get_paper_pdf_url(date_version: str) -> Optional[str]:
    """获取特定日期特定版本的人民日报pdf的URL"""
    yearmonthday = date_version[:8] if date_version.isdigit() and len(date_version) == 10 else ""
    version = date_version[8:] if date_version.isdigit() and len(date_version) == 10 else ""

    year_month = f"{yearmonthday[:4]}-{yearmonthday[4:6]}" if yearmonthday else ""
    day = yearmonthday[6:8] if yearmonthday else ""

    url = f"http://paper.people.com.cn/rmrb/images/{year_month}/{day}/{version}/rmrb{yearmonthday}{version}.pdf"
    return url if yearmonthday and version else print("输入的日期版本号不符合要求，请重新输入...") and None


def get_paper_pdf_path(date_version: str) -> Optional[str]:
    """获取特定日期特定版本的人民日报pdf的路径"""
    if not (date_version.isdigit() and len(date_version) == 10):
        print("输入的日期版本号不符合要求，请重新输入...")
        return None

    yearmonthday = date_version[:8]
    version = date_version[8:]
    save_path = get_abs_path(f"data/paper_people_pdf/{yearmonthday}{version}.pdf")

    if has_downloaded_paper_pdf(date_version):
        print(f"已经下载过{save_path}")
        return save_path
    else:
        pdf_url = get_paper_pdf_url(date_version)
        if pdf_url:
            download_paper_pdf(pdf_url, save_path)
            return save_path
        else:
            return None


def get_today_paper_pdf_url() -> Optional[str]:
    """获取今日01版人民日报pdf的URL"""
    today_date_version = get_current_ymd() + "01"
    return get_paper_pdf_url(today_date_version)


def get_today_paper_pdf_path() -> Optional[str]:
    """获取今日01版人民日报pdf的路径"""
    today_date_version = get_current_ymd() + "01"
    return get_paper_pdf_path(today_date_version)

# import os
# from typing import Optional
#
# import requests
# from utils.time import get_current_year_month, get_current_day, get_current_ymd
# from utils.path import get_abs_path
# #TODO:封装是否已经下载过人民日报pdf到本地方法
# def download_paper_people_pdf(date_version: str) -> str:
#     """判断是否已经人民日报pdf到本地"""
#     pass
#
# def get_paper_people_pdf_url(date_version: str) -> str:#2024010901
#     """获取特定日期特定版本的人民日报pdf到本地并返回url"""
#     #判断字符串是否为数字并且长度为10
#     if date_version.isdigit() and len(date_version) == 10:
#         yearmonthday = date_version[:8]#20240109
#         year = date_version[:4]#2024
#         month = date_version[4:6]#01
#         day = date_version[6:8]#09
#         year_month = f"{year}-{month}"#2024-01
#         version = date_version[8:]#01
#         save_path = get_abs_path(f"data/paper_people_pdf/{yearmonthday}{version}.pdf")
#         # url = "http://paper.people.com.cn/rmrb/images/2024-01/09/01/rmrb2024010901.pdf"
#         url = f"http://paper.people.com.cn/rmrb/images/{year_month}/{day}/{version}/rmrb{yearmonthday}{version}.pdf"
#
#         # 判断是否已经人民日报pdf到本地
#         if os.path.exists(save_path):
#             print(f"已经下载过{save_path}")
#             return url
#         else:
#             try:
#                 response = requests.get(url, timeout=10)
#                 if response.status_code == 200:
#                     with open(save_path, "wb") as file:
#                         file.write(response.content)
#                     print(f"下载成功，保存路径为{save_path}")
#                 else:
#                     print(f"下载失败，状态码为{response.status_code}")
#             except Exception as e:
#                 print(f"下载失败，错误为{e}")
#             return url
#     if not (date_version.isdigit() and len(date_version) == 10):
#         e = "输入的日期版本号不符合要求，请重新输入\n若要获取2021年1月2日03版的人民日报的url，请输入\n/people url 2021010203"
#         return e
#
# def get_paper_people_url() -> str:
#     """获取今日01版人民日报pdf的url"""
#     yearmonthday = get_current_ymd()
#     version = "01"
#     today_version = f"{yearmonthday}{version}"
#     url = get_paper_people_pdf_url(today_version)
#     return url
#
# def get_paper_people_dateversionpdf(date_version: str) -> Optional[str]:
#     """获取特定日期特定版本的人民日报pdf的路径"""
#     #判断字符串是否为数字并且长度为10
#     if date_version.isdigit() and len(date_version) == 10:
#         yearmonthday = date_version[:8]#20240109
#         year = date_version[:4]#2024
#         month = date_version[4:6]#01
#         day = date_version[6:8]#09
#         year_month = f"{year}-{month}"#2024-01
#         version = date_version[8:]#01
#         save_path = get_abs_path(f"data/paper_people_pdf/{yearmonthday}{version}.pdf")
#         # url = "http://paper.people.com.cn/rmrb/images/2024-01/09/01/rmrb2024010901.pdf"
#         url = f"http://paper.people.com.cn/rmrb/images/{year_month}/{day}/{version}/rmrb{yearmonthday}{version}.pdf"
#
#         # 判断是否已经人民日报pdf到本地
#         if os.path.exists(save_path):
#             print(f"已经下载过{save_path}")
#             return save_path
#         else:
#             try:
#                 response = requests.get(url, timeout=10)
#                 if response.status_code == 200:
#                     with open(save_path, "wb") as file:
#                         file.write(response.content)
#                     print(f"下载成功，保存路径为{save_path}")
#                 else:
#                     print(f"下载失败，状态码为{response.status_code}")
#             except Exception as e:
#                 print(f"下载失败，错误为{e}")
#             return save_path
#     if not (date_version.isdigit() and len(date_version) == 10):
#         print("输入的日期版本号不符合要求，请重新输入...")
#         return None
#
#
# def get_paper_people_todaypdf() -> str:#2024010901
#     """获取今日01版人民日报pdf的路径"""
#     yearmonthday = get_current_ymd()
#     version = "01"
#     today_version = f"{yearmonthday}{version}"
#     save_path = get_paper_people_dateversionpdf(today_version)
#     return save_path
