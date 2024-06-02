from sys import exit

from async_mongo import AsyncClient

from bot import*
from vars import*

try:
    mongo = AsyncClient(DB_URI)
    db = mongo["Assistant"]
    logger.info("Connected to your Mongo Database.")
except Exception as e:
    logger.error(f"Failed to connect to your Mongo Database.\ {e}")
    exit(1)

usersdb = db["users"]


async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})
