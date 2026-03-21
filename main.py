import asyncio
from pyrogram import Client, idle
import aiosqlite

# ================== KEEP ALIVE (Flask) ==================

from flask import Flask
from threading import Thread

web_app = Flask('')

@web_app.route('/')
def home():
    return "Bot is alive ✅"

def run_web():
    web_app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# ================== CONFIG ==================


# ================== CONFIG ==================

DB_NAME = "database.db"

# Telegram API
APP_API_ID = 39226873
APP_API_HASH = "3d434a799f8a642ebfb5e175bfc52e77"

# Bot Tokens
PW_BOT_TOKEN = "8553289877:AAGIUHX2PEu-xCjlw3EQOD8p1E206DVHNYc"
NEXT_BOT_TOKEN = "8437748698:AAErdBGclNfK9C05CBuyu6uPdA1ohXZXggk"
DELIVERY_BOT_TOKEN = "8790924971:AAGWB0RXmyKsmCcz1nde8mb2-xqmDK9Gpx8"

# Bot Info
PW_BOT_URL = "https://t.me/PwStudyHud_bot"
NEXT_BOT_URL = "https://t.me/NextTopperStudyHub_bot"

# Channel Config
PRIVATE_CHANNEL_ID = -1003812084739
FORCE_JOIN_CHANNEL = "https://t.me/Boardchanel10"

# Admin
ADMIN_USER_ID = 7046379635

# Shortlink APIs
SHORTLINK_API_LECTURE = "https://arolinks.com/api?api=6d6b19730d806e46dc258768e715e5c4a498fb97&url={url}&alias={alias}"
SHORTLINK_API_BOOK = "https://arolinks.com/api?api=b43087cc2e97e7131232209d2adc98364ecbf21f&url={url}&alias={alias}"

# ================== DATABASE ==================

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT
        );
        """)
        await db.commit()

# ================== BOTS ==================

pw_bot = Client(
    "pw_bot",
    bot_token=PW_BOT_TOKEN,
    api_id=APP_API_ID,
    api_hash=APP_API_HASH
)

next_bot = Client(
    "next_bot",
    bot_token=NEXT_BOT_TOKEN,
    api_id=APP_API_ID,
    api_hash=APP_API_HASH
)

delivery_bot = Client(
    "delivery_bot",
    bot_token=DELIVERY_BOT_TOKEN,
    api_id=APP_API_ID,
    api_hash=APP_API_HASH
)

# ================== HANDLERS ==================

@pw_bot.on_message()
async def pw_handler(client, message):
    if message.text and message.text.startswith("/start"):
        await message.reply(
            "🎓 Welcome to PW Study Hub\n\n"
            "📚 Get Lectures\n"
            "📖 Get Books\n\n"
            f"🚀 Next Bot: {NEXT_BOT_URL}"
        )

@next_bot.on_message()
async def next_handler(client, message):
    if message.text and message.text.startswith("/start"):
        await message.reply(
            "🚀 Welcome to Next Topper Hub\n\n"
            "🔥 Boost your preparation here!"
        )

@delivery_bot.on_message()
async def delivery_handler(client, message):
    if message.text and message.text.startswith("/start"):
        parts = message.text.split()

        if len(parts) > 1:
            file_id = parts[1]

            try:
                await message.reply_video(file_id)
            except:
                await message.reply("❌ File not found")

# ================== MAIN ==================

async def main():
    await init_db()

    await pw_bot.start()
    await next_bot.start()
    await delivery_bot.start()

    print("🚀 PW + NEXT + DELIVERY Bots Running...")

    await idle()

    await pw_bot.stop()
    await next_bot.stop()
    await delivery_bot.stop()

# ================== RUN ==================

if __name__ == "__main__":
    asyncio.run(main())
