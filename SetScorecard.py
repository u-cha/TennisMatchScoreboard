from GameScorecard import GameScorecard


class SetScorecard:
    def __init__(self):
        self.__this_set_score = {1: 0, 2: 0}
        self.__winner = None

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

