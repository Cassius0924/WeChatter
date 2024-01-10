from typing import Optional

from utils.time import get_current_ymd


def get_paper_people_pdf_url(date_version: str) -> Optional[str]:  # 2024010901
    """获取特定日期特定版本的人民日报pdf到本地并返回url"""
    # 判断字符串是否为数字并且长度为10
    if date_version.isdigit() and len(date_version) == 10:
        yearmonthday = date_version[:8]  # 20240109
        year = date_version[:4]  # 2024
        month = date_version[4:6]  # 01
        day = date_version[6:8]  # 09
        year_month = f"{year}-{month}"  # 2024-01
        version = date_version[8:]  # 01
        # url = "http://paper.people.com.cn/rmrb/images/2024-01/09/01/rmrb2024010901.pdf"
        url = f"http://paper.people.com.cn/rmrb/images/{year_month}/{day}/{version}/rmrb{yearmonthday}{version}.pdf"
        return url
    if not (date_version.isdigit() and len(date_version) == 10):
        print("输入的日期版本号不符合要求，请重新输入...")
        return None


def get_paper_people_url() -> str:
    """获取今日01版人民日报pdf的url"""
    yearmonthday = get_current_ymd()
    version = "01"
    today_version = f"{yearmonthday}{version}"
    url = get_paper_people_pdf_url(today_version)
    return url
