from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import os

# Use environment variable for DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app instance
app = FastAPI()

# --- Database Models ---
class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    stats = relationship("PlayerStats", back_populates="player")

class PlayerStats(Base):
    __tablename__ = "player_stats"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    pa = Column(Integer)
    ab = Column(Integer)
    h = Column(Integer)
    hr = Column(Integer)
    rbi = Column(Integer)
    tb = Column(Integer)

    player = relationship("Player", back_populates="stats")

# --- Dependency to get DB session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ---

@app.post("/players")
def create_player(name: str, db: Session = Depends(get_db)):
    player = Player(name=name)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

@app.post("/players/{player_id}/stats")
def add_stats(
    player_id: int,
    pa: int,
    ab: int,
    h: int,
    hr: int,
    rbi: int,
    tb: int,
    db: Session = Depends(get_db)
):
    stats = PlayerStats(player_id=player_id, pa=pa, ab=ab, h=h, hr=hr, rbi=rbi, tb=tb)
    db.add(stats)
    db.commit()
    db.refresh(stats)
    return stats

@app.get("/players")
def list_players(db: Session = Depends(get_db)):
    return db.query(Player).all()

@app.get("/players/{player_id}/stats")
def get_player_stats(player_id: int, db: Session = Depends(get_db)):
    return db.query(PlayerStats).filter(PlayerStats.player_id == player_id).all()

# --- Create database tables if they don't exist ---
Base.metadata.create_all(bind=engine)
