from Handlers.handler import Handler
from View import View
from DBService import DBService, InMemoryDBService, PermanentDBService
from urllib.parse import parse_qs, urlparse
from ScoreUpdateService import ScoreUpdateService
import json


class FinishedMatchesHandler(Handler):
    def perform_get(self):
        match = self.__retrieve_matches_from_db()
        match_params = ScoreUpdateService.show_match_params(match)
        body = View.render("match_score", **match_params)
        self.response.body = body

    def perform_post(self):
        pass


    def __retrieve_matches_from_db(self):
        db_service = DBService(PermanentDBService)
        matches_list = db_service.get_all_matches()
        return matches_list


