from typing import Optional

from pydantic import BaseModel


class UrlLink(BaseModel):
    """
    链接消息类
    """

    title: str
    url: str
    desc: Optional[str] = None
    cover_url: Optional[str] = None
