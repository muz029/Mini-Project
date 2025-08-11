from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

TC_AGREE = "tc_agree"
TC_DECLINE = "tc_decline"

WELCOME = (
    "👋 Welcome to BotZilla!\n\n"
    "Before we continue, please review and accept our Terms & Conditions to use the bot."
)

TC_TEXT = (
    "📄 **Terms & Conditions (summary)**\n\n"
    "• This bot is for educational use for now.\n"
    "• You are responsible for your trading decisions.\n"
    "• We do not store your Telegram messages beyond what’s required for operations.\n\n"
    "Do you accept?"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    storage = context.application.bot_data["storage"]
    u = update.effective_user
    # Upsert user on first interaction
    storage.upsert_user(
        telegram_id=u.id,
        username=(u.username or ""),
        first_name=(u.first_name or ""),
        last_name=(u.last_name or ""),
        profile_pic_url="",  # can be fetched later via getUserProfilePhotos
        joined_at=datetime.utcnow().isoformat() + "Z",
        status="unverified",
    )
    # Send welcome + T&C
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ I Agree", callback_data=TC_AGREE),
                InlineKeyboardButton("❌ I Do Not Agree", callback_data=TC_DECLINE),
            ]
        ]
    )
    await update.effective_chat.send_message(WELCOME)
    await update.effective_chat.send_message(TC_TEXT, reply_markup=kb)

async def on_tc_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    storage = context.application.bot_data["storage"]
    query = update.callback_query
    await query.answer()

    if query.data == TC_AGREE:
        storage.update_status(update.effective_user.id, "verified")
        await query.edit_message_text("✅ Thanks! You’re verified and ready to go.")
    else:
        await query.edit_message_text("❗ Understood. You can /start again anytime.")

# Pure function for tests

def handle_consent(storage, telegram_id: int, agree: bool):
    if agree:
        storage.update_status(telegram_id, "verified")
        return "verified"
    return "unverified"


def register_start_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_tc_callback, pattern=f"^({TC_AGREE}|{TC_DECLINE})$"))
