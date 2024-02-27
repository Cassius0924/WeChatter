from typing import Dict, Type

from loguru import logger

from wechatter.commands.handlers import command
from wechatter.models.wechat import Message, SendTo
from wechatter.sender import sender
from wechatter.utils.unique_list import UniqueList

from ._games import *  # noqa: F403
from .game import Game

games = {}
game_class_name_dict: Dict[str, Type[Game]] = {}


def load_games():
    """
    加载所有游戏
    """
    for game in Game.__subclasses__():
        games[game.name] = {
            "class": game,
            "desc": game.desc,
            "keys": game.keys,
        }
        game_class_name_dict[game.__name__] = game
        logger.info(f"加载游戏: {game.name}")
        logger.info(f"游戏描述: {game.desc}")
        logger.info(f"游戏关键字: {game.keys}")

        @command(
            command=game.name,
            keys=game.keys,
            desc=game.desc,
        )
        def game_command_handler(to: SendTo, message: str = "", message_obj=None):
            """
            创建游戏
            """
            _execute_game("create", to, message, message_obj, game_class=game)

    _register_game_basic_command()
    logger.info(f"共加载了{len(games)}个游戏")


def _execute_game(
    cmd: str,
    to: SendTo,
    message: str,
    message_obj: Message,
    game_class: Type[Game] = None,
):
    """
    执行游戏命令
    :param cmd: 游戏命令（create、start、join、play、over）
    :param to: 发送对象
    :param message: 消息内容
    :param message_obj: 消息对象
    :param game_class: 游戏类
    """
    # 目前只支持群中游戏
    if not message_obj.is_group:
        logger.info("目前只支持群中游戏！")
        message = "目前只支持群中游戏！"
        sender.send_msg(message_obj.sender_name, message, is_group=message_obj.is_group)
        return

    # 从数据库中获取未结束的游戏的游戏状态
    group_id = None
    if message_obj.is_group:
        group_id = message_obj.group.id
    game_states = Game.get_game_states(
        person_id=message_obj.person.id, group_id=group_id
    )
    if cmd == "create":
        # 有游戏在进行中
        if game_states:
            message = (
                "当前已有游戏在进行中！\n"
                "若要创建新游戏，请使用 over 命令结束当前游戏。"
            )
            sender.send_msg(
                message_obj.sender_name, message, is_group=message_obj.is_group
            )
            return

        group = None
        if to.group:
            group = to.group
        game = game_class(
            game_host_person=to.person,
            game_players=UniqueList([to.person]),
            game_host_group=group,
        )
        game.create_game()
        return

    if game_states is None:
        message = "当前没有游戏在进行中！"
        sender.send_msg(message_obj.sender_name, message, is_group=message_obj.is_group)
        return

    game_class = game_class_name_dict[game_states.game_class_name]
    game = game_class.from_dict(game_states.states)
    if cmd == "start":
        game.start_game(player=to.person, game_states=game_states)
    elif cmd == "join":
        game.join_game(player=to.person, message=message, game_states=game_states)
    elif cmd == "play":
        game.play_game(player=to.person, message=message, game_states=game_states)
    elif cmd == "over":
        game.over_game(message=message, game_states=game_states)


def _register_game_basic_command():
    @command(
        command="start",
        keys=["start", "开始"],
        desc="开始游戏",
    )
    def start_game_handler(to: SendTo, message: str = "", message_obj=None):
        """
        开始游戏
        """
        _execute_game("start", to, message, message_obj)

    @command(
        command="join",
        keys=["join", "加入"],
        desc="加入游戏",
    )
    def join_game_handler(to: SendTo, message: str = "", message_obj=None):
        """
        加入游戏
        """
        _execute_game("join", to, message, message_obj)

    @command(
        command="play",
        keys=["play", "玩"],
        desc="进行一回合游戏",
    )
    def play_game_handler(to: SendTo, message: str = "", message_obj=None):
        """
        进行一回合游戏
        """
        _execute_game("play", to, message, message_obj)

    @command(
        command="over",
        keys=["over", "结束"],
        desc="结束游戏",
    )
    def over_game_handler(to: SendTo, message: str = "", message_obj=None):
        """
        结束游戏
        """
        _execute_game("over", to, message, message_obj)


__all__ = ["load_games", "games", "game_class_name_dict", "Game"]
