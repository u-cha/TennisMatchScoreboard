class GameScoreCalculationInterface:

    def __update_score(self, scorecard, point_winner: int):
        scorecard[point_winner] += 1

    def __check_is_over(self):
        pass

    def __change_server(self):
        pass

    def __update_winner(self):
        pass


