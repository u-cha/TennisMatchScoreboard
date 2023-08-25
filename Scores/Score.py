from random import randint

from Scores.Game import Game, GameSchema
from Scores.Set import Set, SetSchema
from marshmallow import Schema, fields, ValidationError, post_load


def validate_server(server):
    if not isinstance(server, int) or server not in (1, 2):
        raise ValidationError


class ScoreSchema(Schema):
    server = fields.Int(required=True, validate=validate_server)
    current_game = fields.Nested(GameSchema, required=True)
    sets = fields.Nested(SetSchema, many=True, required=True)
    match_is_over = fields.Boolean(required=True)
    num_sets = fields.Integer(required=True)
    match_winner = fields.Integer(required=True, allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Score(**data)


class Score:
    def __init__(self, server=None, current_game=None, sets=None, match_is_over=False, match_winner=None, **kwargs):
        if server is None:
            self.server = self.__get_initial_server()
        else:
            self.server = server
        if current_game is None:
            self.current_game = Game()
        else:
            self.current_game = current_game
        if sets is None:
            self.sets = [Set()]
        else:
            self.sets = sets
        self.match_is_over = match_is_over
        self.num_sets = len(self.sets)
        self.match_winner = match_winner

    @staticmethod
    def __get_initial_server():
        return randint(1, 2)

    def serialize(self):
        schema = ScoreSchema()
        return schema.dumps(self)
