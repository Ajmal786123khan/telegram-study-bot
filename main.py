import asyncio
import logging
from pyrogram import Client, filters, idle
import aiosqlite
from flask import Flask
from threading import Thread
import requests

================== LOGGING ==================

logging.basicConfig(level=logging.INFO)

================== KEEP ALIVE ==================

web_app = Flask('')

@web_app.route('/')
def home():
return "Bot is alive ✅"

def run_web():
web_app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

def keep_alive():
t = Thread(target=run_web)
t.daemon = True
t.start()

================== CONFIG ==================

DB_NAME = "database.db"

Telegram API

API_ID = 39226873
API_HASH = "3d434a799f8a642ebfb5e175bfc52e77"

Bot Tokens (⚠️ CHANGE THESE AFTER USE)

PW_BOT_TOKEN = "8553289877:AAGIUHX2PEu-xCjlw3EQOD8p1E206DVHNYc"
NEXT_BOT_TOKEN = "8437748698:AAErdBGclNfK9C05CBuyu6uPdA1ohXZXggk"
DELIVERY_BOT_TOKEN = "8790924971:AAGWB0RXmyKsmCcz1nde8mb2-xqmDK9Gpx8"

Bot Links

PW_BOT_URL = "https://t.me/PwStudyHud_bot"
NEXT_BOT_URL = "https://t.me/NextTopperStudyHub_bot"

Channel Config

FORCE_JOIN_CHANNEL = "Boardchanel10"  # without https://t.me/

Admin

ADMIN_ID = 7046379635

Shortlink API

SHORTLINK_API = "https://arolinks.com/api?api=YOUR_API&url={url}&alias={alias}"

================== DATABASE ==================

async def init_db():
async with aiosqlite.connect(DB_NAME) as db:
await db.executescript("""
CREATE TABLE IF NOT EXISTS users (
user_id INTEGER PRIMARY KEY,
username TEXT
);

    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id TEXT
    );
    """)
    await db.commit()

================== BOTS ==================

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

================== UTIL FUNCTIONS ==================

async def force_join(client, user_id):
try:
member = await client.get_chat_member(FORCE_JOIN_CHANNEL, user_id)
return member.status in ["member", "administrator", "creator"]
except:
return False

def get_shortlink(url, alias):
try:
api = SHORTLINK_API.format(url=url, alias=alias)
res = requests.get(api).json()
return res.get("shortenedUrl", url)
except:
return url

================== PW BOT ==================

@pw_bot.on_message(filters.command("start"))
async def pw_start(client, message):
user_id = message.from_user.id

if not await force_join(client, user_id):
    return await message.reply(
        f"🚫 Join Channel First:\nhttps://t.me/{FORCE_JOIN_CHANNEL}"
    )

await message.reply(
    "🎓 Welcome to PW Study Hub\n\n"
    "📚 Send /lectures\n"
    "📖 Send /books\n\n"
    f"🚀 Next Bot: {NEXT_BOT_URL}"
)

================== NEXT BOT ==================

@next_bot.on_message(filters.command("start"))
async def next_start(client, message):
await message.reply(
"🚀 Welcome to Next Topper Hub\n\n"
"🔥 Best content available!"
)

================== ADMIN UPLOAD ==================

@delivery_bot.on_message(filters.video & filters.user(ADMIN_ID))
async def save_file(client, message):
file_id = message.video.file_id

async with aiosqlite.connect(DB_NAME) as db:
    await db.execute("INSERT INTO files (file_id) VALUES (?)", (file_id,))
    await db.commit()

file_link = f"https://t.me/{client.me.username}?start={file_id}"
short = get_shortlink(file_link, file_id[:6])

await message.reply(f"✅ Saved!\n🔗 {short}")

================== DELIVERY BOT ==================

@delivery_bot.on_message(filters.command("start"))
async def deliver_file(client, message):
parts = message.text.split()

if len(parts) > 1:
    file_id = parts[1]

    try:
        await message.reply_video(file_id)
    except:
        await message.reply("❌ File not found")

================== MAIN ==================

async def main():
keep_alive()

await init_db()

await pw_bot.start()
await next_bot.start()
await delivery_bot.start()

print("🚀 All Bots Running...")

await idle()

await pw_bot.stop()
await next_bot.stop()
await delivery_bot.stop()

================== RUN ==================

if name == "main":
asyncio.run(main())
