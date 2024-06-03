import sqlalchemy.exc
from sqlalchemy import create_engine, Connection
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete, union
from TennisMatchScoreboard.DBModels import Base, Match, Player
from TennisMatchScoreboard.exceptions import MatchNotFoundByUUID


class InMemoryDBService:
    engine = create_engine("sqlite+pysqlite:///:memory:",
                           connect_args={"check_same_thread": False},
                           poolclass=StaticPool, echo=True)

    connection = None

    @classmethod
    def __get_session(cls):
        cls.__establish_connection()
        cls.__create_tables()
        return Session(cls.connection, expire_on_commit=False)

    @classmethod
    def __establish_connection(cls):
        if cls.connection is None:
            cls.connection = Connection(cls.engine)

    @classmethod
    def __create_tables(cls):
        Base.metadata.create_all(cls.engine)

    @classmethod
    def persist(cls, obj):
        with cls.__get_session() as session:
            try:
                session.add(obj)
                session.commit()
                return True
            except sqlalchemy.exc.IntegrityError as error:
                return False

    @classmethod
    def remove(cls, obj):
        with cls.__get_session() as session:
            session.delete(obj)
            session.commit()

    @classmethod
    def get_player_id_by_name(cls, name):
        with cls.__get_session() as session:
            stmt = select(Player.id).where(Player.name == name)
            result = session.execute(stmt)
            return result.fetchone()[0]

    @classmethod
    def get_match_by_uuid(cls, uuid):
        with cls.__get_session() as session:
            try:
                stmt = select(Match).where(Match.uuid == uuid)
                result = session.execute(stmt)
                return result.fetchone()[0]
            except TypeError:
                raise MatchNotFoundByUUID("no ongoing matches with this uuid. perhaps, this match is over.")

    @classmethod
    def update_match_score(cls, uuid, new_score):
        with cls.__get_session() as session:
            stmt = update(Match).where(Match.uuid == uuid).values(score=new_score)
            session.execute(stmt)
            session.commit()

    @classmethod
    def delete_match(cls, match_uuid):
        with cls.__get_session() as session:
            stmt = delete(Match).where(Match.uuid == match_uuid)
            session.execute(stmt)
            session.commit()

    @classmethod
    def delete_players(cls, match_uuid):
        with cls.__get_session() as session:
            select1 = select(Match.player1).where(Match.uuid == match_uuid)
            select2 = select(Match.player2).where(Match.uuid == match_uuid)
            player_ids = union(select1, select2)
            stmt = delete(Player).where(Player.id.in_(player_ids))
            session.execute(stmt)
            session.commit()

    @classmethod
    def get_player_names(cls, player1_id, player2_id):
        with cls.__get_session() as session:
            player_ids = [player1_id, player2_id]
            stmt = select(Player.name).where(Player.id.in_(player_ids))
            result = session.execute(stmt)
            names_list = result.fetchall()
            names_dict = {"player1_name": names_list[0][0], "player2_name": names_list[1][0]}
            return names_dict
