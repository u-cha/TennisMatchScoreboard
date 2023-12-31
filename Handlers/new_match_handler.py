from urllib.parse import parse_qs
from Handlers.handler import Handler
from View import View
from NewMatchCreationService import NewMatchService
from DBService import DBService, InMemoryDBService, PermanentDBService
from DBModels.dbmodels import Player


class NewMatchHandler(Handler):
    def perform_get(self):
        body = View.render("new_match")
        self.response.body = body

    def perform_post(self):
        player1_name, player2_name = self.__retrieve_player_names_from_request()
        player_persistence_result = self.__persist_players(player1_name, player2_name)
        if player_persistence_result is False:
            body = View.render("busy_player")
            self.response.body = body
            self.response.status = "400"
            return
        match = self.__get_new_match(player1_name, player2_name)
        self.__persist_match(match)
        self.response.status = "301 Redirect"
        self.response.headers = [("Location", f"/match-score?uuid={match.uuid}")]

    def __get_new_match(self, player1_name, player2_name):
        temp_player1_id, temp_player2_id = self.__get_temporary_player_ids(player1_name, player2_name)
        return NewMatchService.create_match(temp_player1_id, temp_player2_id)

    @staticmethod
    def __persist_match(match):
        DBService(InMemoryDBService).persist(match)

    def __get_temporary_player_ids(self, player1_name, player2_name):
        db_service = DBService(InMemoryDBService)
        temp_player1_id = db_service.get_player_id_by_name(player1_name)
        temp_player2_id = db_service.get_player_id_by_name(player2_name)
        return temp_player1_id, temp_player2_id

    def __retrieve_player_names_from_request(self):
        request_body = self.environ.get('wsgi.input').read().decode()
        parsed_request_body = parse_qs(request_body)
        player1_name = parsed_request_body["player1"][0]
        player2_name = parsed_request_body["player2"][0]
        return player1_name, player2_name

    def __persist_players(self, player1_name, player2_name):
        self.__persist_player_names_permanently(player1_name, player2_name)
        return self.__persist_player_names_temporarily(player1_name, player2_name)

    @staticmethod
    def __persist_player_names_permanently(player1_name, player2_name):
        db_service = DBService(PermanentDBService)
        db_service.persist(Player(name=player1_name))
        db_service.persist(Player(name=player2_name))

    @staticmethod
    def __persist_player_names_temporarily(player1_name, player2_name):
        db_service = DBService(InMemoryDBService)
        if db_service.persist(Player(name=player1_name)) is False:
            return False
        if db_service.persist(Player(name=player2_name)) is False:
            db_service.remove(Player(name=player1_name))
            return False
        return True
