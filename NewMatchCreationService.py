from DBModels.dbmodels import Match
from Scores.Score import Score
from UUIDEmissionService import UUIDEmissionService


class NewMatchService:
    @classmethod
    def create_match(cls, player1_name, player2_name) -> Match:
        uuid = cls.__get_new_uuid()
        score = Score().serialize()
        new_match = Match(uuid=uuid, player1=player1_name, player2=player2_name, score=score)
        return new_match

    @staticmethod
    def __get_new_uuid():
        return UUIDEmissionService.emit_uuid()
