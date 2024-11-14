from datetime import datetime
from typing import Union, List

from loguru import logger

from wechatter.commands.handlers import command
from wechatter.config import config
from wechatter.database import (
    GptChatInfo as DbGptChatInfo,
    GptChatMessage as DbGptChatMessage,
    make_db_session,
)
from wechatter.models.gpt import GptChatInfo
from wechatter.models.wechat import Person, SendTo
from wechatter.sender import sender
from wechatter.utils import post_request_json
from wechatter.utils.time import get_current_date, get_current_week, get_current_time

DEFAULT_TOPIC = "（对话进行中*）"
# TODO: 初始化对话，Prompt选择
DEFAULT_CONVERSATION = [
    {
        "role": "system",
        "content": f"你的名字是 WeChatter，是一位虚拟助手。今天是{get_current_date()}（年月日），星期{get_current_week()}，现在是{get_current_time()}。",
    }
]

this_model = config["spark_model"]


@command(
    command="spark",
    keys=["spark", "spark_chat"],
    desc="与 Spark AI 聊天",
)
def spark_command_handler(to: SendTo, message: str = "", message_obj=None) -> None:
    _gptx(this_model, to, message, message_obj)


@command(
    command="spark-chats",
    keys=["spark-chats", "spark对话记录"],
    desc="列出Spark对话记录。",
)
def spark_chats_command_handler(to: SendTo, message: str = "", message_obj=None) -> None:
    _gptx_chats(this_model, to, message, message_obj)


@command(
    command="spark-record",
    keys=["spark-record", "spark记录"],
    desc="获取Spark对话记录。",
)
def spark_record_command_handler(
        to: SendTo, message: str = "", message_obj=None
) -> None:
    _gptx_record(this_model, to, message)


@command(
    command="spark-continue",
    keys=["spark-continue", "spark继续"],
    desc="继续Spark对话。",
)
def spark_continue_command_handler(
        to: SendTo, message: str = "", message_obj=None
) -> None:
    _gptx_continue(this_model, to, message)


def _gptx(model: str, to: SendTo, message: str = "", message_obj=None) -> None:
    person = to.person
    # 获取文件夹下最新的对话记录
    chat_info = SparkChat.get_chatting_chat_info(person, model)
    if message == "":  # /gpt4
        # 判断对话是否有效
        sender.send_msg(to, "正在创建新对话...")
        if chat_info is None or SparkChat._is_chat_valid(chat_info):
            SparkChat.create_chat(person, model)
            logger.info("创建新对话成功")
            sender.send_msg(to, "创建新对话成功")
            return
        logger.info("对话未开始，继续上一次对话")
        sender.send_msg(to, "对话未开始，继续上一次对话")
    else:  # /gpt4 <message>
        # 如果没有对话记录，则创建新对话
        sender.send_msg(to, f"正在调用 {model} 进行对话...")
        if chat_info is None:
            chat_info = SparkChat.create_chat(person, model)
            logger.info("无历史对话记录，创建新对话成功")
            sender.send_msg(to, "无历史对话记录，创建新对话成功")
        try:
            response = SparkChat.chat(
                chat_info, message=message, message_obj=message_obj
            )
            logger.info(response)
            sender.send_msg(to, response)
        except Exception as e:
            error_message = f"调用{this_model}服务失败，错误信息：{str(e)}"
            logger.error(error_message)
            sender.send_msg(to, error_message)


def _gptx_chats(model: str, to: SendTo, message: str = "", message_obj=None) -> None:
    response = SparkChat.get_chat_list_str(to.person, model)
    sender.send_msg(to, response)


def _gptx_record(model: str, to: SendTo, message: str = ""):
    person = to.person
    if message == "":
        # 获取当前对话的对话记录
        chat_info = SparkChat.get_chatting_chat_info(person, model)
    else:
        # 获取指定对话的对话记录
        chat_info = SparkChat.get_chat_info(person, model, int(message))
    if chat_info is None:
        logger.warning("对话不存在")
        sender.send_msg(to, "对话不存在")
        return
    response = SparkChat.get_brief_conversation_str(chat_info)
    logger.info(response)
    sender.send_msg(to, response)


def _gptx_continue(model: str, to: SendTo, message: str = "") -> None:
    person = to.person
    # 判断message是否为数字
    if not message.isdigit():
        logger.info("请输入对话记录编号")
        sender.send_msg(to, "请输入对话记录编号")
        return
    sender.send_msg(to, f"正在切换到对话记录 {message}...")
    chat_info = SparkChat.continue_chat(
        person=person, model=model, chat_index=int(message)
    )
    if chat_info is None:
        warning_message = "选择历史对话失败，对话不存在"
        logger.warning(warning_message)
        sender.send_msg(to, warning_message)
        return
    response = SparkChat.get_brief_conversation_str(chat_info)
    response += "====================\n"
    response += "对话已选中，输入命令继续对话"
    logger.info(response)
    sender.send_msg(to, response)


class SparkChat:
    spark_api = config["spark_api"]
    token = "Bearer " + config["spark_token"]

    @staticmethod
    def create_chat(person: Person, model: str) -> GptChatInfo:
        """
        创建一个新的对话
        :param person: 用户
        :param model: 模型
        :return: 新的对话信息
        """
        # 生成上一次对话的主题
        SparkChat._save_chatting_chat_topic(person, model)
        SparkChat._set_all_chats_not_chatting(person, model)
        gpt_chat_info = GptChatInfo(
            person=person,
            model=model,
            topic=DEFAULT_TOPIC,
            is_chatting=True,
        )
        with make_db_session() as session:
            _gpt_chat_info = DbGptChatInfo.from_model(gpt_chat_info)
            session.add(_gpt_chat_info)
            session.commit()
            # 获取 SQLite 自动生成的 chat_id
            session.refresh(_gpt_chat_info)
            gpt_chat_info = _gpt_chat_info.to_model()
            return gpt_chat_info

    @staticmethod
    def continue_chat(
            person: Person, model: str, chat_index: int
    ) -> Union[GptChatInfo, None]:
        """
        继续对话，选择历史对话
        :param person: 用户
        :param model: 模型
        :param chat_index: 对话记录索引（从1开始）
        :return: 对话信息
        """
        # 读取对话记录文件
        chat_info = SparkChat.get_chat_info(person, model, chat_index)
        if chat_info is None:
            return None
        chatting_chat_info = SparkChat.get_chatting_chat_info(person, model)
        if chatting_chat_info:
            if not SparkChat._is_chat_valid(chatting_chat_info):
                # 如果对话无效，则删除该对话记录后再继续对话
                SparkChat._delete_chat(chatting_chat_info)
            else:
                # 生成上一次对话的主题
                SparkChat._save_chatting_chat_topic(person, model)
        SparkChat._set_chatting_chat(person, model, chat_info)
        return chat_info

    @staticmethod
    def _set_chatting_chat(person: Person, model: str, chat_info: GptChatInfo) -> None:
        """
        设置正在进行中的对话记录
        """
        # 先将所有对话记录的 is_chatting 字段设置为 False
        SparkChat._set_all_chats_not_chatting(person, model)
        with make_db_session() as session:
            chat_info = session.query(DbGptChatInfo).filter_by(id=chat_info.id).first()
            if chat_info is None:
                logger.error("对话记录不存在")
                raise ValueError("对话记录不存在")
            chat_info.is_chatting = True
            session.commit()

    @staticmethod
    def _delete_chat(chat_info: GptChatInfo) -> None:
        """
        删除对话记录
        """
        with make_db_session() as session:
            session.query(DbGptChatMessage).filter_by(gpt_chat_id=chat_info.id).delete()
            session.query(DbGptChatInfo).filter_by(id=chat_info.id).delete()
            session.commit()

    @staticmethod
    def get_brief_conversation_str(chat_info: GptChatInfo) -> str:
        """
        获取对话记录的字符串
        :param chat_info: 对话记录
        :return: 对话记录字符串
        """
        with make_db_session() as session:
            chat_info = session.query(DbGptChatInfo).filter_by(id=chat_info.id).first()
            if chat_info is None:
                logger.error("对话记录不存在")
                raise ValueError("对话记录不存在")
            conversation_str = f"✨==={chat_info.topic}===✨\n"
            if not chat_info.gpt_chat_messages:
                conversation_str += "    无对话记录"
                return conversation_str
            for msg in chat_info.gpt_chat_messages:
                content: str = msg.message.content
                # 合并成一行，提升观感
                content = content.replace("\n", "")
                # 去掉命令前缀和命令关键词
                content = content[content.find(" ") + 1:][:30]
                response = msg.gpt_response[:30]
                response = response.replace("\n", "")
                if len(msg.message.content) > 30:
                    content += "..."
                if len(msg.gpt_response) > 30:
                    response += "..."
                conversation_str += f"💬：{content}\n"
                conversation_str += f"🤖：{response}\n"
            return conversation_str

    @staticmethod
    def _set_all_chats_not_chatting(person: Person, model: str) -> None:
        """
        将所有对话记录的 is_chatting 字段设置为 False
        """
        with make_db_session() as session:
            session.query(DbGptChatInfo).filter_by(
                person_id=person.id, model=model
            ).update({"is_chatting": False})
            session.commit()

    @staticmethod
    def _list_chat_info(person: Person, model: str) -> List:
        """
        列出用户的所有对话记录
        """
        # 按照 chat_talk_time 字段倒序排序，取前20个
        with make_db_session() as session:
            chat_info_list = (
                session.query(DbGptChatInfo)
                .filter_by(person_id=person.id, model=model)
                .order_by(
                    DbGptChatInfo.is_chatting.desc(),
                    DbGptChatInfo.talk_time.desc(),
                )
                .limit(20)
                .all()
            )
            _chat_info_list = []
            for chat_info in chat_info_list:
                _chat_info_list.append(chat_info.to_model())
            return _chat_info_list

    @staticmethod
    def get_chat_list_str(person: Person, model: str) -> str:
        """
        获取用户的所有对话记录
        :param person: 用户
        :param model: 模型
        :return: 对话记录
        """
        chat_info_list = SparkChat._list_chat_info(person, model)
        chat_info_list_str = f"✨==={model}对话记录===✨\n"
        if not chat_info_list:
            chat_info_list_str += "     📭 无对话记录"
            return chat_info_list_str
        with make_db_session() as session:
            for i, chat_info in enumerate(chat_info_list):
                chat = session.query(DbGptChatInfo).filter_by(id=chat_info.id).first()
                if chat.is_chatting:
                    chat_info_list_str += f"{i + 1}. 💬{chat.topic}\n"
                else:
                    chat_info_list_str += f"{i + 1}. {chat.topic}\n"
            return chat_info_list_str

    @staticmethod
    def get_chat_info(
            person: Person, model: str, chat_index: int
    ) -> Union[GptChatInfo, None]:
        """
        获取用户的对话信息
        :param person: 用户
        :param model: 模型
        :param chat_index: 对话记录索引（从1开始）
        :return: 对话信息
        """
        chat_info_id_list = SparkChat._list_chat_info(person, model)
        if not chat_info_id_list:
            return None
        if chat_index <= 0 or chat_index > len(chat_info_id_list):
            return None
        return chat_info_id_list[chat_index - 1]

    @staticmethod
    def get_chatting_chat_info(person: Person, model: str) -> Union[GptChatInfo, None]:
        """
        获取正在进行中的对话信息
        :param person: 用户
        :param model: 模型
        :return: 对话信息
        """
        with make_db_session() as session:
            chat_info = (
                session.query(DbGptChatInfo)
                .filter_by(person_id=person.id, model=model, is_chatting=True)
                .first()
            )
            if not chat_info:
                return None
            return chat_info.to_model()

    @staticmethod
    def chat(chat_info: GptChatInfo, message: str, message_obj) -> str:
        """
        持续对话
        :param chat_info: 对话信息
        :param message: 用户消息
        :param message_obj: 消息对象
        :return: GPT 回复
        """
        # 对外暴露的对话方法，必须保存对话记录
        return SparkChat._chat(
            chat_info=chat_info, message=message, message_obj=message_obj, is_save=True
        )

    @staticmethod
    def _chat(chat_info: GptChatInfo, message: str, message_obj, is_save: bool) -> str:
        """
        持续对话
        :param chat_info: 对话信息
        :param message: 用户消息
        :param message_obj: 消息对象
        :param is_save: 是否保存此轮对话记录
        :return: GPT 回复
        """
        newconv = [{"role": "user", "content": message}]
        # 发送请求
        headers = {
            "Authorization": SparkChat.token,
            "Content-Type": "application/json",
        }
        json = {
            "model": this_model,
            "messages": DEFAULT_CONVERSATION + chat_info.get_conversation() + newconv,
        }
        r_json = post_request_json(
            url=SparkChat.spark_api, headers=headers, json=json, timeout=60
        )

        print(r_json)
        # 判断是否有 error 或 code 字段
        if r_json:
            SparkChat._check_r_json(r_json)

        msg = r_json["choices"][0]["message"]
        msg_content = msg.get("content", "调用" + this_model + "服务失败")
        # 将返回的 assistant 回复添加到对话记录中
        if is_save is True:
            newconv.append({"role": "assistant", "content": msg_content})
            chat_info.extend_conversation(newconv)
            with make_db_session() as session:
                _chat_info = (
                    session.query(DbGptChatInfo).filter_by(id=chat_info.id).first()
                )
                _chat_info.talk_time = datetime.now()
                for chat_message in chat_info.gpt_chat_messages[-len(newconv) // 2:]:
                    _chat_message = DbGptChatMessage.from_model(chat_message)
                    _chat_message.message_id = message_obj.id
                    _chat_info.gpt_chat_messages.append(_chat_message)
                session.commit()
        return msg_content

    @staticmethod
    def _check_r_json(r_json):
        if "error" in r_json:
            raise ValueError(this_model + " 服务返回值错误")
        if "code" in r_json:
            code = r_json["code"]
            error_messages = {
                0: None,  # 成功，不抛出异常
                10007: this_model + " 用户流量受限：服务正在处理用户当前的问题，需等待处理完成后再发送新的请求。（必须要等大模型完全回复之后，才能发送下一个问题）",
                10013: this_model + " 输入内容审核不通过，涉嫌违规，请重新调整输入内容",
                10014: this_model + " 输出内容涉及敏感信息，审核不通过，后续结果无法展示给用户",
                10019: this_model + " 表示本次会话内容有涉及违规信息的倾向；建议开发者收到此错误码后给用户一个输入涉及违规的提示",
                10907: this_model + " token数量超过上限。对话历史+问题的字数太多，需要精简输入",
                11200: this_model + " 授权错误：该appId没有相关功能的授权 或者 业务量超过限制",
                11201: this_model + " 授权错误：日流控超限。超过当日最大访问量的限制",
                11202: this_model + " 授权错误：秒级流控超限。秒级并发超过授权路数限制",
                11203: this_model + " 授权错误：并发流控超限。并发路数超过授权路数限制",
            }
            error_message = error_messages.get(code)
            if error_message:
                raise ValueError(error_message)

    @staticmethod
    def _save_chatting_chat_topic(person: Person, model: str) -> None:
        """
        生成正在进行的对话的主题
        """
        chat_info = SparkChat.get_chatting_chat_info(person, model)
        if chat_info is None or SparkChat._has_topic(chat_info):
            return
        # 生成对话主题
        if not SparkChat._is_chat_valid(chat_info):
            logger.error("对话记录长度小于1")
            return

        topic = SparkChat._generate_chat_topic(chat_info)
        if not topic:
            logger.error("生成对话主题失败")
            raise ValueError("生成对话主题失败")
        # 更新对话主题
        with make_db_session() as session:
            chat_info = session.query(DbGptChatInfo).filter_by(id=chat_info.id).first()
            chat_info.topic = topic
            session.commit()

    @staticmethod
    def _generate_chat_topic(chat_info: GptChatInfo) -> str:
        """
        生成对话主题，用于保存对话记录
        """
        assert SparkChat._is_chat_valid(chat_info)
        # 通过一次对话生成对话主题，但这次对话不保存到对话记录中
        prompt = "请用10个字以内总结一下这次对话的主题，不带任何标点符号"
        topic = SparkChat._chat(
            chat_info=chat_info, message=prompt, message_obj=None, is_save=False
        )
        # 限制主题长度
        if len(topic) > 21:
            topic = topic[:21] + "..."
        logger.info(f"生成对话主题：{topic}")
        return topic

    @staticmethod
    def _has_topic(chat_info: GptChatInfo) -> bool:
        """
        判断对话是否有主题
        """
        return chat_info.topic != DEFAULT_TOPIC

    @staticmethod
    def _is_chat_valid(chat_info: GptChatInfo) -> bool:
        """
        判断对话是否有效
        """
        if chat_info.gpt_chat_messages:
            return True
        return False
