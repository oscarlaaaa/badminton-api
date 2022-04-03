# Copyright © 2022 Oscar La
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this 
# software and associated documentation files (the "Software"), to deal in the Software 
# without restriction, including without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to the following 
# conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies 
# or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from bwfapi.api.database import Base

class Player(Base):
    __tablename__ = "player"

    id = Column(String, primary_key=True)
    name = Column(String)
    event = Column(String)
    country = Column(String)
    birthDate = Column(Date)
    playHand = Column(String)
    height = Column(Integer)
    img_link = Column(String)

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
    startDate = Column(Date)
    winnerPoints = Column(Integer)
    loserPoints = Column(Integer)
    setCount = Column(Integer)

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