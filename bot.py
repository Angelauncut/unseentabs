from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
import os

MAIN_CHANNEL_ID = -1002441344477

channel_links = [
    ("🔞 Jav Nation", "https://t.me/+A5sllB-vY4diNzk9"),
    ("🥵 Jav Collection", "https://t.me/+A5sllB-vY4diNzk9"),
    ("🔥 OnlyFans Nation", "https://t.me/+IO7rG_j0CFE3NDg9"),
    ("💀 OnlyFans Collection", "https://t.me/+IO7rG_j0CFE3NDg9"),
    ("💖 Favhouse Nation", "https://t.me/+4X0ep0FK_lc2Nzg1"),
    ("🩷 Favhouse Collection", "https://t.me/+4X0ep0FK_lc2Nzg1"),
]

def get_join_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Pehle Channel Join Karein", url="https://t.me/unseentabs")],
        [InlineKeyboardButton("🔄 Dobara Try Karein", callback_data="check_join")]
    ])

def get_channel_markup():
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, callback_data=f"open_{i}")] for i, (text, _) in enumerate(channel_links)])

async def is_user_joined(user_id, context):
    member = await context.bot.get_chat_member(chat_id=MAIN_CHANNEL_ID, user_id=user_id)
    return member.status not in ["left", "kicked"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if await is_user_joined(user.id, context):
        await update.message.reply_text(
            "✅ Aap ne channel join kar liya hai. Ab niche se category select karein:",
            reply_markup=get_channel_markup()
        )
    else:
        await update.message.reply_text(
            "❌ Pehle aapko hamara main channel join karna hoga.",
            reply_markup=get_join_markup()
        )

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if await is_user_joined(user.id, context):
        await query.message.reply_text(
            "✅ Aap ne channel join kar liya hai. Ab niche se category select karein:",
            reply_markup=get_channel_markup()
        )
    else:
        await query.message.reply_text(
            "⚠️ Pehle aapko hamara main channel join karna hoga.",
            reply_markup=get_join_markup()
        )

async def handle_channel_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if not await is_user_joined(user.id, context):
        await query.message.reply_text(
            "⚠️ Pehle aapko hamara main channel join karna hoga.",
            reply_markup=get_join_markup()
        )
        return

    index = int(query.data.replace("open_", ""))
    text, url = channel_links[index]
    await query.message.reply_text(
        f"🔗 {text}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text, url=url)]])
    )

# ✅ Railway-Compatible Launch
if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("❌ BOT_TOKEN not found in Railway Variables.")
    else:
        app = ApplicationBuilder().token(token).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
        app.add_handler(CallbackQueryHandler(handle_channel_button, pattern=r"open_\d+"))

        print("✅ Bot is running...")
        app.run_polling(stop_signals=None)
