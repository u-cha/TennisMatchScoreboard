from Match import Match
from MatchScorecard import MatchScorecard
from TieBreakScorecard import TieBreakScorecard


class MatchStatusUpdateService:

    def __init__(self, match: Match):
        self.__match = match

    @property
    def match(self):
        return self.__match

    def add_point(self, point_winner: int):
        self.match.add_point(point_winner)
        self.__update_match_status()

    def __update_match_status(self):
        match = self.match
        current_game = match.current_game
        if current_game.is_game_over():
            match.scorecard.current_game = ...

