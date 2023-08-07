import json
from Score import Score


class ScoreUpdateService:
    @classmethod
    def update(cls, match, point_winner=0):
        if point_winner == 0:
            return match
        score = cls.__retrieve_score(match)
        score.add_point(point_winner)
        match.score = score.json()
        return match

    @staticmethod
    def __retrieve_match_params(match):
        score_dict = json.loads(match.score)
        uuid = match.uuid
        match_params = dict(score_dict.items(), uuid=uuid, player1=match.player1, player2=match.player2)
        return match_params

    @staticmethod
    def __retrieve_score(match):
        score_dict = json.loads(match.score)
        score = Score(score_dict)
        return score

    @classmethod
    def show_match_params(cls, match):
        return cls.__retrieve_match_params(match)
