from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os

MAIN_CHANNEL_ID = -1002441344477  # Replace with your main channel ID

# Direct channel buttons (each opens link directly)
channel_buttons = [
    ("🔞 Jav Nation", "https://t.me/+A5sllB-vY4diNzk9"),
    ("🥵 Jav Collection", "https://t.me/+A5sllB-vY4diNzk9"),
    ("🔥 OnlyFans Nation", "https://t.me/+IO7rG_j0CFE3NDg9"),
    ("💀 OnlyFans Collection", "https://t.me/+IO7rG_j0CFE3NDg9"),
    ("💖 Favhouse Nation", "https://t.me/+4X0ep0FK_lc2Nzg1"),
    ("🩷 Favhouse Collection", "https://t.me/+4X0ep0FK_lc2Nzg1"),
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    member = await context.bot.get_chat_member(chat_id=MAIN_CHANNEL_ID, user_id=user.id)

    if member.status in ["left", "kicked"]:
        # User has not joined the channel
        join_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Pehle Channel Join Karein", url="https://t.me/unseentabs")],
            [InlineKeyboardButton("🔄 Dobara Try Karein", callback_data="retry_join")]
        ])
        await update.message.reply_text(
            "❌ Pehle aapko hamara main channel join karna hoga.",
            reply_markup=join_buttons
        )
    else:
        # Show direct buttons with URLs
        buttons = [[InlineKeyboardButton(text, url=url)] for text, url in channel_buttons]
        markup = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(
            "✅ Aap ne channel join kar liya hai. Ab niche se category select karein:",
            reply_markup=markup
        )


async def retry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    member = await context.bot.get_chat_member(chat_id=MAIN_CHANNEL_ID, user_id=user.id)

    if member.status in ["left", "kicked"]:
        join_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Pehle Channel Join Karein", url="https://t.me/unseentabs")],
            [InlineKeyboardButton("🔄 Dobara Try Karein", callback_data="retry_join")]
        ])
        await query.edit_message_text(
            "⚠️ Pehle aapko hamara main channel join karna hoga.",
            reply_markup=join_buttons
        )
    else:
        buttons = [[InlineKeyboardButton(text, url=url)] for text, url in channel_buttons]
        markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            "✅ Aap ne channel join kar liya hai. Ab niche se category select karein:",
            reply_markup=markup
        )


if __name__ == "__main__":
    import asyncio

    async def main():
        token = os.getenv("BOT_TOKEN")
        if not token:
            print("❌ BOT_TOKEN not found. Set it in Railway Variables.")
            return

        app = ApplicationBuilder().token(token).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(telegram.ext.CallbackQueryHandler(retry, pattern="retry_join"))

        print("✅ Bot is running...")
        await app.run_polling()

    asyncio.run(main())
