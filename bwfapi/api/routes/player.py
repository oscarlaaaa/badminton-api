from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from web_scraper.services import EchoService
from api.exceptions import InvalidParameterException, NoResultsException
from api import crud, dependencies

router = APIRouter(
    prefix="/player",
    responses={404: {"description": "Not found"}}
)

@router.get("")
async def get_player(player_id: str="", db: Session=Depends(dependencies.get_db)) -> dict:
    EchoService.echo(f"get_player called for player_id={player_id}")
    player = crud.get_player(db, player_id=player_id)
    if player is None:
        raise NoResultsException(status_code=404, detail="Player could not found")
    return player

VALID_EVENTS = {"MS", "WS", ""}
@router.get("/top")
async def get_top_wins(event: str="", limit: int=10, db: Session=Depends(dependencies.get_db)) -> dict:
    EchoService.echo(f"get_top_wins called for event={event}, limit={limit}")
    if limit < 1:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a search limit below 1.")
    if event.upper() not in VALID_EVENTS:
        raise InvalidParameterException(status_code=404, detail=f"Event must be WS, MS, or blank.")

    players = crud.get_top_win_players(db, event=event, limit=limit)
    if players is None:
        raise NoResultsException(status_code=404, detail="Error in querying top players")
    return players

@router.get("/search") ## takes in /search?name=<STUFF>
async def search_player(name: str="", limit: int=20, db: Session=Depends(dependencies.get_db)) -> dict:
    EchoService.echo(f"search_player called for name={name}, limit={limit}")
    if limit < 1:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a search limit below 1.")

    players = crud.search_player(db, search_text=name, limit=limit)
    if players is None:
        raise NoResultsException(status_code=404, detail=f"No player with {name} in their name.")
    return players


@router.get("/records")
async def get_records(player_id: str="", sort_wins: bool=True, sort_desc: bool=True, limit: int=10, db: Session=Depends(dependencies.get_db)) -> dict:
    sortby = "wins" if sort_wins else "losses"
    order = "descending" if sort_desc else "ascending"
    EchoService.echo(f"get_head_to_heads called for player_id={player_id} sorted by {sortby} in {order}, limit={limit}")
    if limit < 1:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a search limit below 1.")

    h2h = crud.get_player_records(db, player_id=player_id, sort_wins=sort_wins, sort_desc=sort_desc, limit=limit)
    if h2h is None:
        raise NoResultsException(status_code=404, detail=f"No head to heads found for {player_id}.")
    return h2h