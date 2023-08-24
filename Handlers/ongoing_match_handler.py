from Handlers.handler import Handler
from View import View
from DBService import DBService, InMemoryDBService, PermanentDBService
from urllib.parse import parse_qs, urlparse
from ScoreUpdateService import ScoreUpdateService
from Score import ScoreSchema


class OngoingMatchHandler(Handler):
    def perform_get(self):
        match = self.__retrieve_match_from_db()
        match_params = ScoreUpdateService.show_match_params(match)
        player_names = self.__get_player_names(match.player1, match.player2, InMemoryDBService)
        body = View.render("match_score", **match_params, **player_names)
        self.response.body = body

    def perform_post(self):
        match = self.__retrieve_match_from_db()
        point_winner = self.__retrieve_point_winner()
        match = ScoreUpdateService.update(match, point_winner)
        player_names_dict = self.__get_player_names(match.player1, match.player2, InMemoryDBService)
        score = ScoreSchema().loads(match.score)
        if score.match_is_over:
            match.winner = score.match_winner
            self.__persist_match(match, PermanentDBService)
            permanent_ids_dict = self.__get_ids_by_names(player_names_dict, PermanentDBService)
            match_uuid = self.__get_uuid_from_query_string()
            self.__update_ids(match_uuid, permanent_ids_dict, PermanentDBService)
            self.__delete_players(match_uuid, InMemoryDBService)
            self.__delete_match(match_uuid, InMemoryDBService)

        else:
            self.__persist_match(match, InMemoryDBService)
        match_params = ScoreUpdateService.show_match_params(match)
        body = View.render("match_score", **match_params, **player_names_dict)
        self.response.body = body

    def __get_uuid_from_query_string(self):
        query_string = self.environ.get("QUERY_STRING", "")
        parsed_query_string = parse_qs(query_string)
        uuid = parsed_query_string["uuid"][0]
        return uuid

    def __retrieve_match_from_db(self):
        uuid = self.__get_uuid_from_query_string()
        db_service = DBService(InMemoryDBService)
        match = db_service.get_match_by_uuid(uuid)
        return match

    def __retrieve_point_winner(self):
        request_body = self.environ.get('wsgi.input').read().decode()
        parsed_request_body = parse_qs(request_body)
        if parsed_request_body.get("player1", None):
            return 1
        else:
            return 2

    @staticmethod
    def __persist_match(match, db_service):
        DBService(db_service).persist(match)

    @staticmethod
    def __delete_match(match_uuid, db_service):
        DBService(db_service).delete_match(match_uuid)

    @staticmethod
    def __delete_players(match_uuid, db_service):
        DBService(db_service).delete_players(match_uuid)

    @staticmethod
    def __get_player_names(player1_id, player2_id, db_service):
        return DBService(db_service).get_player_names(player1_id, player2_id)

    @staticmethod
    def __get_ids_by_names(player_names_dict, db_service):
        result = []
        player_names = [player_names_dict["player1_name"], player_names_dict["player2_name"]]
        for player_name in player_names:
            id_ = DBService(db_service).get_player_id_by_name(player_name)
            result.append(id_)
        return {"player1": result[0], "player2": result[1]}

    def __update_ids(self, match_uuid, permanent_ids_dict, db_service):
        DBService(db_service).update_ids(match_uuid, permanent_ids_dict)


