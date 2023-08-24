import json
from Score import Score, ScoreSchema
from Game import Game
from Set import Set


class ScoreUpdateService:
    @classmethod
    def update(cls, match, point_winner=0):
        if point_winner == 0:
            return match
        score = cls.__retrieve_score(match)
        score = cls.add_point(score, point_winner)
        match.score = score.serialize()
        return match

    @classmethod
    def add_point(cls, score, point_winner):
        if score.match_is_over:
            return score
        current_game = score.current_game
        current_set = score.sets[-1]
        current_game.add_point(point_winner)
        if current_game.is_tie and (current_game.p1_points + current_game.p2_points) % 2 != 0:
            score.server = 3 - score.server
        if current_game.is_over:
            score.server = 3 - score.server
            current_set.add_point(current_game.winner)
            score.match_is_over = cls.__is_match_over(score)
            if not score.match_is_over:
                if current_set.is_over:
                    score.sets.append(Set())
                if current_set.needs_tie and not current_set.is_over:
                    score.current_game = Game(is_tie=True)
                else:
                    score.current_game = Game()
            else:
                score.match_winner = cls.__fix_match_winner(score)

        return score

    @staticmethod
    def __is_match_over(score):
        match_is_over = bool(len(score.sets) == 3 and score.sets[-1].is_over
                             or len(score.sets) == 2 and score.sets[0].winner == score.sets[1].winner)
        return match_is_over

    @staticmethod
    def __is_current_set_over(score):
        return score.sets[-1].is_over

    @staticmethod
    def __retrieve_match_params(match):
        score_dict = json.loads(match.score)
        uuid = match.uuid
        match_params = dict(score_dict.items(), uuid=uuid, player1=match.player1, player2=match.player2)
        return match_params

    @staticmethod
    def __retrieve_score(match):
        schema = ScoreSchema()
        score = schema.loads(match.score)
        return score

    @classmethod
    def show_match_params(cls, match):
        return cls.__retrieve_match_params(match)

    @classmethod
    def __fix_match_winner(cls, score):
        p1_won_sets = 0
        p2_won_sets = 0
        for set_ in score.sets:
            if set_.winner == 1:
                p1_won_sets += 1
            else:
                p2_won_sets += 1
        if p1_won_sets > p2_won_sets:
            match_winner = 1
        else:
            match_winner = 2
        return match_winner
