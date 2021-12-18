from sqlalchemy.orm import Session

from . import models

def get_player(db: Session, player_name: str):
    player_name = player_name.replace("_", " ").upper()
    return db.query(models.Player).filter(models.Player.name == player_name).first()