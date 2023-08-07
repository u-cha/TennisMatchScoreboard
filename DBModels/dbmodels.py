import sqlalchemy.exc
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Connection
from sqlalchemy.orm import Session


class Base(DeclarativeBase):
    pass


class Match(Base):
    __tablename__ = "matches"
    uuid: Mapped[str] = mapped_column(primary_key=True)
    player1: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player2: Mapped[int] = mapped_column(ForeignKey("players.id"))
    winner: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=True)
    score: Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"Match(uuid={self.uuid!r}, player1={self.player1!r}, player2={self.player2!r}, winner={self.winner!r}),\
        score={self.score!r}"


class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), index=True, unique=True)

    matches = relationship("Match", backref="player",
                           foreign_keys=[Match.player1, Match.player2],
                           primaryjoin="or_(Player.id==Match.player1, Player.id==Match.player2)")

    def __repr__(self) -> str:
        return f"Player(id={self.id!r}, name={self.name!r})"


if __name__ == "__main__":

    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine)

    with Connection(engine) as connection:
        session = Session(connection)
        player = Player(name='Agassi')
        player2 = Player(name='Federer')

        session.add_all([player, player2])

        session.commit()

        player3 = Player(name='Agassi')
        try:
            session.add(player3)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print("smth", e.__dict__)
