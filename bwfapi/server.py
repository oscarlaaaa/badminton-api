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

import random
import uvicorn
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import logging
from os import path
from bwfapi.web_scraper.bwf_scraper import scrape_current_month_matches
from bwfapi.web_scraper.services import EchoService
from bwfapi.api.routes import player, match, tournament

## Snippet taken from: https://philstories.medium.com/fastapi-logging-f6237b84ea64
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/index", StaticFiles(directory="bwfapi/static", html=True), name="static")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://analytics.badminton-api.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

wait = random.randint(0, 5)
@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24 * (15 + wait), raise_exceptions=True, wait_first=True)  # ~half a month
async def update_database():
    logger.info("Updating database")
    EchoService.echo("Running scraping script")
    await scrape_current_month_matches()
    EchoService.echo("Scraping script complete")

@app.get("/")
async def root():
    response = RedirectResponse(url="index")
    return response

app.include_router(player.router)
app.include_router(match.router)
app.include_router(tournament.router)

if __name__ == "__main__":
    uvicorn.run('server:app', host='0.0.0.0', port=5000, reload=False, root_path="")