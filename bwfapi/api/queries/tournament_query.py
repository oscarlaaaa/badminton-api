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

from sqlalchemy import and_
from sqlalchemy.orm import Session
from bwfapi.api import models, utils
from typing import Optional

def get_tournament(db: Session, tournament_id: str) -> Optional[dict]:
    result = db.query(models.Tournament) \
        .filter(models.Tournament.id == tournament_id) \
            .first()
    
    return utils.format_response(result, f"GET request for tournament '{tournament_id}'")

def search_tournament(db: Session, search_text: str, start_year: int, end_year: int, limit: int) -> Optional[dict]:
    start = f"{start_year}-01-01"
    end = f"{end_year}-01-01"
    filter_list = [models.Tournament.name.contains(part) for part in search_text.split()]
    result = db.query(models.Tournament) \
        .filter(and_(and_(*filter_list), models.Tournament.startDate.between(start, end))) \
            .limit(limit) \
                .all()

    return utils.format_response(result, f"GET request tournaments with '{search_text}' in their name; start of '{start_year}'; end of '{end_year}'; limit of '{limit}'")

