from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
import os

MAIN_CHANNEL_ID = -1002441344477  # Replace with your channel ID

channel_buttons = {
    "jav": [("🔞 Jav Nation", "https://t.me/+A5sllB-vY4diNzk9"), ("🥵 Jav Collection", "https://t.me/+A5sllB-vY4diNzk9")],
    "onlyfans": [("🔥 OnlyFans Nation", "https://t.me/+IO7rG_j0CFE3NDg9"), ("💀 OnlyFans Collection", "https://t.me/+IO7rG_j0CFE3NDg9")],
    "favhouse": [("💖 Favhouse Nation", "https://t.me/+4X0ep0FK_lc2Nzg1"), ("🩷 Favhouse Collection", "https://t.me/+4X0ep0FK_lc2Nzg1")],
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    member = await context.bot.get_chat_member(chat_id=MAIN_CHANNEL_ID, user_id=user.id)
    if member.status in ["left", "kicked"]:
        join_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Main Channel", url="https://t.me/unseentabs")],
            [InlineKeyboardButton("I've Joined", callback_data="check_join")]
        ])
        await update.message.reply_text("Please join the main channel first:", reply_markup=join_markup)
    else:
        await show_categories(update, context)

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    member = await context.bot.get_chat_member(chat_id=MAIN_CHANNEL_ID, user_id=user.id)
    if member.status in ["left", "kicked"]:
        await query.edit_message_text("❌ You haven't joined the main channel yet.")
    else:
        await show_categories(update, context, query)

async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    buttons = [
        [InlineKeyboardButton("🔞 JAV", callback_data="jav")],
        [InlineKeyboardButton("🔥 OnlyFans", callback_data="onlyfans")],
        [InlineKeyboardButton("💖 Favhouse", callback_data="favhouse")],
    ]
    markup = InlineKeyboardMarkup(buttons)
    if query:
        await query.edit_message_text("Select a category:", reply_markup=markup)
    else:
        await update.message.reply_text("Select a category:", reply_markup=markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data in channel_buttons:
        btns = [[InlineKeyboardButton(text, url=url)] for text, url in channel_buttons[data]]
        await query.edit_message_text("Here are your channels:", reply_markup=InlineKeyboardMarkup(btns))

def main():
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
