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

from sqlalchemy import func, and_, desc, or_, union_all
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Integer
from bwfapi.api import models
from typing import Optional, Union

def format_response(data: Optional[Union[str, int]], req: str) -> Optional[dict]:
    if data:
        return {
            "request": req,
            "status": "success",
            "status_code": 200,
            "data": data
        }

## Players
def get_player(db: Session, player_id: str) -> Optional[dict]:
    result = db.query(models.Player) \
        .filter(models.Player.id == player_id) \
            .first()
            
    return format_response(result, f"GET request for player '{player_id}'")

def search_player(db: Session, search_text: str, limit: int) -> Optional[dict]:
    filter_list = [models.Player.name.contains(part) for part in search_text.split()]
    result = db.query(models.Player) \
        .filter(and_(*filter_list)) \
            .limit(limit) \
                .all()
    return format_response(result, f"GET request players with '{search_text}' in their name; limit of '{limit}'")

def get_top_win_players(db: Session, event: str, limit: int) -> Optional[dict]:
    result = db.query(models.Match.winnerId, models.Player.name, func.count(models.Match.winnerId).label("wins")). \
        join(models.Player, and_(models.Player.event.contains(event), (models.Player.id == models.Match.winnerId))). \
            group_by(models.Match.winnerId) \
                .order_by(desc("wins")) \
                    .limit(limit) \
                        .all()

    return format_response(result, f"GET top '{limit}' players from '{event}' according to win-rate")

## this beautiful query was thanks to vivian wu @ https://github.com/vvnwu
def get_player_records(db: Session, player_id: str, sort_wins: bool, sort_desc: bool, limit: int) -> Optional[dict]:
    players1 = db.query(models.Match.winnerId.label("opponent")) \
        .filter(models.Match.loserId == player_id) \
            .group_by(models.Match.winnerId)
    players2 = db.query(models.Match.loserId.label("opponent")) \
        .filter(models.Match.winnerId == player_id) \
            .group_by(models.Match.loserId)
    players_sq = players1.union(players2).order_by("opponent").subquery()

    losses_sq = db.query(models.Match.winnerId, coalesce(func.count(models.Match.loserId), 0).label("losses")) \
        .filter(models.Match.loserId == player_id) \
            .group_by(models.Match.winnerId).subquery()
    
    wins_sq = db.query(models.Match.loserId, coalesce(func.count(models.Match.winnerId), 0).label("wins")) \
        .filter(models.Match.winnerId == player_id) \
            .group_by(models.Match.loserId).subquery()

    results = db.query(players_sq.columns.opponent, coalesce(wins_sq.columns.wins, 0).label("wins"), coalesce(losses_sq.columns.losses, 0).label("losses")) \
        .outerjoin(wins_sq, players_sq.columns.opponent == wins_sq.columns.loserId) \
            .outerjoin(losses_sq, players_sq.columns.opponent == losses_sq.columns.winnerId) \
    
    if sort_desc:
        results = results.order_by(desc("wins" if sort_wins else "losses"))
    else:
        results = results.order_by("wins" if sort_wins else "losses")
        
    results = results.limit(limit).all()
    is_desc = "desc" if sort_desc else "asc"
    is_wins = "wins" if sort_wins else "losses"
    return format_response(results, f"GET head-to-head records of player '{player_id}' sorted by '{is_wins}', '{is_desc}'; limit of '{limit}'")

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

    return format_response(result, f"GET request match with player ids '{player_id}', '{opponent_id}'; tournament id '{tournament_id}'")

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

    results = results.limit(limit).all()
    
    return format_response(results, f"GET request matches from player id '{player_id}'; start of '{start_year}'; end of '{end_year}'; limit of '{limit}'")

def get_detailed_player_matches(db: Session, player_id: str, sort_desc: bool) -> Optional[dict]:
    result = db.query(models.Tournament.startDate, \
                        models.Match.winnerId, \
                        models.Match.loserId, \
                        models.Match.tournamentId, \
                        coalesce(func.sum(models.Set.winnerScore), 0).label("winnerPoints"), \
                        coalesce(func.sum(models.Set.loserScore), 0).label("loserPoints"), \
                        coalesce(func.count(models.Set.tournamentId)).label("setCount")) \
        .join(models.Tournament, models.Match.tournamentId.contains(models.Tournament.id)) \
            .join(models.Set, and_(models.Match.winnerId.contains(models.Set.winnerId), models.Match.loserId.contains(models.Set.loserId), models.Match.tournamentId.contains(models.Set.tournamentId))) \
                .filter(or_((models.Match.winnerId == player_id), (models.Match.loserId == player_id))) \
                    .group_by(models.Match.winnerId, models.Match.loserId, models.Match.tournamentId) 

    if sort_desc:
        result = result.order_by(desc(models.Tournament.startDate)).all()
    else:
        result = result.order_by(models.Tournament.startDate).all()

    return format_response(result, f"GET detailed matches of '{player_id}'")

def get_tournament_matches(db: Session, tournament_id: str, event: str, limit: int) -> Optional[dict]:
    result = db.query(models.Match) \
        .filter(models.Match.tournamentId == tournament_id) \
            .join(models.Player, models.Match.loserId.contains(models.Player.id)) \
                .filter(models.Player.event == event) \
                    .limit(limit) \
                        .all()

    return format_response(result, f"GET matches of event '{event}' from tournament '{tournament_id}'")


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

    return format_response(result, f"GET request matches between '{player_id}' and '{opponent_id}'; limit of '{limit}'")


## Tournaments
def get_tournament(db: Session, tournament_id: str) -> Optional[dict]:
    result = db.query(models.Tournament) \
        .filter(models.Tournament.id == tournament_id) \
            .first()
    
    return format_response(result, f"GET request for tournament '{tournament_id}'")

def search_tournament(db: Session, search_text: str, start_year: int, end_year: int, limit: int) -> Optional[dict]:
    start = f"{start_year}-01-01"
    end = f"{end_year}-01-01"
    filter_list = [models.Tournament.name.contains(part) for part in search_text.split()]
    result = db.query(models.Tournament) \
        .filter(and_(and_(*filter_list), models.Tournament.startDate.between(start, end))) \
            .limit(limit) \
                .all()

    return format_response(result, f"GET request tournaments with '{search_text}' in their name; start of '{start_year}'; end of '{end_year}'; limit of '{limit}'")

