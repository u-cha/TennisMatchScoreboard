from GameScorecard import GameScorecard
from TieBreakScorecard import TieBreakScorecard


class GameStatusUpdateService:
    def __init__(self, game_score_card: GameScorecard | TieBreakScorecard):
        self.__scorecard = game_score_card

    @property
    def scorecard(self):
        return self.__scorecard

    def update_winner(self) -> None:
        scorecard = self.scorecard
        serving_player = scorecard.serving_player
        serves_played = sum(scorecard.score.values())
        won_by_server = scorecard.score[serving_player]
        won_by_opponent = serves_played - won_by_server
        points_difference = won_by_server - won_by_opponent

        if isinstance(scorecard, GameScorecard):
            if serves_played >= 4 and abs(points_difference) >= 2:
                if points_difference > 0:
                    scorecard.set_winner(serving_player)
                else:
                    scorecard.set_winner(3 - serving_player)

        if isinstance(scorecard, TieBreakScorecard):
            if serves_played >= 7 and abs(points_difference) >= 2:
                if points_difference > 0:
                    scorecard.set_winner(serving_player)
                else:
                    scorecard.set_winner(3 - serving_player)

            if serves_played % 4 in (0, 3):
                self.change_serving_player()

    def change_serving_player(self):
        scorecard = self.scorecard
        if scorecard.serving_player == 1:
            scorecard.set_serving_player(2)
        else:
            scorecard.set_serving_player(1)
