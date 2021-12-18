from fastapi import FastAPI, Depends, HTTPException
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session

import time
import asyncio
import nest_asyncio
from enum import Enum
from web_scraper import scrape_current_month_matches, lol
from web_scraper.db import DBOperator
from datetime import date

import logging
from fastapi import FastAPI
from web_scraper.services import EchoService
from api import crud, models
from api import SessionLocal, engine

nest_asyncio.apply()

## Snippet taken from: https://philstories.medium.com/fastapi-logging-f6237b84ea64
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/players/{name}")
async def get_player(name: str, db: Session=Depends(get_db)):
    player = crud.get_player(db, player_name=name)
    if player is None:
        raise HTTPException(status_code=404, detail="Player could not found")
    return player

@app.on_event("startup")
@repeat_every(seconds=999999, raise_exceptions=True, wait_first=True)  # 1 week
async def update_database():
    logger.info("Updating database")
    EchoService.echo("Running scraping script")
    await scrape_current_month_matches()
    EchoService.echo("a scraping script")

@app.get("/")
async def root():
    logger.info("logging from the root logger")
    EchoService.echo("hi")
    return {"message": "Hello World"}

@app.get("/clear")
async def reset_db():
    logger.info("Clearing database")
    EchoService.echo("Running clearing script")
    db = DBOperator()
    db.reset_database()
    return {"message" : "Database cleared!"}

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}