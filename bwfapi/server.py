from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

import logging
from web_scraper import scrape_current_month_matches
from web_scraper.services import EchoService
from api.routes import player, match, tournament

## Snippet taken from: https://philstories.medium.com/fastapi-logging-f6237b84ea64
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/index", StaticFiles(directory="static", html=True), name="static")

@app.on_event("startup")
@repeat_every(seconds=999999, raise_exceptions=True, wait_first=True)  # 1 week
async def update_database():
    logger.info("Updating database")
    EchoService.echo("Running scraping script")
    await scrape_current_month_matches()
    EchoService.echo("Scraping script complete")

@app.get("/")
async def root():
    response = RedirectResponse(url="/index")
    return response

app.include_router(player.router)
app.include_router(match.router)
app.include_router(tournament.router)