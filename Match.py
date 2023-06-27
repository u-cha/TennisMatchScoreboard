from typing import Tuple
from Player import Player
from MatchScorecard import MatchScorecard


class Match:
    def __init__(self, player1_name: str, player2_name: str):
        self.__player1 = Player(player1_name)
        self.__player2 = Player(player2_name)
        self.__scorecard = MatchScorecard()
        self.__current_game = self.__scorecard.current_game_scorecard
        self.__current_set = self.__scorecard.current_set_scorecard
        self.__winner = None

    def add_point(self, point_winner: int):
        self.__scorecard.add_point(point_winner)

    @property
    def players(self) -> Tuple[str, str]:
        return self.__player1.name, self.__player2.name

    @property
    def scorecard(self):
        return self.__scorecard

    @property
    def winner(self):
        return self.__winner

    def is_over(self):
        return bool(self.winner)

    @property
    def current_game(self):
        return self.__current_game

    @property
    def current_set(self):
        return self.__current_set


