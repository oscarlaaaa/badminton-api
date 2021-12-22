from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from web_scraper.services import EchoService
from api.exceptions import InvalidParameterException, NoResultsException
from api import crud, dependencies
from datetime import date

START_YEAR = 2008
END_YEAR = date.today().year + 1
router = APIRouter(
    prefix="/match",
    responses={404: {"description": "Not found"}}
)

@router.get("/player")
async def search_player_matches(player_id: str="", start_year: int=START_YEAR, end_year: int=END_YEAR, limit: int=50, db: Session=Depends(dependencies.get_db)) -> dict:
    EchoService.echo(f"search_player_matches called for player_id={player_id}, start_year={start_year}, end_year={end_year}, limit={limit}")
    if start_year > end_year:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a start date after the end date.")
    if limit < 1:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a search limit below 1.")
    if player_id == "":
        raise InvalidParameterException(status_code=404, detail=f"Must include player_id parameter in query.")

    matches = crud.get_player_matches(db, player_id=player_id, start_year=start_year, end_year=end_year, limit=limit)

    if matches is None:
        raise NoResultsException(status_code=404, detail=f"No matches from {player_id}.")
    return matches

@router.get("/vs")
async def search_vs_matches(player_id: str="", opponent_id: str="", limit: int=50, db: Session=Depends(dependencies.get_db)) -> dict:
    EchoService.echo(f"search_vs_matches called for player_id={player_id}, opponent_id={opponent_id}, limit={limit}")
    if limit < 1:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a search limit below 1.")
    if player_id == "" or opponent_id == "":
        raise InvalidParameterException(status_code=404, detail=f"Must include player_id and opponent_id parameters in query.")

    matches = crud.get_vs_matches(db, player_id=player_id, opponent_id=opponent_id,  limit=limit)

    if matches is None:
        raise NoResultsException(status_code=404, detail=f"No matches between {player_id} and {opponent_id}.")
    return matches

@router.get("/tournament")
async def search_tournament_matches(tournament_id: str="", limit: int=50, db: Session=Depends(dependencies.get_db)) -> dict:
    EchoService.echo(f"search_tournament_matches called for tournament_id={tournament_id}, limit={limit}")
    if tournament_id == "":
        raise InvalidParameterException(status_code=404, detail=f"Must include tournament_id parameter in query.")
    
    matches = crud.get_tournament_matches(db, tournament_id=tournament_id, limit=limit)
    if matches is None:
        raise NoResultsException(status_code=404, detail=f"No matches found for tournament {tournament_id}.")
    return matches