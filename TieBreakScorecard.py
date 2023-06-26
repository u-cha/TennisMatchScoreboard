from GameScorecard import GameScorecard


class TieBreakScorecard(GameScorecard):
    def __init__(self, serving_player: int):
        super().__init__(serving_player)
        self.__serve_counter = 0



