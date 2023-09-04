class GameScoreTranslator:
    game_points = {0: 0,
                   1: 15,
                   2: 30,
                   3: 40}

    @classmethod
    def translate(cls, game_score_dict):
        if game_score_dict["is_tie"]:
            return game_score_dict
        p1_points = game_score_dict["p1_points"]
        p2_points = game_score_dict["p2_points"]
        if p1_points < 4 and p2_points < 4:
            game_score_dict["p1_points"] = cls.game_points[p1_points]
            game_score_dict["p2_points"] = cls.game_points[p2_points]
        else:
            if p1_points == p2_points:
                game_score_dict["p1_points"] = game_score_dict["p2_points"] = cls.game_points[3]
            elif p1_points < p2_points:
                game_score_dict["p1_points"] = ""
                game_score_dict["p2_points"] = "A"
            else:
                game_score_dict["p1_points"] = "A"
                game_score_dict["p2_points"] = ""
        return game_score_dict
