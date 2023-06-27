from GameScorecard import GameScorecard
from TieBreakScorecard import TieBreakScorecard


class GameStatusUpdateService:
    def __init__(self, game_score_card: GameScorecard | TieBreakScorecard):
        self.__scorecard = game_score_card

    @property
    def scorecard(self):
        return self.__scorecard

    def update_game_status(self):
        scorecard = self.scorecard
        is_game_over = self.__check_if_game_over()
        if is_game_over:
            winner = self.__define_game_winner()
            scorecard.set_winner(winner)
            return
        if isinstance(scorecard, TieBreakScorecard):
            serves_played = self.__calculate_serves_played()
            if serves_played and serves_played % 2 == 0:
                self.__change_serving_player()

    def __change_serving_player(self):
        scorecard = self.scorecard
        if scorecard.serving_player == 1:
            scorecard.set_serving_player(2)
        else:
            scorecard.set_serving_player(1)

    def __check_if_game_over(self) -> bool:
        serves_played = self.__calculate_serves_played()
        points_difference = self.__calculate_points_difference()

        if isinstance(self.scorecard, GameScorecard):
            if serves_played >= 4 and abs(points_difference) >= 2:
                return True

        if isinstance(self.scorecard, TieBreakScorecard):
            if serves_played >= 7 and abs(points_difference) >= 2:
                return True

        return False

    def __define_game_winner(self):
        scorecard = self.scorecard
        serving_player = scorecard.serving_player
        points_difference = self.__calculate_points_difference()

        if points_difference > 0:
            return serving_player
        else:
            return 3 - serving_player

    def __calculate_points_difference(self) -> int:
        score = self.scorecard.score
        serving_player = self.__get_serving_player()
        serves_played = self.__calculate_serves_played()
        points_won_by_server = score[serving_player]
        points_won_by_opponent = serves_played - points_won_by_server
        points_difference = points_won_by_server - points_won_by_opponent
        return points_difference

    def __calculate_serves_played(self) -> int:
        scorecard = self.scorecard
        serves_played = sum(scorecard.score.values())
        return serves_played

    def __get_serving_player(self) -> int:
        scorecard = self.scorecard
        serving_player = scorecard.serving_player
        return serving_player
