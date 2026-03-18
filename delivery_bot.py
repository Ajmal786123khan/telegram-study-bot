import logging
import requests
import aiosqlite
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ================== CONFIG ==================

DB_NAME = "database.db"

PW_BOT_TOKEN = "8553289877:AAGIUHX2PEu-xCjlw3EQOD8p1E206DVHNYc"
NEXT_BOT_TOKEN = "8437748698:AAErdBGclNfK9C05CBuyu6uPdA1ohXZXggk"
DELIVERY_BOT_TOKEN = "8790924971:AAGWB0RXmyKsmCcz1nde8mb2-xqmDK9Gpx8"

ADMIN_USER_ID = 7046379635
PRIVATE_CHANNEL_ID = -1003812084739

FORCE_JOIN_CHANNEL = "https://t.me/Boardchanel10"

SHORTLINK_API_BOOK = "https://arolinks.com/api?api=b43087cc2e97e7131232209d2adc98364ecbf21f&url="
SHORTLINK_API_LECTURE = "https://arolinks.com/api?api=6d6b19730d806e46dc258768e715e5c4a498fb97&url="

NEXT_BOT_URL = "https://t.me/NextTopperStudyHub_bot"
PW_BOT_URL = "https://t.me/PwStudyHud_bot"

logging.basicConfig(level=logging.INFO)

# ================== DATABASE ==================

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            points INTEGER DEFAULT 0,
            referrals INTEGER DEFAULT 0,
            premium INTEGER DEFAULT 0,
            referral_code TEXT
        );

        CREATE TABLE IF NOT EXISTS shortlinks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            resource_type TEXT,
            resource_id INTEGER,
            alias TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        await db.commit()

# ================== USER SYSTEM ==================

async def add_user(user):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT OR IGNORE INTO users (user_id, username)
        VALUES (?, ?)
        """, (user.id, user.username))
        await db.commit()

# ================== SHORTLINK ==================

def create_shortlink(api, url):
    try:
        r = requests.get(f"{api}{url}")
        return r.text
    except:
        return url

async def save_shortlink(user_id, r_type, alias):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT INTO shortlinks (user_id, resource_type, alias)
        VALUES (?, ?, ?)
        """, (user_id, r_type, alias))
        await db.commit()

# ================== FORCE JOIN ==================

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        member = await context.bot.get_chat_member("@Boardchanel10", user.id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ================== START ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await add_user(user)

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
        [InlineKeyboardButton("📚 Lecture", callback_data="lecture")],
        [InlineKeyboardButton("📖 Books", callback_data="books")],
        [InlineKeyboardButton("🚀 Next Bot", url=NEXT_BOT_URL)],
        [InlineKeyboardButton("🎯 PW Bot", url=PW_BOT_URL)]
    ]

    await update.message.reply_text(
        "🎓 Welcome to Nova Study Hub",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================== BUTTON ==================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    if query.data == "retry":
        await start(update, context)

    elif query.data == "lecture":
        link = "https://example.com/lecture"
        short = create_shortlink(SHORTLINK_API_LECTURE, link)

        await save_shortlink(user.id, "lecture", short)

        keyboard = [[InlineKeyboardButton("📥 Download Lecture", url=short)]]
        await query.message.reply_text(
            "🎥 Lecture Ready",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "books":
        link = "https://example.com/book"
        short = create_shortlink(SHORTLINK_API_BOOK, link)

        await save_shortlink(user.id, "book", short)

        keyboard = [[InlineKeyboardButton("📥 Download Book", url=short)]]
        await query.message.reply_text(
            "📚 Book Ready",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ================== ADMIN DELIVERY ==================

async def deliver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        return

    if update.message.reply_to_message:
        await context.bot.copy_message(
            chat_id=update.message.chat_id,
            from_chat_id=PRIVATE_CHANNEL_ID,
            message_id=update.message.reply_to_message.message_id
        )

# ================== MAIN ==================

def main():
    import asyncio
    asyncio.run(init_db())

    app = Application.builder().token(DELIVERY_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("deliver", deliver))

    print("🚀 Bot Running with Database...")
    app.run_polling()

if __name__ == "__main__":
    main()
