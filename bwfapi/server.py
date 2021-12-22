from typing import Optional
from fastapi import FastAPI, Depends
from fastapi_utils.tasks import repeat_every
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from web_scraper import scrape_current_month_matches
from datetime import date
from starlette.responses import RedirectResponse

import logging
from fastapi import FastAPI
from web_scraper.services import EchoService
from api import InvalidParameterException, NoResultsException
from api import crud
from api import SessionLocal

## Snippet taken from: https://philstories.medium.com/fastapi-logging-f6237b84ea64
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/index", StaticFiles(directory="static", html=True), name="static")

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
async def root():
    response = RedirectResponse(url="/index")
    return response

## lol i should leave this publicly available
# @app.get("/clear")
# async def reset_db() -> dict:
#     logger.info("Clearing database")
#     EchoService.echo("Running clearing script")
#     db = DBOperator()
#     db.reset_database()
#     return {
#         "request" : "clear database",
#         "status" : "success",
#     }

@app.get("/player")
async def get_player(player_id: str="", db: Session=Depends(get_db)) -> dict:
    player = crud.get_player(db, player_id=player_id)
    if player is None:
        raise NoResultsException(status_code=404, detail="Player could not found")
    return player

VALID_EVENTS = {"MS", "WS", ""}
@app.get("/players/top")
async def get_top_wins(event: str="", limit: int=10, db: Session=Depends(get_db)) -> dict:
    if limit < 1:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a search limit below 1.")
    if event.upper() not in VALID_EVENTS:
        raise InvalidParameterException(status_code=404, detail=f"Event must be WS, MS, or blank.")

    players = crud.get_top_win_players(db, event=event, limit=limit)
    if players is None:
        raise NoResultsException(status_code=404, detail="Error in querying top players")
    return players

@app.get("/search") ## takes in /search?name=<STUFF>
async def search_player(name: str="", limit: int=20, db: Session=Depends(get_db)) -> dict:
    if limit < 1:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a search limit below 1.")

    players = crud.search_player(db, search_text=name, limit=limit)
    if players is None:
        raise NoResultsException(status_code=404, detail=f"No player with {name} in their name.")
    return players

START_YEAR = 2008
END_YEAR = date.today().year + 1

@app.get("/matches")
async def search_player_matches(player_id: Optional[str]=None, opponent_id: Optional[str]=None, start_year: int=2008, end_year: int=END_YEAR, limit: int=50, db: Session=Depends(get_db)) -> dict:
    if start_year > end_year:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a start date after the end date.")

    if limit < 1:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a search limit below 1.")

    if player_id == "":
        raise InvalidParameterException(status_code=404, detail=f"Must include player_id parameter in query.")

    matches = crud.get_player_matches(db, player_id=player_id, opponent_id=opponent_id, start_year=start_year, end_year=end_year, limit=limit)

    if matches is None:
        if opponent_id is None:
            raise NoResultsException(status_code=404, detail=f"No matches from {player_id}.")
        else:
            raise NoResultsException(status_code=404, detail=f"No matches between {player_id} and {opponent_id}.")

    return matches
