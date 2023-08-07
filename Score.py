import json
from random import randint


class Score:
    def __init__(self, score_dict=None):
        if score_dict:
            for key, value in score_dict.items():
                setattr(self, key, value)
            return
        self.server: int = self.__get_initial_server()
        self.game_score = [0, 0]
        self.set1_score = [0, 0]
        self.set2_score = [0, 0]
        self.set3_score = [0, 0]
        self.game_is_tie = False
        self.current_set = 1

    @staticmethod
    def __get_initial_server():
        return randint(1, 2)

    def json(self):
        return json.dumps(self.__dict__)

    def add_point(self, point_winner: 1 | 2):
        self.game_score[point_winner - 1] += 1
        if self.__game_is_over():
            setattr(self, f"set{self.current_set}_score", [1, 0])

    def __game_is_over(self):
        if self.game_is_tie:
            return False
        max_points = max(self.game_score)
        points_diff = max_points - min(self.game_score)
        if max_points >= 4 and points_diff >=2:
            return True
        return False

    def __set_is_over(self):


