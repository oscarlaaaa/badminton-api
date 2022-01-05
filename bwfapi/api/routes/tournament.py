from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from web_scraper.services import EchoService
from api.exceptions import InvalidParameterException, NoResultsException
from api import crud, dependencies
from datetime import date

START_YEAR = 2008
END_YEAR = date.today().year + 1
router = APIRouter(
    prefix="/tournament",
    responses={404: {"description": "Not found"}}
)

@router.get("")
async def get_tournament(tournament_id: str, db: Session=Depends(dependencies.get_db)) -> dict:
    EchoService.echo(f"get_tournament called for id={tournament_id}")
    if tournament_id == "":
        raise InvalidParameterException(status_code=404, detail=f"Must have tournament id.")
    
    tournament = crud.get_tournament(db, tournament_id)
    if tournament is None:
        raise NoResultsException(status_code=404, detail=f"No tournament with {tournament_id} as an id.")
    return tournament

@router.get("/search")
async def search_tournament(name: str="", start_year: int=START_YEAR, end_year: int=END_YEAR, limit: int=50, db: Session=Depends(dependencies.get_db)) -> dict:
    EchoService.echo(f"search_tournament called for name={name}, start_year={start_year}, limit={limit}")
    if limit < 1:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a search limit below 1.")
    if start_year > end_year:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a start date after the end date.")

    tournaments = crud.search_tournament(db, search_text=name, start_year=start_year, end_year=end_year, limit=limit)
    if tournaments is None:
        raise NoResultsException(status_code=404, detail=f"No tournament with {name} in its name between {start_year} and {end_year}.")
    return tournaments


