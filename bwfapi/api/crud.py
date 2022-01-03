from sqlalchemy import func, and_, desc, or_, union_all
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Integer
from api import models
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
    parts = search_text.split()
    filter_list = [models.Player.name.contains(part) for part in parts]

    result = db.query(models.Player) \
        .filter(or_(*filter_list)) \
            .limit(limit) \
                .all()

    # result = db.query(models.Player) \
    #     .filter(models.Player.name.contains(search_text)) \
    #         .limit(limit) \
    #             .all()

    return format_response(result, f"GET request players with '{search_text}' in their name; limit of '{limit}'")

def get_top_win_players(db: Session, event: str, limit: int) -> Optional[dict]:
    result = db.query(models.Match.winnerId, models.Player.name, func.count(models.Match.winnerId, Integer).label("wins")). \
        join(models.Player, and_(models.Player.event.contains(event), (models.Player.id == models.Match.winnerId))). \
            group_by(models.Match.winnerId) \
                .order_by(desc("wins")) \
                    .limit(limit) \
                        .all()

    return format_response(result, f"GET top {limit} players from {event} according to win-rate")

## this beautiful query was thanks to vivian wu @ https://github.com/vvnwu
def get_player_head_to_heads(db: Session, player_id: str, wins: bool, desc: bool, limit: int) -> Optional[dict]:
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
    
    if desc:
        results = results.order_by(desc("wins" if wins else "losses"))
    else:
        results = results.order_by("wins" if wins else "losses")

    is_desc = "desc" if desc else "asc"
    is_wins = "wins" if wins else "losses"
    return format_response(results, f"GET head-to-head records of player {player_id} sorted by {is_wins}, {is_desc}; limit of '{limit}'")

## Matches
def get_player_matches(db: Session, player_id: str, start_year: int, end_year: int, limit: int) -> Optional[dict]:
    start = f"{start_year}-01-01"
    end = f"{end_year}-01-01"
    result = db.query(models.Match).join(models.Tournament) \
        .filter(models.Tournament.startDate.between(start, end)) \
            .limit(limit) \
                .all()

    return format_response(result, f"GET request matches from player id '{player_id}'; start of '{start_year}'; end of '{end_year}'; limit of '{limit}'")


def get_tournament_matches(db: Session, tournament_id: str, event: str, limit: int) -> Optional[dict]:
    result = db.query(models.Match).filter(models.Match.tournamentId == tournament_id) \
        .join(models.Player, models.Match.loserId.contains(models.Player.event)) \
            .filter(models.Player.event == event) \
                .limit(limit) \
                    .all()

    return format_response(result, f"GET matches of event {event} from tournament {tournament_id}")


def get_vs_matches(db: Session, player_id: str, opponent_id: str, limit: int) -> Optional[dict]:
    result = db.query(models.Match).join(models.Tournament) \
        .filter(or_(and_((models.Match.winnerId == player_id), (models.Match.loserId == opponent_id)), and_((models.Match.loserId == player_id), (models.Match.winnerId == opponent_id)))) \
            .limit(limit) \
                .all()

    return format_response(result, f"GET request matches between '{player_id}' and '{opponent_id}'; limit of '{limit}'")


## Tournaments
def search_tournament(db: Session, search_text: str, limit: int) -> Optional[dict]:
    result = db.query(models.Tournament) \
        .filter(models.Tournament.name.contains(search_text)) \
            .order_by(desc(models.Tournament.startDate)) \
                .limit(limit) \
                    .all()

    return format_response(result, f"GET request tournaments with '{search_text}' in their name; limit of '{limit}'")

def get_tournament(db: Session, tournament_id: str) -> Optional[dict]:
    result = db.query(models.Tournament) \
        .filter(models.Tournament.id == tournament_id) \
            .first()
    
    return format_response(result, f"GET request for tournament '{tournament_id}'")