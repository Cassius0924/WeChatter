from typing import Dict

import requests
from loguru import logger

DEAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
}


def get_request(
    url, params=None, headers=DEAULT_HEADERS, timeout=5
) -> requests.Response:
    """
    发送GET请求，并返回Response对象
    :param url: 请求的URL
    :param params: 请求参数（默认为None）
    :param headers: 请求头（默认为带有User-Agent的请求头）
    :param timeout: 超时时间（默认为5秒）
    :return: Response对象
    """
    headers = _check_headers(headers)
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.encoding = "utf-8"
        response.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
    except requests.ConnectionError as e:
        logger.error(f"请求 {url} 失败，连接错误：{e}")
        raise
    except requests.HTTPError as e:
        logger.error(f"请求 {url} 失败，HTTP错误：{e}")
        raise
    except requests.Timeout as e:
        logger.error(f"请求 {url} 失败，请求超时：{e}")
        raise
    except requests.URLRequired as e:
        logger.error(f"请求 {url} 失败，无效的URL：{e}")
        raise
    except requests.TooManyRedirects as e:
        logger.error(f"请求 {url} 失败，重定向次数过多：{e}")
        raise
    except Exception as e:
        logger.error(f"请求 {url} 失败，未知错误：{e}")
        raise
    else:
        return response


def get_request_json(url, params=None, headers=DEAULT_HEADERS, timeout=5) -> Dict:
    """
    发送GET请求，并解析返回的JSON
    :param url: 请求的URL
    :param params: 请求参数（默认为None）
    :param headers: 请求头（默认为带有User-Agent的请求头）
    :param timeout: 超时时间（默认为5秒）
    :return: JSON对象
    """
    response = get_request(url, params=params, headers=headers, timeout=timeout)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        logger.error("解析 {url} 返回的JSON失败")
        raise


def post_request(
    url, data=None, json=None, files=None, headers=DEAULT_HEADERS, timeout=5
) -> requests.Response:
    """
    发送POST请求，并返回Response对象
    :param url: 请求的URL
    :param data: 请求体（默认为None）
    :param json: 请求体（默认为None）
    :param files: 文件（默认为None）
    :param headers: 请求头（默认为带有User-Agent的请求头）
    :param timeout: 超时时间（默认为5秒）
    :return: Response对象
    """
    headers = _check_headers(headers)
    try:
        response = requests.post(
            url, data=data, json=json, files=files, headers=headers, timeout=timeout
        )
        response.raise_for_status()
    except requests.ConnectionError as e:
        logger.error(f"请求 {url} 失败，连接错误：{e}")
        raise
    except requests.HTTPError as e:
        logger.error(f"请求 {url} 失败，HTTP错误：{e}")
        raise
    except requests.Timeout as e:
        logger.error(f"请求 {url} 失败，请求超时：{e}")
        raise
    except requests.URLRequired as e:
        logger.error(f"请求 {url} 失败，无效的URL：{e}")
        raise
    except requests.TooManyRedirects as e:
        logger.error(f"请求 {url} 失败，重定向次数过多：{e}")
        raise
    except Exception as e:
        logger.error(f"请求 {url} 失败，未知错误：{e}")
        raise
    else:
        response.encoding = "utf-8"
        return response


def post_request_json(
    url, data=None, json=None, files=None, headers=DEAULT_HEADERS, timeout=5
) -> Dict:
    """
    发送POST请求，并解析返回的JSON
    :param url: 请求的URL
    :param data: 请求体（默认为None）
    :param json: 请求体（默认为None）
    :param files: 文件（默认为None）
    :param headers: 请求头（默认为带有User-Agent的请求头）
    :param timeout: 超时时间（默认为5秒）
    :return: JSON对象
    """
    response = post_request(
        url, data=data, json=json, files=None, headers=headers, timeout=timeout
    )
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"解析 {url} 返回的JSON失败，错误信息：{str(e)}")
        raise


# 检测 headers，是否包含 User-Agent，如果没有，就添加一个默认的 User-Agent
def _check_headers(headers: Dict) -> Dict:
    if "User-Agent" not in headers:
        headers["User-Agent"] = DEAULT_HEADERS["User-Agent"]
    return headers
