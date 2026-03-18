from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import FORCE_JOIN_CHANNEL

CHANNEL_USERNAME = "Boardchanel10"  # extracted from your link

def register(app):

    # ================== START COMMAND ==================

    @app.on_message(filters.command("start"))
    async def start(client, message):
        user_id = message.from_user.id

        # 🔍 Check if user joined channel
        try:
            member = await client.get_chat_member(CHANNEL_USERNAME, user_id)

            if member.status not in ["member", "administrator", "creator"]:
                raise Exception("Not joined")

        except:
            buttons = [
                [InlineKeyboardButton("📢 Join Channel", url=FORCE_JOIN_CHANNEL)],
                [InlineKeyboardButton("✅ Retry", callback_data="check_join")]
            ]

            await message.reply(
                "⚠️ You must join our channel to use this bot!",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return

        # ✅ If joined
        buttons = [
            [InlineKeyboardButton("📚 Lectures", callback_data="lectures")],
            [InlineKeyboardButton("📖 Books", callback_data="books")]
        ]

        await message.reply(
            "🎓 Welcome to Study Hub 🚀\n\nSelect an option:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # ================== RETRY BUTTON ==================

    @app.on_callback_query(filters.regex("check_join"))
    async def check_join_callback(client, callback_query):
        user_id = callback_query.from_user.id

        try:
            member = await client.get_chat_member(CHANNEL_USERNAME, user_id)

            if member.status not in ["member", "administrator", "creator"]:
                raise Exception("Still not joined")

        except:
            await callback_query.answer(
                "❌ Join the channel first!",
                show_alert=True
            )
            return

        # ✅ Joined successfully
        buttons = [
            [InlineKeyboardButton("📚 Lectures", callback_data="lectures")],
            [InlineKeyboardButton("📖 Books", callback_data="books")]
        ]

        await callback_query.message.edit_text(
            "✅ Access Granted!\n\nChoose below:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
