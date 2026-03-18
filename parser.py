import logging
import requests
import aiosqlite
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# ================== CONFIG ==================

DB_NAME = "database.db"

DELIVERY_BOT_TOKEN = "8790924971:AAGWB0RXmyKsmCcz1nde8mb2-xqmDK9Gpx8"

ADMIN_USER_ID = 7046379635
PRIVATE_CHANNEL_ID = -1003812084739

FORCE_JOIN_CHANNEL = "https://t.me/Boardchanel10"

SHORTLINK_API_BOOK = "https://arolinks.com/api?api=b43087cc2e97e7131232209d2adc98364ecbf21f&url="
SHORTLINK_API_LECTURE = "https://arolinks.com/api?api=6d6b19730d806e46dc258768e715e5c4a498fb97&url="

logging.basicConfig(level=logging.INFO)

# ================== PARSER ==================

def clean_title(title: str):
    title = re.sub(r"\bClass\s*\d+\w*\b.*?", "", title)
    title = re.sub(r"-\s*\d{3,4}p(\.mp4)?", "", title)
    title = re.sub(r"\d{3,4}p", "", title)
    title = re.sub(r"Powered by.*", "", title)
    title = re.sub(r"⚡.*", "", title)
    return title.strip()

def extract_lecture_info(title):
    title = clean_title(title)
    match = re.search(r"(\d{1,3})$", title)
    lecture_no = int(match.group(1)) if match else 1
    chapter = re.sub(r"\d{1,3}$", "", title).strip()
    return chapter, lecture_no

def normalize_subject(subject):
    subject = subject.lower()
    if "math" in subject:
        return "maths"
    return subject

# ================== DATABASE ==================

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executescript("""
        CREATE TABLE IF NOT EXISTS lectures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            chapter TEXT,
            lecture_no INTEGER,
            file_id TEXT
        );
        """)
        await db.commit()

async def save_lecture(subject, chapter, lecture_no, file_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT INTO lectures (subject, chapter, lecture_no, file_id)
        VALUES (?, ?, ?, ?)
        """, (subject, chapter, lecture_no, file_id))
        await db.commit()

# ================== SHORTLINK ==================

def create_shortlink(api, url):
    try:
        r = requests.get(f"{api}{url}")
        return r.text
    except:
        return url

# ================== FORCE JOIN ==================

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        member = await context.bot.get_chat_member("@Boardchanel10", update.effective_user.id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ================== AUTO LECTURE CAPTURE ==================

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post

    if message.chat.id != PRIVATE_CHANNEL_ID:
        return

    if not message.video:
        return

    caption = message.caption or "Unknown Lecture"

    # Extract info
    chapter, lecture_no = extract_lecture_info(caption)
    subject = normalize_subject(caption)

    # Save in DB
    await save_lecture(subject, chapter, lecture_no, message.video.file_id)

    print(f"Saved: {subject} | {chapter} | Lecture {lecture_no}")

# ================== START ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joined = await check_join(update, context)

    if not joined:
        keyboard = [
            [InlineKeyboardButton("Join Channel", url=FORCE_JOIN_CHANNEL)],
            [InlineKeyboardButton("Retry", callback_data="retry")]
        ]
        await update.message.reply_text(
            "⚠️ Join channel first!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    keyboard = [
        [InlineKeyboardButton("📚 Get Lecture", callback_data="lecture")]
    ]

    await update.message.reply_text(
        "🎓 Welcome!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================== BUTTON ==================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "lecture":
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT file_id FROM lectures ORDER BY id DESC LIMIT 1")
            row = await cursor.fetchone()

        if not row:
            await query.message.reply_text("No lectures available")
            return

        file_id = row[0]

        # Generate shortlink
        link = f"https://t.me/NovaStudy10_bot?start={file_id}"
        short = create_shortlink(SHORTLINK_API_LECTURE, link)

        keyboard = [[InlineKeyboardButton("📥 Unlock Lecture", url=short)]]

        await query.message.reply_text(
            "🎥 Click below to get lecture",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ================== DELIVERY ==================

async def deliver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if not args:
        return

    file_id = args[0]

    await update.message.reply_video(file_id)

# ================== MAIN ==================

def main():
    import asyncio
    asyncio.run(init_db())

    app = Application.builder().token(DELIVERY_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("start", deliver))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_channel_post))

    print("🚀 Smart Lecture Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
