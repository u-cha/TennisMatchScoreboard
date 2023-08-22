from DBModels.dbmodels import Match
from Score import Score


class NewMatchService:
    @staticmethod
    def create_match(uuid, player1_name, player2_name, score=Score().serialize()) -> Match:
        new_match = Match(uuid=uuid, player1=player1_name, player2=player2_name, score=score)
        return new_match


