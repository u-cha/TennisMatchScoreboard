from Match import Match
from uuid import uuid4


class OngoingMatchesService:
    def __init__(self):
        self.ongoing_matches_list = []

    def create_match(self, player1_name, player2_name) -> None:
        match_uuid = uuid4().hex
        new_match = Match(match_uuid, player1_name, player2_name)
        self.ongoing_matches_list.append(new_match)


if __name__ == '__main__':
    service = OngoingMatchesService()
    service.create_match('Bob', 'Sim')
    service.create_match('Bob', 'Sim')
    print(service.ongoing_matches_list)




