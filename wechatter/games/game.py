from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from loguru import logger

from wechatter.database import GameStates as DbGameStates, make_db_session
from wechatter.models.game import GameStates
from wechatter.models.wechat import Group, Person
from wechatter.sender import sender
from wechatter.utils.unique_list import UniqueList


class Game(ABC):
    """
    聊天交互式游戏基类
    """

    name: str
    desc: str
    keys: List[str]

    def __init__(
        self,
        game_host_person: Person,
        game_players: UniqueList[Person],
        game_host_group: Group = None,
        least_player_num: int = 0,
        most_player_num: int = 0,
    ):
        """
        初始化游戏
        :param game_host_person: 游戏创建者
        :param game_players: 参与游戏的玩家（包括创建者）
        :param game_host_group: 游戏创建者所在群
        :param least_player_num: 最少玩家数
        :param most_player_num: 最多玩家数
        """
        self.game_host_person = game_host_person
        self.game_players = game_players
        self.game_host_group = game_host_group
        self.least_player_num = least_player_num
        self.most_player_num = most_player_num
        # 是否已开始
        self.is_started = False
        # 当前回合数
        self.round = 0
        if game_host_group:
            # 发送者名称
            self.sender_name = game_host_group.name
            # 是否是群游戏
            self.is_group = True
        else:
            self.sender_name = game_host_person.name
            self.is_group = False
        # 是否可以加入游戏
        self.can_join = True
        # 当前玩家下标
        self.current_player_index = 0
        pass

    @classmethod
    def from_dict(cls, data: Dict):
        instance = cls.__new__(cls)
        instance.game_host_person = Person(**data["game_host_person"])
        game_players = UniqueList()
        for player in data["game_players"]:
            game_players.add(Person(**player))
        instance.game_players = game_players
        if data["is_group"]:
            instance.game_host_group = Group(**data["game_host_group"])
        instance.least_player_num = data["least_player_num"]
        instance.most_player_num = data["most_player_num"]
        instance.is_group = data["is_group"]
        instance.is_started = data["is_started"]
        instance.sender_name = data["sender_name"]
        instance.round = data["round"]
        instance.can_join = data["can_join"]
        instance.current_player_index = data["current_player_index"]
        # 填充子类属性
        instance.fill_from_dict(data)
        return instance

    @staticmethod
    def get_game_states(
        person_id: str, group_id: Optional[str] = None
    ) -> Optional[GameStates]:
        """
        获取游戏状态
        """

        # 检测是否有游戏在进行中
        with make_db_session() as session:
            if group_id:
                _game_states = (
                    session.query(DbGameStates)
                    .filter_by(host_group_id=group_id, is_over=False)
                    .first()
                )
            else:
                # TODO: 去群中心化游戏
                _game_states = (
                    session.query(DbGameStates)
                    .filter_by(host_person_id=person_id, is_over=False)
                    .first()
                )
            # 有游戏在进行中
            if _game_states:
                game_states = _game_states.to_model()
                return game_states
            return None

    def create_game(self):
        """
        创建游戏
        """
        with make_db_session() as session:
            # 插入新游戏状态
            game_states = GameStates(
                host_person=self.game_host_person,
                host_group=self.game_host_group,
                game_class_name=self.__class__.__name__,
                states=self.to_dict(),
            )
            _game_states = DbGameStates.from_model(game_states)
            session.add(_game_states)
            session.commit()
            self.create()

    def start_game(self, player: Person, game_states: GameStates):
        # 消息发送者是否为游戏创建者
        if player.id != self.game_host_person.id:
            logger.warning(
                f"⚠️ 只有游戏创建者 {self.game_host_person.name} 可以开始游戏！"
            )
            self._send_msg(
                f"⚠️ 只有游戏创建者 {self.game_host_person.name} 可以开始游戏！"
            )
            return

        # 判断游戏是否已经开始
        if self.is_started:
            logger.warning("⚠️ 游戏已开始！")
            self._send_msg("⚠️ 游戏已开始！")
            return
        # 判断游戏人数是否满足最少游戏人数
        if len(self.game_players) < self.least_player_num:
            logger.warning(
                f"⚠️ 游戏人数不足，无法开始游戏！最低游戏人数为 {self.least_player_num} 人。"
            )
            self._send_msg(
                f"⚠️ 游戏人数不足，无法开始游戏！最低游戏人数为 {self.least_player_num} 人。"
            )
            return

        self.is_started = True
        self.start(game_states)

        with make_db_session() as session:
            _game_states = (
                session.query(DbGameStates).filter_by(id=game_states.id).first()
            )
            # TODO: 直接优化成表的一个字段？
            game_states.states = self.to_dict()
            _game_states.update(game_states)
            session.commit()

        logger.info("游戏开始！")

    def join_game(self, player: Person, message: str, game_states: GameStates):
        """
        加入游戏
        """
        # 判断游戏是否已经开始
        if self.is_started:
            logger.warning("⚠️ 游戏已开始！无法加入游戏！")
            self._send_msg("⚠️ 游戏已开始！无法加入游戏！")
            return

        # 判断游戏人数是否大于等于最多游戏人数
        if len(self.game_players) >= self.most_player_num:
            self.can_join = False
            logger.warning(
                f"⚠️ 游戏人数已满，无法加入游戏！最多游戏人数为 {self.most_player_num} 人。"
            )
            self._send_msg(
                f"⚠️ 游戏人数已满，无法加入游戏！最多游戏人数为 {self.most_player_num} 人。"
            )
            return

        if self.can_join:
            try:
                self.game_players.add(player)
                logger.info(f"{player.name} 加入游戏成功！")
            # 已经在游戏中
            except ValueError:
                logger.warning(f"⚠️ 加入游戏失败，{player.name} 已经在游戏中！")
                self._send_msg(f"⚠️ 加入游戏失败，{player.name} 已经在游戏中！")
                return

        if len(self.game_players) >= self.most_player_num:
            self.can_join = False

        self.join(player, message, game_states)

        # 更新游戏状态
        with make_db_session() as session:
            _game_states = (
                session.query(DbGameStates).filter_by(id=game_states.id).first()
            )
            game_states.states = self.to_dict()
            _game_states.update(game_states)
            session.commit()
            # TODO: 封装
            join_msg = (
                f"{player.name} 加入游戏成功！\n"
                f"目前游戏人数为 {len(self.game_players)} 人。\n"
            )
            if len(self.game_players) < self.least_player_num:
                join_msg += f"最低游戏人数为 {self.least_player_num} 人。"
            elif len(self.game_players) == self.most_player_num:
                join_msg += "游戏人数已满，使用 start 命令开始游戏。"
            else:
                join_msg += "满足最低游戏人数，使用 start 命令开始游戏。"
            self._send_msg(join_msg)

    def play_game(self, player: Person, message: str, game_states: GameStates):
        try:
            self.play(player, message, game_states)
        except Exception:
            logger.error("游戏回合出现异常！")
        else:
            self.round += 1
            # 下一个玩家
            self.next_player()
            with make_db_session() as session:
                _game_states = (
                    session.query(DbGameStates).filter_by(id=game_states.id).first()
                )
                game_states.states = self.to_dict()
                _game_states.update(game_states)
                session.commit()

    def over_game(self, message: str, game_states: GameStates):
        self.over(message, game_states)
        with make_db_session() as session:
            _game_states = (
                session.query(DbGameStates).filter_by(id=game_states.id).first()
            )
            game_states.is_over = True
            _game_states.update(game_states)
            session.commit()
        logger.info("游戏结束！")
        self._send_msg("游戏结束！")

    @staticmethod
    def generate_raw_create_msg(title: str):
        """
        获取创建游戏的消息
        """
        create_msg = (
            f"=== {title} ===\n"
            "🕹️ 游戏开始！等待对手加入游戏...\n"
            "😃 使用 join 命令加入游戏。\n"
            "⛔ 使用 over 命令退出游戏。"
        )
        return create_msg

    def to_dict(self) -> Dict:
        """
        转换为字典
        """
        result = self.__dict__.copy()
        result["game_host_person"] = self.game_host_person.to_dict()
        game_players = UniqueList()
        for player in self.game_players:
            game_players.add(player.to_dict())
        result["game_players"] = game_players
        if self.is_group:
            result["game_host_group"] = self.game_host_group.to_dict()
        return result

    def _send_msg(self, message: str, type: str = "text"):
        """
        发送给游戏房间消息
        :param message: 消息内容
        :param type: 消息类型
        """
        print(self.sender_name)
        sender.send_msg(self.sender_name, message, type=type, is_group=self.is_group)

    def next_player(self):
        """
        下一个玩家
        """
        # 默认是列表顺序
        self.current_player_index = (self.current_player_index + 1) % len(
            self.game_players
        )

    @abstractmethod
    def fill_from_dict(cls, data: Dict):
        """
        从字典创建游戏实例
        """
        pass

    @abstractmethod
    def create(self):
        """
        创建游戏房间
        """
        pass

    @abstractmethod
    def start(self, game_states: GameStates):
        """
        开始游戏
        """
        pass

    @abstractmethod
    def join(self, player: Person, message: str, game_states: GameStates):
        """
        加入游戏
        """
        pass

    @abstractmethod
    def play(self, player: Person, message: str, game_states: GameStates):
        """
        进行一回合游戏
        """
        pass

    @abstractmethod
    def over(self, message: str, game_states: GameStates):
        """
        结束游戏
        """
        pass
