import json

from marshmallow import Schema, fields, post_load


class Set:
    def __init__(self, p1_points=0, p2_points=0, is_over=False, needs_tie=False, winner=None, **kwargs):
        self.p1_points = p1_points
        self.p2_points = p2_points
        self.is_over = is_over
        self.needs_tie = needs_tie
        self.winner = winner

    def __str__(self):
        return json.dumps(self.__dict__, default=str)

    def add_point(self, points_winner):
        if self.is_over:
            return False
        player_points = getattr(self, f"p{points_winner}_points")
        setattr(self, f"p{points_winner}_points", player_points + 1)
        self.needs_tie = self.__does_need_tie()
        self.is_over = self.__is_set_over()
        if self.is_over:
            self.__fix_winner()
        return True

    def __does_need_tie(self):
        if self.needs_tie:
            return True
        if self.p1_points == 6 and self.p2_points == 6:
            return True
        return False

    def __is_set_over(self):
        min_points_to_win = 6
        max_won_points = max(self.p1_points, self.p2_points)
        points_diff = max_won_points - min(self.p1_points, self.p2_points)
        if self.needs_tie and points_diff > 0:
            return True
        if max_won_points >= min_points_to_win and points_diff >= 2:
            return True
        return False

    def __fix_winner(self):
        if self.p1_points > self.p2_points:
            self.winner = 1
        else:
            self.winner = 2


class SetSchema(Schema):
    p1_points = fields.Int(required=True)
    p2_points = fields.Int(required=True)
    is_over = fields.Bool(required=True)
    winner = fields.Int(required=True, allow_none=True)
    needs_tie = fields.Bool(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Set(**data)
