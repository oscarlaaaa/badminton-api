from fastapi import FastAPI, Depends, HTTPException
from fastapi_utils.tasks import repeat_every
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from enum import Enum
from web_scraper import scrape_current_month_matches
from web_scraper.db import DBOperator
from datetime import date

import logging
from fastapi import FastAPI
from web_scraper.services import EchoService
from api import crud, models
from api import SessionLocal, engine

## Snippet taken from: https://philstories.medium.com/fastapi-logging-f6237b84ea64
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
@repeat_every(seconds=999999, raise_exceptions=True, wait_first=True)  # 1 week
async def update_database() -> dict:
    logger.info("Updating database")
    EchoService.echo("Running scraping script")
    await scrape_current_month_matches()
    EchoService.echo("Scraping script complete")
    return {
        "request" : "update database",
        "status" : "success",
    }

@app.get("/")
async def root() -> dict:
    logger.info("logging from the root logger")
    EchoService.echo("hi")
    return {"message": "Hello World"}

@app.get("/clear")
async def reset_db() -> dict:
    logger.info("Clearing database")
    EchoService.echo("Running clearing script")
    db = DBOperator()
    db.reset_database()
    return {
        "request" : "clear database",
        "status" : "success",
    }

@app.get("/players/{player_id}")
async def get_player(player_id: str, db: Session=Depends(get_db)) -> dict:
    player = crud.get_player(db, player_id=player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player could not found")
    return player

@app.get("/search") ## takes in /search?name=<STUFF>
async def search_player(name: str, db: Session=Depends(get_db)) -> dict:
    players = crud.search_player(db, search_text=name)
    if players is None:
        raise HTTPException(status_code=404, detail=f"No player with {name} in their name.")
    return players

@app.get("/matches/{player_id}")
async def search_player_matches(player_id: str, db: Session=Depends(get_db)) -> dict:
    matches = crud.get_player_matches(db, player_id=player_id)
    if matches is None:
        raise HTTPException(status_code=404, detail=f"No matches from {player_id}.")
    return matches