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

async def check_user_joined(user_id, context):
    member = await context.bot.get_chat_member(chat_id=MAIN_CHANNEL_ID, user_id=user_id)
    return member.status not in ["left", "kicked"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if await check_user_joined(user.id, context):
        await send_all_buttons(update.message.reply_text)
    else:
        await send_join_prompt(update.message.reply_text)

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    if await check_user_joined(user.id, context):
        await query.edit_message_text("✅ Aap ne channel join kar liya hai. Ab niche se category select karein:")
        await send_all_buttons(query.message.reply_text)
    else:
        await query.edit_message_text("⚠️ Pehle aapko hamara main channel join karna hoga.")
        await send_join_prompt(query.message.reply_text)

async def send_all_buttons(send_fn):
    buttons = [[InlineKeyboardButton(text, url=url)] for text, url in channel_links]
    markup = InlineKeyboardMarkup(buttons)
    await send_fn("👇 Niche diye gaye channels me se select karein:", reply_markup=markup)

async def send_join_prompt(send_fn):
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Pehle Channel Join Karein", url="https://t.me/unseentabs")],
        [InlineKeyboardButton("🔄 Dobara Try Karein", callback_data="check_join")]
    ])
    await send_fn("⚠️ Pehle aapko hamara main channel join karna hoga.", reply_markup=markup)

# ✅ Railway-compatible run block
if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("❌ BOT_TOKEN not found in Railway Variables.")
    else:
        app = ApplicationBuilder().token(token).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))

        print("✅ Bot is running...")
        app.run_polling(stop_signals=None)
