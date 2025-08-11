from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

# Role-check decorator

def restricted(role: str = "admin"):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            uid = update.effective_user.id
            admins = context.application.bot_data.get("admin_ids", set())
            devs = context.application.bot_data.get("developer_ids", set())
            allowed = (uid in admins) or (role == "developer" and uid in devs)
            if not allowed:
                await update.effective_chat.send_message("⛔ This command is restricted.")
                return
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator

@restricted("admin")
async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    storage = context.application.bot_data["storage"]
    count = storage.count_users()
    await update.effective_chat.send_message(f"📊 Users in DB: {count}")


def register_admin_handlers(app):
    app.add_handler(CommandHandler("admin_status", status_cmd))
