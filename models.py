from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    stats = relationship("PlayerStats", back_populates="player")

class PlayerStats(Base):
    __tablename__ = "player_stats"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    pa = Column(Integer)
    ab = Column(Integer)
    h = Column(Integer)
    roe = Column(Integer)
    single_1b = Column(Integer)
    double_2b = Column(Integer)
    triple_3b = Column(Integer)
    hr = Column(Integer)
    bb = Column(Integer)
    r = Column(Integer)
    rbi = Column(Integer)
    sb = Column(Integer)
    ra = Column(Integer)
    cs = Column(Integer)
    tho = Column(Integer)
    hbp = Column(Integer)
    tb = Column(Integer)
    sac_f = Column(Integer)
    sac_b = Column(Integer)
    gidp = Column(Integer)
    outs = Column(Integer)
    k = Column(Integer)
    rob = Column(Integer)
    lob = Column(Integer)
    tob = Column(Integer)

    player = relationship("Player", back_populates="stats")
