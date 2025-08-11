import os
import json
import atexit
import logging
import asyncio
from datetime import datetime
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application

# Local modules
from storage.sqlite import SQLiteStorage
try:
    from storage.mongo import MongoStorage
except Exception:
    MongoStorage = None
from handlers.start import register_start_handlers
from handlers.admin import register_admin_handlers

load_dotenv()

# ----- Logging (JSON) -----
class JsonFormatter(logging.Formatter):
    def format(self, record):
        base = {
            "level": record.levelname,
            "message": record.getMessage(),
            "time": datetime.utcnow().isoformat() + "Z",
            "logger": record.name,
        }
        if record.exc_info:
            base["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(base)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), handlers=[handler])
log = logging.getLogger("botzilla")

# ----- Config -----
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise SystemExit("BOT_TOKEN is required in .env")

DB_BACKEND = os.getenv("DB_BACKEND", "mongo").lower()  # default: mongo
ADMIN_IDS = {int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()}
DEVELOPER_IDS = {int(x.strip()) for x in os.getenv("DEVELOPER_IDS", "").split(",") if x.strip()}

# ----- Storage -----
if DB_BACKEND == "mongo":
    if not MongoStorage:
        raise SystemExit("Mongo backend selected but dependencies not available")
    STORAGE = MongoStorage(os.getenv("MONGO_URI", "mongodb://localhost:27017/botzilla"))
else:
    STORAGE = SQLiteStorage(os.getenv("SQLITE_PATH", "botzilla.db"))

# ----- Telegram Application -----
application = Application.builder().token(TOKEN).build()

# Inject shared state
application.bot_data["storage"] = STORAGE
application.bot_data["admin_ids"] = ADMIN_IDS
application.bot_data["developer_ids"] = DEVELOPER_IDS

# Register handlers
register_start_handlers(application)
register_admin_handlers(application)

# ----- Flask App -----
flask_app = Flask(__name__)

@flask_app.get("/healthz")
def healthz():
    return jsonify({"ok": True, "backend": DB_BACKEND}), 200

@flask_app.post("/webhook")
def webhook():
    if request.headers.get("content-type") != "application/json":
        abort(415)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400)
    update = Update.de_json(data, application.bot)
    # Process the update via PTB in the current thread/event loop
    asyncio.get_event_loop().run_until_complete(application.process_update(update))
    return "", 204

# Initialize and start PTB once on startup
async def _ptb_start():
    await application.initialize()
    await application.start()
    log.info("PTB application started")

async def _ptb_stop():
    await application.stop()
    await application.shutdown()
    log.info("PTB application stopped")

# Ensure proper PTB lifecycle when running this module directly
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_ptb_start())

    def _on_exit():
        try:
            loop.run_until_complete(_ptb_stop())
        except Exception as e:
            log.error(f"PTB shutdown error: {e}")
    atexit.register(_on_exit)

    port = int(os.getenv("PORT", 5000))
    log.info(f"Starting Flask on :{port}")
    flask_app.run(host="0.0.0.0", port=port)
