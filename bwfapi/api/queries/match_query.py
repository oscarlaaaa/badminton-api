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

from sqlalchemy import and_, desc, or_
from sqlalchemy.orm import Session
from bwfapi.api import models, utils
from typing import Optional

## Matches
def get_match(db: Session, player_id: str, opponent_id: str, tournament_id: str) -> Optional[dict]:
    match = db.query(models.Match).filter(and_(models.Match.tournamentId == tournament_id, 
        or_(and_(models.Match.winnerId == player_id, models.Match.loserId == opponent_id), and_(models.Match.winnerId == opponent_id, models.Match.loserId == player_id)))).subquery()
    
    sets = db.query(models.Set).filter(and_(models.Set.tournamentId == tournament_id, 
        or_(and_(models.Set.winnerId == player_id, models.Set.loserId == opponent_id), and_(models.Set.winnerId == opponent_id, models.Set.loserId == player_id)))) \
            .order_by(models.Set.round) \
                .subquery()
    
    result = db.query(match, sets.columns.round, sets.columns.winnerScore, sets.columns.loserScore) \
        .outerjoin(sets, match.columns.winnerId == sets.columns.winnerId).all()

    return utils.format_response(result, f"GET request match with player ids '{player_id}', '{opponent_id}'; tournament id '{tournament_id}'")

def get_player_matches(db: Session, player_id: str, start_year: int, end_year: int, sort_desc: bool, limit: int) -> Optional[dict]:
    start = f"{start_year}-01-01"
    end = f"{end_year}-01-01"
    results = db.query(models.Match) \
        .join(models.Tournament, models.Match.tournamentId.contains(models.Tournament.id)) \
            .filter(and_(or_((models.Match.winnerId == player_id), (models.Match.loserId == player_id)), models.Tournament.startDate.between(start, end))) \
    
    if sort_desc:
        results = results.order_by(desc(models.Tournament.startDate))
    else:
        results = results.order_by(models.Tournament.startDate)

    if limit != 0:
        results = results.limit(limit).all()
    else:
        results = results.all()
    
    return utils.format_response(results, f"GET request matches from player id '{player_id}'; start of '{start_year}'; end of '{end_year}'; limit of '{limit}'")

def get_tournament_matches(db: Session, tournament_id: str, event: str, limit: int) -> Optional[dict]:
    result = db.query(models.Match) \
        .filter(models.Match.tournamentId == tournament_id) \
            .join(models.Player, models.Match.loserId.contains(models.Player.id)) \
                .filter(models.Player.event == event) \
                    .limit(limit) \
                        .all()

    return utils.format_response(result, f"GET matches of event '{event}' from tournament '{tournament_id}'")


def get_vs_matches(db: Session, player_id: str, opponent_id: str, sort_desc: bool, limit: int) -> Optional[dict]:
    result = db.query(models.Match) \
        .join(models.Tournament, models.Match.tournamentId.contains(models.Tournament.id)) \
            .filter(or_(and_((models.Match.winnerId == player_id), (models.Match.loserId == opponent_id)), 
                and_((models.Match.loserId == player_id), (models.Match.winnerId == opponent_id)))) 

    if sort_desc:
        results = results.order_by(desc(models.Tournament.startDate))
    else:
        results = results.order_by(models.Tournament.startDate)

    results = results.limit(limit).all()

    return utils.format_response(result, f"GET request matches between '{player_id}' and '{opponent_id}'; limit of '{limit}'")

