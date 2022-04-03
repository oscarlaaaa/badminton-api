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

from sqlalchemy import func, and_, desc
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.orm import Session
from bwfapi.api import models, utils
from typing import Optional

def get_player(db: Session, player_id: str) -> Optional[dict]:
    result = db.query(models.Player) \
        .filter(models.Player.id == player_id) \
            .first()
            
    return utils.format_response(result, f"GET request for player '{player_id}'")

def search_player(db: Session, search_text: str, limit: int) -> Optional[dict]:
    filter_list = [models.Player.name.contains(part) for part in search_text.split()]
    result = db.query(models.Player) \
        .filter(and_(*filter_list)) \
            .limit(limit) \
                .all()
    return utils.format_response(result, f"GET request players with '{search_text}' in their name; limit of '{limit}'")

def get_top_win_players(db: Session, event: str, limit: int) -> Optional[dict]:
    result = db.query(models.Match.winnerId, models.Player.name, func.count(models.Match.winnerId).label("wins")). \
        join(models.Player, and_(models.Player.event.contains(event), (models.Player.id == models.Match.winnerId))). \
            group_by(models.Match.winnerId) \
                .order_by(desc("wins")) \
                    .limit(limit) \
                        .all()

    return utils.format_response(result, f"GET top '{limit}' players from '{event}' according to win-rate")


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
    return utils.format_response(results, f"GET head-to-head records of player '{player_id}' sorted by '{is_wins}', '{is_desc}'; limit of '{limit}'")