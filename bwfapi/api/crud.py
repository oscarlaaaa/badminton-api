from sqlalchemy import func, and_, desc
from sqlalchemy.orm import Session
from . import models
from typing import Optional, Union

def format_response(data: Optional[Union[str, int]], req: str) -> Optional[dict]:
    if data:
        return {
            "request": req,
            "status": "success",
            "status_code": 200,
            "data": data
        }

def get_player(db: Session, player_id: str) -> Optional[dict]:
    result = db.query(models.Player).filter(
        models.Player.id == player_id).first()
    return format_response(result, f"GET request for player '{player_id}'")

def search_player(db: Session, search_text: str, limit: int) -> Optional[dict]:
    result = db.query(models.Player).filter(
        models.Player.name.contains(search_text)).limit(limit).all()
    return format_response(result, f"GET request players with '{search_text}' in their name; limit of '{limit}'")

def get_player_matches(db: Session, player_id: str, opponent_id: Optional[str], start_year: int, end_year: int, limit: int) -> Optional[dict]:
    start = f"{start_year}-01-01"
    end = f"{end_year}-01-01"
    if opponent_id is None:
        result = db.query(models.Match).join(models.Tournament).filter(
            models.Tournament.startDate.between(start, end)).limit(limit).all()
        return format_response(result, f"GET request matches from player id '{player_id}'; start of '{start_year}'; end of '{end_year}'; limit of '{limit}'")
    else:
        result = db.query(models.Match).join(models.Tournament). \
            filter(models.Tournament.startDate.between(start, end) & (((models.Match.winnerId == player_id) & (models.Match.loserId == opponent_id)) | ((models.Match.loserId == player_id) & (models.Match.winnerId == opponent_id)))).limit(limit).all()
        return format_response(result, f"GET request matches between '{player_id}' and '{opponent_id}'; start of '{start_year}'; end of '{end_year}'; limit of '{limit}'")

def get_top_win_players(db: Session, event: str, limit: int) -> Optional[dict]:
    result = db.query(models.Match.winnerId, models.Player.name, func.count(models.Match.winnerId).label("Wins")). \
        join(models.Player, and_((models.Player.event.contains(event)) & (models.Player.id == models.Match.winnerId))). \
            group_by(models.Match.winnerId).order_by(desc("Wins")).limit(limit).all()

    return format_response(result, f"GET top {limit} players from {event} according to win-rate")
