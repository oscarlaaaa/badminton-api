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
from bwfapi.api import crud, dependencies
from datetime import date

START_YEAR = 2008
END_YEAR = date.today().year + 1
router = APIRouter(
    prefix="/match",
    responses={404: {"description": "Not found"}}
)

@router.get("")
async def get_match(player_id: str="", opponent_id: str="", tournament_id: str="", db: Session=Depends(dependencies.get_db)) -> dict:
    EchoService.echo(f"search_player_matches called for player_id={player_id}, opponent_id={opponent_id}, tournament_id={tournament_id}")
    if player_id == "" or opponent_id == "" or tournament_id == "":
        raise InvalidParameterException(status_code=404, detail=f"Must include player, opponent, and tournament ids.")
    
    match = crud.get_match(db, player_id=player_id, opponent_id=opponent_id, tournament_id=tournament_id)
    if match is None:
        raise NoResultsException(status_code=404, detail=f"No match found for player_id={player_id}, opponent_id={opponent_id}, tournament_id={tournament_id}.")
    return match

@router.get("/player")
async def search_player_matches(player_id: str="", start_year: int=START_YEAR, end_year: int=END_YEAR, sort_desc: bool=True, limit: int=50, db: Session=Depends(dependencies.get_db)) -> dict:
    EchoService.echo(f"search_player_matches called for player_id={player_id}, start_year={start_year}, end_year={end_year}, limit={limit}")
    if start_year > end_year:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a start date after the end date.")
    if limit < 1:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a search limit below 1.")
    if player_id == "":
        raise InvalidParameterException(status_code=404, detail=f"Must include player_id parameter in query.")

    matches = crud.get_player_matches(db, player_id=player_id, start_year=start_year, end_year=end_year, sort_desc=sort_desc, limit=limit)

    if matches is None:
        raise NoResultsException(status_code=404, detail=f"No matches from {player_id}.")
    return matches

@router.get("/vs")
async def search_vs_matches(player_id: str="", opponent_id: str="", sort_desc: bool=True, limit: int=50, db: Session=Depends(dependencies.get_db)) -> dict:
    EchoService.echo(f"search_vs_matches called for player_id={player_id}, opponent_id={opponent_id}, limit={limit}")
    if limit < 1:
        raise InvalidParameterException(status_code=404, detail=f"Cannot have a search limit below 1.")
    if player_id == "" or opponent_id == "":
        raise InvalidParameterException(status_code=404, detail=f"Must include player_id and opponent_id parameters in query.")

    matches = crud.get_vs_matches(db, player_id=player_id, opponent_id=opponent_id, sort_desc=sort_desc, limit=limit)

    if matches is None:
        raise NoResultsException(status_code=404, detail=f"No matches between {player_id} and {opponent_id}.")
    return matches


@router.get("/tournament")
async def search_tournament_matches(tournament_id: str="", event: str="", limit: int=50, db: Session=Depends(dependencies.get_db)) -> dict:
    EchoService.echo(f"search_tournament_matches called for tournament_id={tournament_id}, limit={limit}")
    if tournament_id == "":
        raise InvalidParameterException(status_code=404, detail=f"Must include tournament_id parameter in query.")
    
    matches = crud.get_tournament_matches(db, tournament_id=tournament_id, event=event, limit=limit)
    if matches is None:
        raise NoResultsException(status_code=404, detail=f"No matches found for tournament {tournament_id}.")
    return matches
