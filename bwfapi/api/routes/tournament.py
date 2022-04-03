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

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from bwfapi.web_scraper.services import EchoService
from bwfapi.api.exceptions import InvalidParameterException, NoResultsException
from bwfapi.api import dependencies
from bwfapi.api.queries import tournament_query
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
    
    tournament = tournament_query.get_tournament(db, tournament_id)
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

    tournaments = tournament_query.search_tournament(db, search_text=name, start_year=start_year, end_year=end_year, limit=limit)
    if tournaments is None:
        raise NoResultsException(status_code=404, detail=f"No tournament with {name} in its name between {start_year} and {end_year}.")
    return tournaments
