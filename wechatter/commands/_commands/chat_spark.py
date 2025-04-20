# from datetime import datetime
# 
# from wechatter.config import config
# from ..handlers import command
# from ...models.wechat import SendTo
# from ..basechat import BaseChat, DEFAULT_CONVERSATION
# from wechatter.models.gpt import GptChatInfo
# from ...utils import post_request_json
# from wechatter.database import (
#     GptChatInfo as DbGptChatInfo,
#     GptChatMessage as DbGptChatMessage,
#     make_db_session,
# )
# 
# this_model = config["spark_model"]
# 
# 
# class SparkChat(BaseChat):
#     def __init__(self):
#         super().__init__(
#             model=this_model,
#             api_url=config["spark_api"],
#             token="Bearer " + config["spark_token"]
#         )
# 
# 
# SparkChat = SparkChat()
# 
# 
# @command(
#     command="spark",
#     keys=["spark", "spark_chat"],
#     desc="与 Spark AI 聊天",
# )
# def spark_command_handler(to: SendTo, message: str = "", message_obj=None) -> None:
#     SparkChat.gptx(this_model, to, message, message_obj)
# 
# 
# @command(
#     command="spark-chats",
#     keys=["spark-chats", "spark对话记录"],
#     desc="列出Spark对话记录。",
# )
# def spark_chats_command_handler(to: SendTo, message: str = "", message_obj=None) -> None:
#     SparkChat.gptx_chats(this_model, to, message, message_obj)
# 
# 
# @command(
#     command="spark-record",
#     keys=["spark-record", "spark记录"],
#     desc="获取Spark对话记录。",
# )
# def spark_record_command_handler(
#         to: SendTo, message: str = "", message_obj=None
# ) -> None:
#     SparkChat.gptx_record(this_model, to, message)
# 
# 
# @command(
#     command="spark-continue",
#     keys=["spark-continue", "spark继续"],
#     desc="继续Spark对话。",
# )
# def spark_continue_command_handler(
#         to: SendTo, message: str = "", message_obj=None
# ) -> None:
#     SparkChat.gptx_continue(this_model, to, message)
