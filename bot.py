from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
import os
import asyncio

MAIN_CHANNEL_ID = -1002441344477

channel_links = [
    ("🔞 Jav Nation", "https://t.me/+A5sllB-vY4diNzk9"),
    ("🥵 Jav Collection", "https://t.me/+A5sllB-vY4diNzk9"),
    ("🔥 OnlyFans Nation", "https://t.me/+IO7rG_j0CFE3NDg9"),
    ("💀 OnlyFans Collection", "https://t.me/+IO7rG_j0CFE3NDg9"),
    ("💖 Favhouse Nation", "https://t.me/+4X0ep0FK_lc2Nzg1"),
    ("🩷 Favhouse Collection", "https://t.me/+4X0ep0FK_lc2Nzg1"),
]

async def is_user_joined(user_id, context):
    member = await context.bot.get_chat_member(chat_id=MAIN_CHANNEL_ID, user_id=user_id)
    return member.status not in ["left", "kicked"]

def get_join_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Pehle Channel Join Karein", url="https://t.me/unseentabs")],
        [InlineKeyboardButton("🔄 Dobara Try Karein", callback_data="check_join")]
    ])

def get_channel_markup():
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, url=url)] for text, url in channel_links])

def get_start_markup():
    return InlineKeyboardMarkup([[InlineKeyboardButton("▶ Start", callback_data="start_again")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if await is_user_joined(user.id, context):
        sent_message = await update.message.reply_text(
            "✅ Aap ne channel join kar liya hai. Ab niche se category select karein:",
            reply_markup=get_channel_markup()
        )
        asyncio.create_task(remove_categories_after_delay(sent_message, context))
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
        sent_message = await query.message.reply_text(
            "✅ Aap ne channel join kar liya hai. Ab niche se category select karein:",
            reply_markup=get_channel_markup()
        )
        asyncio.create_task(remove_categories_after_delay(sent_message, context))
    else:
        await query.message.reply_text(
            "⚠️ Pehle aapko hamara main channel join karna hoga.",
            reply_markup=get_join_markup()
        )

async def remove_categories_after_delay(message, context):
    await asyncio.sleep(60)  # 1 minute delay

    # Purane messages delete karna
    try:
        chat_id = message.chat_id
        last_msg_id = message.message_id
        for msg_id in range(last_msg_id, max(last_msg_id - 20, 0), -1):
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
    except:
        pass

    # Naya start button bhejna
    await context.bot.send_message(
        chat_id=message.chat_id,
        text="▶ Bot dobara start karne ke liye button dabayein:",
        reply_markup=get_start_markup()
    )

async def start_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if await is_user_joined(user.id, context):
        sent_message = await query.message.reply_text(
            "✅ Aap ne channel join kar liya hai. Ab niche se category select karein:",
            reply_markup=get_channel_markup()
        )
        asyncio.create_task(remove_categories_after_delay(sent_message, context))
    else:
        await query.message.reply_text(
            "⚠️ Pehle aapko hamara main channel join karna hoga.",
            reply_markup=get_join_markup()
        )

# ✅ Railway Compatible Start Block
if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("❌ BOT_TOKEN not found in Railway Variables.")
    else:
        app = ApplicationBuilder().token(token).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
        app.add_handler(CallbackQueryHandler(start_again, pattern="start_again"))

        print("✅ Bot is running...")
        app.run_polling(stop_signals=None)
