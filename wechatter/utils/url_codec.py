from urllib.parse import quote, quote_plus, unquote, unquote_plus


def url_encode(s: str, safe=":/?=&", plus: bool = False) -> str:
    """
    对字符串进行url编码
    :param s: 待编码字符串
    :param safe: 保留字符
    :param plus: 是否用"+"替换空格
    :return: 编码后的字符串
    """
    if plus:
        return quote_plus(s, safe=safe)
    else:
        return quote(s, safe=safe)


def url_decode(s: str, plus: bool = False) -> str:
    """
    对字符串进行url解码
    :param s: 待解码字符串
    :param plus: 是否用"+"替换空格
    :return: 解码后的字符串
    """
    if plus:
        return unquote_plus(s)
    else:
        return unquote(s)
