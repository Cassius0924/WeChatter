# from ..basechat import BaseChat
# from wechatter.config import config
# from ..handlers import command
# from ...models.wechat import SendTo
# 
# 
# class OpenaiChatGPT3(BaseChat):
#     def __init__(self):
#         super().__init__(
#             model="gpt-3.5-turbo",
#             api_url=config["openai_base_api"] + "/v1/chat/completions",
#             token="Bearer " + config["openai_token"]
#         )
# 
# 
# OpenaiChatGPT3 = OpenaiChatGPT3()
# 
# 
# # openai_chat_gpt.py
# @command(
#     command="gpt35",
#     keys=["gpt"],
#     desc="使用GPT3.5进行对话。",
# )
# def gpt35_command_handler(to: SendTo, message: str = "", message_obj=None) -> None:
#     OpenaiChatGPT3.gptx("gpt-3.5-turbo", to, message, message_obj)
# 
# 
# @command(
#     command="gpt35-chats",
#     keys=["gpt-chats", "gpt对话记录"],
#     desc="列出GPT3.5对话记录。",
# )
# def gpt35_chats_command_handler(
#         to: SendTo, message: str = "", message_obj=None
# ) -> None:
#     OpenaiChatGPT3.gptx_chats("gpt-3.5-turbo", to, message, message_obj)
# 
# 
# @command(
#     command="gpt35-record",
#     keys=["gpt-record", "gpt记录"],
#     desc="获取GPT3.5对话记录。",
# )
# def gpt35_record_command_handler(
#         to: SendTo, message: str = "", message_obj=None
# ) -> None:
#     OpenaiChatGPT3.gptx_record("gpt-3.5-turbo", to, message)
# 
# 
# @command(
#     command="gpt35-continue",
#     keys=["gpt-continue", "gpt继续"],
#     desc="继续GPT3.5对话。",
# )
# def gpt35_continue_command_handler(
#         to: SendTo, message: str = "", message_obj=None
# ) -> None:
#     OpenaiChatGPT3.gptx_continue("gpt-3.5-turbo", to, message)
# 
# 
# class OpenaiChatGPT4(BaseChat):
#     def __init__(self):
#         super().__init__(
#             model="gpt-4",
#             api_url=config["openai_base_api"] + "/v1/chat/completions",
#             token="Bearer " + config["openai_token"]
#         )
# 
# 
# OpenaiChatGPT4 = OpenaiChatGPT4()
# 
# 
# @command(
#     command="gpt4",
#     keys=["gpt4"],
#     desc="使用GPT4进行对话。",
# )
# def gpt4_command_handler(to: SendTo, message: str = "", message_obj=None) -> None:
#     OpenaiChatGPT4.gptx("gpt-4", to, message, message_obj)
# 
# 
# @command(
#     command="gpt4-chats",
#     keys=["gpt4-chats", "gpt4对话记录"],
#     desc="列出GPT4对话记录。",
# )
# def gpt4_chats_command_handler(to: SendTo, message: str = "", message_obj=None) -> None:
#     OpenaiChatGPT4.gptx_chats("gpt-4", to, message, message_obj)
# 
# 
# @command(
#     command="gpt4-record",
#     keys=["gpt4-record", "gpt4记录"],
#     desc="获取GPT4对话记录。",
# )
# def gpt4_record_command_handler(
#         to: SendTo, message: str = "", message_obj=None
# ) -> None:
#     OpenaiChatGPT4.gptx_record("gpt-4", to, message)
# 
# 
# @command(
#     command="gpt4-continue",
#     keys=["gpt4-continue", "gpt4继续"],
#     desc="继续GPT4对话。",
# )
# def gpt4_continue_command_handler(
#         to: SendTo, message: str = "", message_obj=None
# ) -> None:
#     OpenaiChatGPT4.gptx_continue("gpt-4", to, message)
# 
# 
# # 命令：/gpt4-remove
# def gpt4_remove_command_handler(
#         to: SendTo, message: str = "", message_obj=None
# ) -> None:
#     pass
