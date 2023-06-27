import typing
from random import randint
from SetScorecard import SetScorecard
from GameScorecard import GameScorecard
from TieBreakScorecard import TieBreakScorecard


class MatchScorecard:
    def __init__(self):

        self.__this_match_score = {1: 0, 2: 0}
        self.__current_set_scorecard = SetScorecard()
        self.__current_game_scorecard = GameScorecard(randint(1, 2))
        self.__winner = None

    def add_point(self, point_winner: int) -> int:
        self.__current_game_scorecard.add_point(point_winner)

    def renew_current_game(self, game_type: GameScorecard | TieBreakScorecard, server_number: int) -> None:
        if not self.current_game_scorecard.is_over:
            raise SyntaxError("cannot renew game. previous game is not over")
        self.__current_game_scorecard = game_type(server_number)

    def renew_current_set(self) -> None:
        if not self.__current_set_scorecard.is_set_over:
            raise SyntaxError("cannot renew game. previous game is not over")
        self.__current_set_scorecard = SetScorecard()

    @property
    def current_game_scorecard(self):
        return self.__current_game_scorecard

    @property
    def current_set_scorecard(self):
        return self.__current_set_scorecard

