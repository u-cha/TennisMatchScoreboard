from random import randint
from SetScorecard import SetScorecard
from GameScorecard import GameScorecard


class MatchScorecard:
    def __init__(self):

        self.__this_match_score = {1: 0, 2: 0}
        self.__current_set_score = {1: 0, 2: 0}
        self.__current_game = GameScorecard(randint(1, 2))
        self.__winner = None

    def add_point(self, point_winner: int):
        self.__current_game.add_point(point_winner)

    def add_game_to_score(self):


    @property
    def current_game(self):
        return self.__current_game



