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

@router.get("/search")
async def search_tournament(name: str="", limit: int=20, db: Session=Depends(dependencies.get_db)) -> dict:
    EchoService.echo(f"search_tournament called for name={name}, limit={limit}")
    if limit < 1:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a search limit below 1.")

    players = crud.search_tournament(db, search_text=name, limit=limit)
    if players is None:
        raise NoResultsException(status_code=404, detail=f"No tournament with {name} in their name.")
    return players