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
        body = View.render("match_score", **match_params)
        self.response.body = body

    def perform_post(self):
        match = self.__retrieve_match_from_db()
        point_winner = self.__retrieve_point_winner()
        match = ScoreUpdateService.update(match, point_winner)
        score = ScoreSchema().loads(match.score)
        if score.match_is_over:
            match.winner = score.match_winner
            self.__persist_match(match, PermanentDBService)
            match_uuid = self.__get_uuid_from_query_string()
            self.__delete_match(match_uuid, InMemoryDBService)
            self.__delete_players(match_uuid, InMemoryDBService)
        else:
            self.__persist_match(match, InMemoryDBService)
        match_params = ScoreUpdateService.show_match_params(match)
        body = View.render("match_score", **match_params)
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
