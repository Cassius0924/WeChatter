from urllib.parse import urljoin

from loguru import logger


def join_urls(base_url, relative_url) -> str:
    """
    拼接 URL
    :param base_url: 基础 URL
    :param relative_url: 相对 URL
    """
    try:
        return urljoin(base_url, relative_url)
    except TypeError as e:
        logger.error(f"拼接 URL 时出错：{e}")
        raise TypeError(f"拼接 URL 时出错：{e}")
