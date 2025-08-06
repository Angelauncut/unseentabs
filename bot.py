from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

BOT_TOKEN = "8288634287:AAF1jpfEt3CMDExMidVw6qp3Jo5iZg1uwIU"
MAIN_CHANNEL = "@unseentabs"
MAIN_CHANNEL_LINK = "https://t.me/unseentabs"

# Links
JAV_LINK = "https://t.me/+A5sllB-vY4diNzk9"
OF_LINK = "https://t.me/+IO7rG_j0CFE3NDg9"
FAV_LINK = "https://t.me/+4X0ep0FK_lc2Nzg1"

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    try:
        member = context.bot.get_chat_member(MAIN_CHANNEL, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            keyboard = [
                [InlineKeyboardButton("🔞 Jav Nation", callback_data="jav")],
                [InlineKeyboardButton("🔥 OnlyFans Nation", callback_data="of")],
                [InlineKeyboardButton("💖 Favhouse Nation", callback_data="fav")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("✅ Aap ne channel join kar liya hai.\nAb niche se category select karein:", reply_markup=reply_markup)
        else:
            raise Exception("Not joined")
    except:
        join_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("👉 Pehle Unseen Tabs Join Karo", url=MAIN_CHANNEL_LINK)]
        ])
        update.message.reply_text("❌ Pehle aapko hamara main channel join karna hoga.", reply_markup=join_button)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

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