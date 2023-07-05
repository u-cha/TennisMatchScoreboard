import typing
from random import randint
from ScoreCalculationInterface import ScoreCalculationInterface
from SetScorecard import SetScorecard
from GameScorecard import GameScorecard
from TieBreakScorecard import TieBreakScorecard


class MatchScorecard(ScoreCalculationInterface):
    def __init__(self):
        self.__interface = ScoreCalculationInterface()
        self.__this_match_score = []
        serving_player = self.__determine_serving_player()
        new_set = self.__current_set_scorecard = SetScorecard(serving_player)
        self.__this_match_score.append(new_set)



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

    def __determine_serving_player(self) -> int:
        if len(self.__this_match_score) == 0:
            serving_player = randint(1, 2)
        else:
            serving_player = 3 - self.__this_match_score[-1].current_server
        return serving_player

