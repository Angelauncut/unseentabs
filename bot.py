from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

import os

MAIN_CHANNEL_ID = -1002441344477  # Replace with your @unseentabs channel ID

# 🔘 Button groups
channel_buttons = {
    "jav": [
        ("🔞 Jav Nation", "https://t.me/+A5sllB-vY4diNzk9"),
        ("🥵 Jav Collection", "https://t.me/+A5sllB-vY4diNzk9"),
    ],
    "onlyfans": [
        ("🔥 OnlyFans Nation", "https://t.me/+IO7rG_j0CFE3NDg9"),
        ("💀 OnlyFans Collection", "https://t.me/+IO7rG_j0CFE3NDg9"),
    ],
    "favhouse": [
        ("💖 Favhouse Nation", "https://t.me/+4X0ep0FK_lc2Nzg1"),
        ("🩷 Favhouse Collection", "https://t.me/+4X0ep0FK_lc2Nzg1"),
    ],
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    member = await context.bot.get_chat_member(chat_id=MAIN_CHANNEL_ID, user_id=user.id)
    
    if member.status in ["left", "kicked"]:
        join_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔐 Join Main Channel", url="https://t.me/unseentabs")],
            [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]
        ])
        await update.message.reply_text("Please join the main channel to continue:", reply_markup=join_button)
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
    reply_markup = InlineKeyboardMarkup(buttons)

    if query:
        await query.edit_message_text("Select a category:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Select a category:", reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data in channel_buttons:
        buttons = [[InlineKeyboardButton(text, url=url)] for text, url in channel_buttons[data]]
        await query.edit_message_text("Here are your channels:", reply_markup=InlineKeyboardMarkup(buttons))

async def main():
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(CallbackQueryHandler(handle_button))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    try:
        member = context.bot.get_chat_member(MAIN_CHANNEL, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            if data == 'jav':
                query.message.reply_text(f"🔞 [Join Jav Nation]({JAV_LINK})", parse_mode="Markdown")
            elif data == 'of':
                query.message.reply_text(f"🔥 [Join OnlyFans Nation]({OF_LINK})", parse_mode="Markdown")
            elif data == 'fav':
                query.message.reply_text(f"💖 [Join Favhouse Nation]({FAV_LINK})", parse_mode="Markdown")
        else:
            raise Exception("Not joined")
    except:
        join_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("👉 Pehle Unseen Tabs Join Karo", url=MAIN_CHANNEL_LINK)]
        ])
        query.message.reply_text("❌ Pehle aapko hamara main channel join karna hoga.", reply_markup=join_button)
    query.answer()

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
