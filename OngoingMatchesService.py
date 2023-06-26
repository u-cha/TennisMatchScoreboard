from Match import Match
from uuid import uuid4


class OngoingMatchesService:
    def __init__(self):
        self.__ongoing_matches_map = {}

    def create_match(self, player1_name, player2_name) -> None:
        match_uuid = uuid4().hex
        new_match = Match(player1_name, player2_name)
        self.__ongoing_matches_map[match_uuid] = new_match

    def get_match_by_uuid(self, match_uuid: str) -> Match:
        return self.__ongoing_matches_map[match_uuid]

    @property
    def ongoing_matches(self) -> dict:
        return self.__ongoing_matches_map


if __name__ == '__main__':
    service = OngoingMatchesService()
    service.create_match('Bob', 'Sim')
    service.create_match('Bob', 'Sim')
    print(service.ongoing_matches)
