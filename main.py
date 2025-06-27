from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Player, PlayerStats

app = FastAPI()

# Create tables on startup (optional)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "OP5 API is running"}

@app.get("/players")
def list_players(db: Session = Depends(SessionLocal)):
    return db.query(Player).all()
