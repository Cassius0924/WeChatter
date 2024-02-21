from typing import Optional

from pydantic import BaseModel

QUOTABLE_FORMAT = "（可引用：%s）\n"


class QuotedResponse(BaseModel):
    """
    引用回复类
    """

    command: str
    response: str
    id: Optional[int] = None
    quotable_id: Optional[str] = None
