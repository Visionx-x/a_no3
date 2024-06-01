from sys import exit

from async_mongo import AsyncClient

from bot import logger
from vars import DB_URI

try:
    mongo = AsyncClient(DB_URI)
    db = mongo["Assistant"]
    logger.info("Connected to your Mongo Database.")
except Exception as e:
    logger.error(f"Failed to connect to your Mongo Database.\ {e}")
    exit(1)
