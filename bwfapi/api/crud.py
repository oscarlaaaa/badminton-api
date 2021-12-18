from sqlalchemy.orm import Session
from . import models
from typing import Optional, Union

def format_response(data: Optional[Union[str, int]], req: str) -> Optional[dict]:
    if data:
        return {
            "request" : req,
            "status" : "success",
            "status_code" : 200,
            "data" : data
        }

def get_player(db: Session, player_id: str) -> Optional[dict]:
    result = db.query(models.Player).filter(models.Player.id == player_id).first()
    return format_response(result, f"GET request for single player {player_id}")

def search_player(db: Session, search_text: str) -> Optional[dict]:
    search_text = search_text.replace("_", " ").upper()
    result = db.query(models.Player).filter(models.Player.name.contains(search_text)).limit(20).all()
    return format_response(result, f"GET request players with {search_text} in their name")

def get_player_matches(db: Session, player_id: str) -> Optional[dict]:
    result = db.query(models.Match).filter((models.Match.winnerId == player_id) | (models.Match.loserId == player_id)).all()
    return format_response(result, f"GET request matches from player id {player_id}")