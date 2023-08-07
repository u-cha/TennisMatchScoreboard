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
