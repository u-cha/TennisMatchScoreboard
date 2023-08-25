from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Match(Base):
    __tablename__ = "matches"
    uuid: Mapped[str] = mapped_column(primary_key=True)
    player1: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"))
    player2: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"))
    winner: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), nullable=True)
    score: Mapped[str] = mapped_column(String(500))

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


