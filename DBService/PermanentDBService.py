import sqlalchemy.exc
from sqlalchemy import create_engine, Connection
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
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
                session.add(obj)
                session.commit()
                return True
            except sqlalchemy.exc.IntegrityError as error:
                return False

    @classmethod
    def get_player_id_by_name(cls, name):
        cls.__create_tables()
        with Connection(cls.engine) as connection:
            session = Session(connection)
            result = session.execute(select(Player.id).where(Player.name == name))
            return result.fetchone()[0]

    @classmethod
    def get_match_by_uuid(cls, uuid):
        cls.__create_tables()
        with Connection(cls.engine) as connection:
            session = Session(connection)
            result = session.execute(select(Match).where(Match.uuid == uuid))
            return result.fetchall()
