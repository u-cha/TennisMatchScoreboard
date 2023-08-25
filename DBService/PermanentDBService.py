import sqlalchemy.exc
from sqlalchemy import create_engine, Connection
from sqlalchemy.orm import Session, Query
from sqlalchemy import select, insert, update, or_, and_
from DBModels.dbmodels import Base, Match, Player


class PermanentDBService:
    engine = create_engine('sqlite+pysqlite:///permanent.db', echo=True)

    @classmethod
    def __create_tables(cls):
        Base.metadata.create_all(cls.engine)

    @classmethod
    def persist(cls, obj):
        cls.__create_tables()
        with Connection(cls.engine) as connection:
            session = Session(connection)
            try:
                session.merge(obj)
                session.commit()
                return True
            except sqlalchemy.exc.IntegrityError as error:
                return False

    @classmethod
    def get_player_id_by_name(cls, name):
        cls.__create_tables()
        with Connection(cls.engine) as connection:
            session = Session(connection)
            stmt = select(Player.id).where(Player.name == name)
            result = session.execute(stmt)
            return result.fetchone()[0]

    @classmethod
    def get_match_by_uuid(cls, uuid):
        cls.__create_tables()
        with Connection(cls.engine) as connection:
            session = Session(connection)
            result = session.execute(select(Match).where(Match.uuid == uuid))
            return result.fetchall()

    @classmethod
    def get_matches(cls, **kwargs):
        cls.__create_tables()
        with Connection(cls.engine) as connection:
            session = Session(connection)
            stmt = select(Match).join(Player, or_(Player.id == Match.player1, Player.id == Match.player2))
            filter_by_player_name = kwargs['filter_by_player_name']
            if filter_by_player_name:
                stmt = stmt.filter(Player.name == filter_by_player_name)
            stmt = stmt.limit(kwargs["limit"]).offset(kwargs["offset"])
            result = session.execute(stmt)
            return result.fetchall()

    @classmethod
    def get_matches_count(cls):
        cls.__create_tables()
        with Connection(cls.engine) as connection:
            session = Session(connection)
            result = session.query(Match).count()
            return result

    @classmethod
    def delete_match(cls, match_uuid):
        pass

    @classmethod
    def delete_players(cls, match_uuid):
        pass

    @classmethod
    def update_player_ids(cls, match_uuid, permanent_ids_dict):
        cls.__create_tables()
        with Connection(cls.engine) as connection:
            session = Session(connection)
            stmt = update(Match).where(Match.uuid == match_uuid).values(
                player1=permanent_ids_dict["player1"], player2=permanent_ids_dict["player2"]
            )
            session.execute(stmt)
            session.commit()

    @classmethod
    def get_player_names_list(cls):
        cls.__create_tables()
        with Connection(cls.engine) as connection:
            session = Session(connection)
            player_names_list = [row[0] for row in
                                 session.execute(select(Player.name).order_by(Player.name.asc())).fetchall()]
        return player_names_list

    @classmethod
    def get_player_names(cls, player1_id, player2_id):
        cls.__create_tables()
        with Connection(cls.engine) as connection:
            session = Session(connection)
            player_ids = [player1_id, player2_id]
            stmt = select(Player.name).where(Player.id.in_(player_ids))
            result = session.execute(stmt)
            names_list = result.fetchall()
            names_dict = {"player1_name": names_list[0][0], "player2_name": names_list[1][0]}
            return names_dict
