from ScoreCalculationInterface import SetScoreCalculationInterface
from GameScorecard import GameScorecard


class SetScorecard:
    def __init__(self, serving_player: int):
        self.__this_set_score = {1: 0, 2: 0}
        self.__current_server = serving_player
        self.__current_game = GameScorecard(serving_player)
        self.__winner = None
        self.__interface = SetScoreCalculationInterface()

    @property
    def current_server(self):
        return self.__current_server

    @property
    def winner(self) -> int | None:
        return self.__winner

    def set_winner(self, winner: int):
        self.__winner = winner

    @property
    def is_set_over(self) -> bool:
        return bool(self.winner)

    def add_point(self, point_winner: int):
        self.__this_set_score[point_winner] += 1
