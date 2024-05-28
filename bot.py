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
    bot_token=B_TOKEN,
    api_id=API,
    api_hash=API_HASH
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
        json.dump(data, file, indent=4)

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
                InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ]
        ]
        await message.reply_text(
            text="**HELLO...⚡\n\ni am an advanced telegram auto request accept bot.**",
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Error in start handler: {e}")

@thanos.on_chat_member_updated(filters.group)
async def welcome_goodbye(client: thanos, message: ChatMemberUpdated):
    try:
        new_chat_member = message.new_chat_member
        old_chat_member = message.old_chat_member
        chat = message.chat

        if new_chat_member:
            if new_chat_member.status == "member":
                add_to_data(group_data, chat.id, GROUP_DATA_FILE)
                user = new_chat_member.user
                logger.info(f"{user.first_name} joined {chat.title}")
                await client.send_message(
                    chat_id=chat.id,
                    text=f"Hello {user.mention}, welcome to {chat.title}!"
                )
        elif old_chat_member:
            if old_chat_member.status == "left":
                user = old_chat_member.user
                logger.info(f"{user.first_name} left {chat.title}")
                await client.send_message(
                    chat_id=chat.id,
                    text=f"Goodbye {user.mention}, we will miss you in {chat.title}!"
                )

                # Send a personal goodbye message to the user
                personal_goodbye_message = (
                    "⚠️ Sorry for the inconvenience caused\n"
                    "🚨 You Can Request any Anime here\n"
                    "👉 https://t.me/SonuBhaiyaBot\n"
                    "🛎️ Koi bhi Help ke liye msg here ☝️"
                )

                await client.send_message(
                    chat_id=user.id,
                    text=personal_goodbye_message
                )
    except Exception as e:
        logger.error(f"Error in welcome_goodbye handler: {e}")

@thanos.on_chat_join_request()
async def autoapprove(client: thanos, message: ChatJoinRequest):
    try:
        await client.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
        logger.info(f"Approved join request for {message.from_user.first_name} in {message.chat.title}")

        # Send a welcome message to the group or channel
        #await client.send_message(
          #  chat_id=message.chat.id,
          #  text=f"Hello {message.from_user.mention}, welcome to {message.chat.title}!"
     #   )

        # Send a personal welcome message to the user
        personal_message = (
            f"👋 𝗛𝗲𝗹𝗹𝗼 {message.from_user.mention}, Welcome to 𝗔𝗻𝗶𝗺𝗲𝗔𝗿𝗶𝘀𝗲\n\n"
            "🔰 𝗪𝗵𝗮𝘁 𝘆𝗼𝘂 𝘄𝗶𝗹𝗹 𝗴𝗲𝘁 𝗯𝘆 𝗝𝗼𝗶𝗻𝗶𝗻𝗴 𝗔𝗻𝗶𝗺𝗲𝗔𝗿𝗶𝘀𝗲?\n"
            "1⃣ All your favourite anime in different audio like English Hindi Tamil etc\n"
            "2⃣ Anime with a Complete Season or Ongoing Episode\n"
            "3⃣ Watch Now and Download link of all the anime\n\n"
            "✊ 𝗕𝗲𝗰𝗼𝗺𝗲 𝗮 𝗺𝗲𝗺𝗯𝗲𝗿 𝗼𝗳 𝗼𝘂𝗿 𝗔𝗻𝗶𝗺𝗲𝗔𝗿𝗶𝘀𝗲 𝗖𝗼𝗺𝗺𝘂𝗻𝗶𝘁𝘆\n"
            "1⃣ Request any anime which you want to watch.\n"
            "2⃣ If the anime is available our Bot will provide you the link.\n"
            "3⃣ Chat with Other Anime Lovers.\n\n"
            "🔰 Anime online dekhe Hindi English Tamil etc languages me\n\n"
            "♥️ Our Community Joining Link 👇\n"
            "https://t.me/AnimeArise\n"
            "https://t.me/AnimeArise\n"
            "https://t.me/AnimeArise\n\n"
            "🔰 𝗦𝗲𝗻𝗱 /start 𝘁𝗼 𝗸𝗻𝗼𝘄 𝗺𝗼𝗿𝗲 𝗮𝗯𝗼𝘂𝘁 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁."
        )

        await client.send_message(
            chat_id=message.from_user.id,
            text=personal_message
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
    