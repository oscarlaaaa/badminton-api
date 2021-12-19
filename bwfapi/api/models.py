from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from .database import Base

class Player(Base):
    __tablename__ = "player"

    id = Column(String, primary_key=True)
    name = Column(String)
    event = Column(String)
    country = Column(String)
    birthDate = Column(Date)
    playHand = Column(String)
    height = Column(Integer)

class Tournament(Base):
    __tablename__ = "tournament"

    id = Column(String, primary_key=True)
    startDate = Column(Date)
    endDate = Column(Date)
    name = Column(String)

class Match(Base):
    __tablename__ = "match"

    winnerId = Column(String, ForeignKey("player.id"), primary_key=True)
    loserId = Column(String, ForeignKey("player.id"), primary_key=True)
    tournamentId = Column(String, ForeignKey("tournament.id"), primary_key=True)
    duration = Column(Integer)

    winner = relationship("Player", foreign_keys="Match.winnerId")
    loser = relationship("Player", foreign_keys="Match.loserId")
    tournament = relationship("Tournament", foreign_keys="Match.tournamentId")

class Set(Base):
    __tablename__ = "set"

    round = Column(Integer, primary_key=True)
    winnerId = Column(String, ForeignKey("match.winnerId"), primary_key=True)
    loserId = Column(String, ForeignKey("match.loserId"), primary_key=True)
    tournamentId = Column(String, ForeignKey("match.tournamentId"), primary_key=True)
    winnerScore = Column(Integer)
    loserScore = Column(Integer)

    winner = relationship("Match", foreign_keys="Set.winnerId")
    loser = relationship("Match", foreign_keys="Set.loserId")
    tournament = relationship("Match", foreign_keys="Set.tournamentId")