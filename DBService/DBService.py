from DBModels.dbmodels import Match, Player


class DBService:

    def __init__(self, service):
        self.service = service

    def persist(self, obj):
        return self.service.persist(obj)

    def get_player_id(self, name):
        self.service.get_player_id(name)

    def get_match_by_uuid(self, uuid):
        return self.service.get_match_by_uuid(uuid)

    def get_player_id_by_name(self, name):
        return self.service.get_player_id_by_name(name)

    def remove(self, obj):
        self.service.remove(obj)

    def get_all_matches(self):
        pass

    def delete_match(self, match_uuid):
        return self.service.delete_match(match_uuid)

    def delete_players(self, match_uuid):
        return self.service.delete_players(match_uuid)

