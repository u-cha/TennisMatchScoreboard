from GameScorecard import GameScorecard


class TieBreakScorecard(GameScorecard):
    def __init__(self, serving_player: int):
        super().__init__(serving_player)

    def set_serving_player(self, player_number):
        self.__serving_player = player_number

