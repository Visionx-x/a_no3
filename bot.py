import os
import json
import logging
from vars import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatMemberUpdated, ChatJoinRequest

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the bot
thanos = Client(
    "bot_started",
    bot_token= B_TOKEN,
    api_id= API,
    api_hash= API_HASH
)

# File paths for storing data
USER_DATA_FILE = "user_data.json"
GROUP_DATA_FILE = "group_data.json"

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

def save_data(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file)

user_data = load_data(USER_DATA_FILE)
group_data = load_data(GROUP_DATA_FILE)

def add_to_data(data_list, new_entry, file_path):
    if new_entry not in data_list:
        data_list.append(new_entry)
        save_data(data_list, file_path)

@thanos.on_message(filters.private & filters.command(["start"]))
async def start(client: thanos, message: Message):
    try:
        add_to_data(user_data, message.from_user.id, USER_DATA_FILE)
        button = [
            [
                InlineKeyboardButton("𝚄𝙿𝙳𝙰𝚃𝙴", url=f"{UPDATE}"),
                InlineKeyboardButton("𝚂𝚄𝙿𝙿𝙾𝚁𝚃", url=f"{SUPPORT}")
            ],
            [
                InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ]
        ]
        await message.reply_text(
            text="**HELLO...⚡\n\ni am a advance telegram auto request accept bot.**",
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Error in start handler: {e}")

@thanos.on_chat_member_updated(filters.group)
async def welcome_goodbye(client: thanos, message: ChatMemberUpdated):
    try:
        if message.new_chat_member.status == "member":
            add_to_data(group_data, message.chat.id, GROUP_DATA_FILE)
            user = message.new_chat_member.user
            chat = message.chat
            logger.info(f"{user.first_name} joined {chat.title}")
            await client.send_message(
                chat_id=chat.id,
                text=f"Hello {user.mention}, welcome to {chat.title}!"
            )

        elif message.new_chat_member.status == "left":
            user = message.old_chat_member.user
            chat = message.chat
            logger.info(f"{user.first_name} left {chat.title}")
            await client.send_message(
                chat_id=chat.id,
                text=f"Goodbye {user.mention}, we will miss you in {chat.title}!"
            )

    except Exception as e:
        logger.error(f"Error in welcome_goodbye handler: {e}")

@thanos.on_chat_join_request(filters.group)
async def autoapprove(client: thanos, message: ChatJoinRequest):
    try:
        await client.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
        logger.info(f"Approved join request for {message.from_user.first_name} in {message.chat.title}")

        await client.send_message(
            chat_id=message.chat.id,
            text=f"Hello {message.from_user.mention}, welcome to {message.chat.title}!"
        )
    except Exception as e:
        logger.error(f"Error in autoapprove handler: {e}")



@thanos.on_message(filters.command("broadcast") & filters.user(ownerid))
async def broadcast_message(client: thanos, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a message to broadcast.")
        return

    broadcast_text = " ".join(message.command[1:])

    for user_id in user_data:
        try:
            await client.send_message(
                chat_id=int(user_id),
                text=f"📛 Broadcast Message From Admin !!\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n{broadcast_text}"
            )
            logger.info(f"Sent broadcast message to {user_id}")
        except Exception as e:
            logger.error(f"Error sending broadcast message to {user_id}: {e}")

    for group_id in group_data:
        try:
            await client.send_message(
                chat_id=int(group_id),
                text=f"📛 Broadcast Message From Admin !!\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n{broadcast_text}"
            )
            logger.info(f"Sent broadcast message to group {group_id}")
        except Exception as e:
            logger.error(f"Error sending broadcast message to group {group_id}: {e}")



if __name__ == "__main__":
    thanos.run()
    