import re
import shutil
from typing import Dict

from loguru import logger
from PIL import Image
from typing_extensions import override

from wechatter.games.game import Game
from wechatter.utils import get_abs_path


class Tictactoe(Game):
    """
    井字棋游戏
    """

    name = "tictactoe"
    desc = "井字棋游戏"
    keys = ["tictactoe", "井字棋", "ttt"]

    # 文件路径
    initial_board_image_path = get_abs_path("assets/games/tictactoe/board.png")
    gaming_board_image_path = get_abs_path("assets/games/tictactoe/gaming_board.png")
    piece_x_image_path = get_abs_path("assets/games/tictactoe/piece_x.png")
    piece_o_image_path = get_abs_path("assets/games/tictactoe/piece_o.png")

    def __init__(
        self,
        game_host_person,
        game_players,
        game_host_group=None,
        least_player_num: int = 2,
        most_player_num: int = 2,
    ):
        super().__init__(
            game_host_person=game_host_person,
            game_players=game_players,
            game_host_group=game_host_group,
            least_player_num=least_player_num,
            most_player_num=most_player_num,
        )
        # 0表示空位，1表示玩家1（O），2表示玩家2（X）
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    @override
    def fill_from_dict(self, data: Dict):
        self.board = data["board"]

    @override
    def create(self):
        create_msg = self.generate_raw_create_msg("井字棋游戏")
        self._send_msg(create_msg)

    @override
    def start(self, game_states):
        # 保存初始棋盘到游戏棋盘
        shutil.copy(self.initial_board_image_path, self.gaming_board_image_path)
        self._send_msg(self.initial_board_image_path, type="localfile")

    @override
    def join(self, player, message, game_states):
        pass

    @override
    def play(self, player, message, game_states):
        # 检测message是否符合 x,y 或者 x y 的格式
        # TODO: 多分割符写成工具函数
        split_list = re.split(r"[\s,]+", message)
        if len(split_list) != 2:
            logger.info("⚠️ 请按照 x,y 或者 x y 的格式输入坐标！")
            self._send_msg("⚠️ 请按照 x,y 或者 x y 的格式输入坐标！")
            raise ValueError

        if self.current_player_index != self.game_players.index(player):
            logger.info(
                f"⚠️ 不是你的回合，当前回合玩家为 {self.game_players[self.current_player_index].name}！"
            )
            self._send_msg(
                f"⚠️ 不是你的回合，当前回合玩家为 {self.game_players[self.current_player_index].name}！"
            )
            raise ValueError
        x, y = split_list
        if not x.isdigit() or not y.isdigit():
            logger.info("⚠️ 请输入有效的坐标！")
            self._send_msg("⚠️ 请输入有效的坐标！")
            raise ValueError
        x, y = int(x) - 1, int(y) - 1
        if not (0 <= x < 3 and 0 <= y < 3):
            logger.info("⚠️ 坐标超出范围！")
            self._send_msg("⚠️ 坐标超出范围！")
            raise ValueError
        if self.board[x][y] != 0:
            logger.info("⚠️ 该位置已经有棋子了！")
            self._send_msg("⚠️ 该位置已经有棋子了！")
            raise ValueError

        # 玩家1为 O
        if self.current_player_index == 0:
            self.board[x][y] = 1
            self.gaming_board_image_path = self.__draw_board(
                self.gaming_board_image_path, x, y
            )
        # 玩家2为 X
        elif self.current_player_index == 1:
            self.board[x][y] = 2
            self.gaming_board_image_path = self.__draw_board(
                self.gaming_board_image_path, x, y
            )
        else:
            logger.error("玩家索引错误！")
            raise ValueError("玩家索引错误！")
        self._send_msg(self.gaming_board_image_path, type="localfile")

        # 判断胜利
        winner = self.__judge_winner()
        if winner == 1:
            self._send_msg(f"🎉 玩家1 {self.game_players[0].name} 胜利！")
            self.over_game(message="", game_states=game_states)
        elif winner == 2:
            self._send_msg(f"🎉 玩家2 {self.game_players[1].name} 胜利！")
            self.over_game(message="", game_states=game_states)
        elif winner == 0:
            self._send_msg("🤝 平局！")
            self.over_game(message="", game_states=game_states)

    @override
    def over(self, message, game_states):
        self._send_msg(message)

    def __judge_winner(self):
        """
        判断胜利
        """
        # 判断横向
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
                return self.board[i][0]
        # 判断纵向
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
                return self.board[0][i]
        # 判断对角线
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return self.board[0][2]
        # 判断平局
        if all([i != 0 for row in self.board for i in row]):
            return 0
        return None

    def __draw_board(
        self, gaming_board_image_path: str = None, i: int = None, j: int = None
    ):
        """
        绘制棋盘
        """
        board_image = Image.open(gaming_board_image_path)
        if self.board[i][j] == 1:
            piece_image = Image.open(self.piece_o_image_path).convert("RGBA")
        elif self.board[i][j] == 2:
            piece_image = Image.open(self.piece_x_image_path).convert("RGBA")
        else:
            logger.error("棋子索引错误！")
            raise ValueError("棋子索引错误！")
        board_image.paste(piece_image, (j * 130 + 60, i * 130 + 90), mask=piece_image)
        board_image.save(self.gaming_board_image_path)
        return self.gaming_board_image_path
