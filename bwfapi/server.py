from fastapi import FastAPI, BackgroundTasks
from fastapi_utils.tasks import repeat_every
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

nest_asyncio.apply()

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project. 
                                      # This will get the root logger since no logger in the configuration has this name.

app = FastAPI()

@app.on_event("startup")
@repeat_every(seconds=60, raise_exceptions=True)  # 1 week
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

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

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

