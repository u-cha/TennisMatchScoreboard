class GameScorecard:
    def __init__(self, serving_player: int):
        self.__serving_player = serving_player
        self.__score = {1: 0, 2: 0}
        self.__winner = None

    def add_point(self, point_winner: int):
        self.__score[point_winner] += 1

    @property
    def serving_player(self) -> int:
        return self.__serving_player

    def set_serving_player(self, player_number):
        pass

    @property
    def winner(self) -> int | None:
        return self.__winner

    def set_winner(self, winner: int):
        self.__winner = winner

    @property
    def is_over(self) -> bool:
        return bool(self.winner)

    @property
    def score(self) -> dict:
        return self.__score
