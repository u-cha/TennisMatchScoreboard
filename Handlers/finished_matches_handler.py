from Handlers.handler import Handler
from View import View
from DBService import DBService, InMemoryDBService, PermanentDBService
from urllib.parse import parse_qs, urlparse
from ScoreUpdateService import ScoreUpdateService
import json
from Score import Score, ScoreSchema


class FinishedMatchesHandler(Handler):
    def perform_get(self):
        matches_count = self.__get_matches_count_from_db()
        num_rows = self.__retrieve_num_rows()
        page_number = self.__retrieve_page_number()
        records = self.__retrieve_matches_from_db(limit=num_rows, offset=num_rows * (page_number - 1))


        output = []
        for record in records:
            match = record[0]
            score = ScoreSchema().loads(match.score)
            player1 = match.player1
            player2 = match.player2
            winner = match.winner
            try:
                set1_results = f"{score.sets[0].p1_points}:{score.sets[0].p2_points}"
            except:
                set1_results = "---"
            try:
                set2_results = f"{score.sets[1].p1_points}:{score.sets[1].p2_points}"
            except:
                set2_results = "---"
            try:
                set3_results = f"{score.sets[2].p1_points}:{score.sets[2].p2_points}"
            except:
                set3_results = "---"

            output.append(dict(player1=player1, player2=player2, winner=winner,
                               set1_results=set1_results, set2_results=set2_results, set3_results=set3_results))

        body = View.render("finished_matches", output=output)
        self.response.body = body

    def perform_post(self):
        pass

    def __retrieve_matches_from_db(self, **kwargs):
        db_service = DBService(PermanentDBService)
        matches_list = db_service.get_matches(**kwargs)
        return matches_list

    def __retrieve_num_rows(self):
        query_string = self.environ.get('QUERY_STRING', None)
        if query_string:
            parsed_query_string = parse_qs(query_string)
            num_rows = int(parsed_query_string["num_rows"][0])
        else:
            num_rows = 10
        return num_rows

    def __get_matches_count_from_db(self):
        db_service = DBService(PermanentDBService)
        matches_count = db_service.get_matches_count()
        return matches_count

    def __retrieve_page_number(self):
        query_string = self.environ.get('QUERY_STRING', None)
        if query_string:
            parsed_query_string = parse_qs(query_string)
            page_number_str = parsed_query_string.get("page", None)
            if page_number_str:
                page_number = int(page_number_str[0])
                return page_number

        page_number = 1
        return page_number
