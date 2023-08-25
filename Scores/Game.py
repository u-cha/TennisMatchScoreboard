import json
from marshmallow import Schema, fields, post_load


class Game:
    def __init__(self, p1_points=0, p2_points=0, is_tie=False, is_over=False, winner=None, **kwargs):
        self.p1_points = p1_points
        self.p2_points = p2_points
        self.is_tie = is_tie
        self.is_over = is_over
        self.winner = winner

    def __str__(self):
        return json.dumps(self.__dict__, default=str)

    def add_point(self, points_winner):
        if self.is_over:
            return False
        player_points = getattr(self, f"p{points_winner}_points")
        setattr(self, f"p{points_winner}_points", player_points + 1)
        self.is_over = self.__is_game_over()
        if self.is_over:
            self.__fix_winner()
        return True

    def __is_game_over(self):
        if self.is_tie:
            min_points_to_win = 7
        else:
            min_points_to_win = 4
        max_won_points = max(self.p1_points, self.p2_points)
        points_diff = max_won_points - min(self.p1_points, self.p2_points)
        if max_won_points >= min_points_to_win and points_diff >= 2:
            return True
        return False

    def __fix_winner(self):
        if self.p1_points > self.p2_points:
            self.winner = 1
        else:
            self.winner = 2


class GameSchema(Schema):
    p1_points = fields.Int(required=True)
    p2_points = fields.Int(required=True)
    is_tie = fields.Bool(required=True)
    is_over = fields.Bool(required=True)
    winner = fields.Int(required=True, allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Game(**data)
