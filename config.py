import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ================== CONFIG ==================

PW_BOT_TOKEN = "8553289877:AAGIUHX2PEu-xCjlw3EQOD8p1E206DVHNYc"
NEXT_BOT_TOKEN = "8437748698:AAErdBGclNfK9C05CBuyu6uPdA1ohXZXggk"
DELIVERY_BOT_TOKEN = "8790924971:AAGWB0RXmyKsmCcz1nde8mb2-xqmDK9Gpx8"

APP_API_ID = 39226873
APP_API_HASH = "3d434a799f8a642ebfb5e175bfc52e77"

ADMIN_USER_ID = 7046379635
PRIVATE_CHANNEL_ID = -1003812084739

FORCE_JOIN_CHANNEL = "https://t.me/Boardchanel10"

SHORTLINK_API_BOOK = "https://arolinks.com/api?api=b43087cc2e97e7131232209d2adc98364ecbf21f&url="
SHORTLINK_API_LECTURE = "https://arolinks.com/api?api=6d6b19730d806e46dc258768e715e5c4a498fb97&url="

NEXT_BOT_URL = "https://t.me/NextTopperStudyHub_bot"
PW_BOT_URL = "https://t.me/PwStudyHud_bot"

# ================== LOGGING ==================

logging.basicConfig(level=logging.INFO)

# ================== SHORTLINK FUNCTION ==================

def create_shortlink(api, url):
    try:
        response = requests.get(f"{api}{url}")
        return response.text
    except:
        return url

# ================== FORCE JOIN CHECK ==================

async def force_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        member = await context.bot.get_chat_member("@Boardchanel10", user.id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False
    except:
        return False

# ================== START COMMAND ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joined = await force_join(update, context)

    if not joined:
        keyboard = [
            [InlineKeyboardButton("Join Channel", url=FORCE_JOIN_CHANNEL)],
            [InlineKeyboardButton("Retry", callback_data="retry")]
        ]
        await update.message.reply_text(
            "⚠️ You must join our channel to use the bot!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    keyboard = [
        [InlineKeyboardButton("📚 Lecture", callback_data="lecture")],
        [InlineKeyboardButton("📖 Books", callback_data="books")],
        [InlineKeyboardButton("🚀 Next Topper", url=NEXT_BOT_URL)],
        [InlineKeyboardButton("🎯 PW Bot", url=PW_BOT_URL)]
    ]

    await update.message.reply_text(
        "🎓 Welcome to Nova Study Hub!\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================== BUTTON HANDLER ==================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "retry":
        await start(update, context)

    elif query.data == "lecture":
        link = "https://example.com/lecture"
        short = create_shortlink(SHORTLINK_API_LECTURE, link)

        keyboard = [
            [InlineKeyboardButton("📥 Download Lecture", url=short)]
        ]

        await query.message.reply_text(
            "🎥 Your lecture is ready:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "books":
        link = "https://example.com/book"
        short = create_shortlink(SHORTLINK_API_BOOK, link)

        keyboard = [
            [InlineKeyboardButton("📥 Download Book", url=short)]
        ]

        await query.message.reply_text(
            "📚 Your book is ready:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ================== DELIVERY BOT ==================

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
    app = Application.builder().token(DELIVERY_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("deliver", deliver))

    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
