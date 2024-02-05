from dataclasses import dataclass

from wechatter.models.message.message import MessageSource


@dataclass
class SendTo:
    """发送对象类"""

    p_id: str
    p_name: str
    # p_alias: str
    g_id: str
    g_name: str

    @classmethod
    def from_message_source(cls, source: MessageSource):
        p_id = ""
        p_name = ""
        # p_alias = ""
        g_id = ""
        g_name = ""
        if source.p_info is not None:
            p_id = source.p_info.id
            p_name = source.p_info.name
        if source.g_info is not None:
            g_id = source.g_info.id
            g_name = source.g_info.name
        return cls(p_id, p_name, g_id, g_name)
