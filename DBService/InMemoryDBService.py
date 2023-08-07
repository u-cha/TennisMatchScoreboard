import sqlalchemy.exc
from sqlalchemy import create_engine, Connection
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update
from DBModels.dbmodels import Base, Match, Player


class InMemoryDBService:
    engine = create_engine("sqlite+pysqlite:///:memory:",
                           connect_args={"check_same_thread": False},
                           poolclass=StaticPool, echo=True)

    connection = None

    @classmethod
    def __establish_connection(cls):
        if cls.connection is None:
            cls.connection = Connection(cls.engine)

    @classmethod
    def __create_tables(cls):
        Base.metadata.create_all(cls.engine)

    @classmethod
    def persist(cls, obj):
        cls.__establish_connection()
        cls.__create_tables()
        with Session(cls.connection, expire_on_commit=False) as session:
            try:
                session.add(obj)
                session.commit()
                return True
            except sqlalchemy.exc.IntegrityError as error:
                return False

    @classmethod
    def remove(cls, obj):
        cls.__establish_connection()
        cls.__create_tables()
        with Session(cls.connection, expire_on_commit=False) as session:
            session.delete(obj)
            session.commit()

    @classmethod
    def get_player_id_by_name(cls, name):
        cls.__establish_connection()
        cls.__create_tables()
        with Session(cls.connection) as session:
            stmt = select(Player.id).where(Player.name == name)
            result = session.execute(stmt)
            return result.fetchone()[0]

    @classmethod
    def get_match_by_uuid(cls, uuid):
        cls.__establish_connection()
        cls.__create_tables()
        with Session(cls.connection) as session:
            stmt = select(Match).where(Match.uuid == uuid)
            result = session.execute(stmt)
            return result.fetchone()[0]

    @classmethod
    def update_match_score(cls, uuid, new_score):
        cls.__establish_connection()
        cls.__create_tables()
        with Session(cls.connection) as session:
            stmt = update(Match).where(Match.uuid == uuid).values(score=new_score)
            session.execute(stmt)
