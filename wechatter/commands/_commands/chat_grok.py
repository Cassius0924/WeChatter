from ..basechat import BaseChat
from wechatter.config import config
from ..handlers import command
from ...models.wechat import SendTo

this_model = config["grok_model"]


class Grok(BaseChat):
    def __init__(self):
        super().__init__(
            model=this_model,
            api_url=config["grok_api"],
            token="Bearer " + config["grok_token"]
        )


Grok = Grok()


@command(
    command="grok",
    keys=["grok"],
    desc="使用grok进行对话。",
)
def grok_command_handler(to: SendTo, message: str = "", message_obj=None) -> None:
    Grok.gptx(this_model, to, message, message_obj)
    
@command(
    command="grok-chats",
    keys=["grok-chats", "grok对话记录"],
    desc="列出grok对话记录。",
)
def grok_chats_command_handler(to: SendTo, message: str = "", message_obj=None) -> None:
    Grok.gptx_chats(this_model, to, message, message_obj)


@command(
    command="grok-record",
    keys=["grok-record", "grok记录"],
    desc="获取grok对话记录。",
)
def grok_record_command_handler(
        to: SendTo, message: str = "", message_obj=None
) -> None:
    Grok.gptx_record(this_model, to, message)


@command(
    command="grok-continue",
    keys=["grok-continue", "grok继续"],
    desc="继续grok对话。",
)
def grok_continue_command_handler(
        to: SendTo, message: str = "", message_obj=None
) -> None:
    Grok.gptx_continue(this_model, to, message)
