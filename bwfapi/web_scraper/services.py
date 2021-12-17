## Taken from https://philstories.medium.com/fastapi-logging-f6237b84ea64

import logging

logger = logging.getLogger(__name__)  

class EchoService:
  def echo(msg):
    logger.info(msg)