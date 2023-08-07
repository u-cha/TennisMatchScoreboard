from Handlers.handler import Handler
from View import View
from DBService import DBService, InMemoryDBService, PermanentDBService
from urllib.parse import parse_qs, urlparse
from ScoreUpdateService import ScoreUpdateService
import json


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
        self.__persist_match(match)
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
        return 2

    @staticmethod
    def __persist_match(match):
        DBService(InMemoryDBService).persist(match)
