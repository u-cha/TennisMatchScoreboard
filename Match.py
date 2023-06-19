from Player import Player
from MatchScore import MatchScore


class Match:
    def __init__(self, uuid: str, player1_name: str, player2_name: str):
        self.__uuid = uuid
        self.__player1 = Player(player1_name)
        self.__player2 = Player(player2_name)
        self.__score = MatchScore()
        self.__winner = None





