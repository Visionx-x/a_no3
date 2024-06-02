from sys import exit

from async_mongo import AsyncClient

from bot import*
from vars import*
import logging
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    mongo = AsyncClient(DB_URI)
    db = mongo["Assistant"]
    logger.info("Connected to your Mongo Database.")
except Exception as e:
    logger.error(f"Failed to connect to your Mongo Database.\ {e}")
    exit(1)
