# BotZilla — Milestone 1 (Mongo)

## What this is
A Telegram bot skeleton with webhook, onboarding + T&C, MongoDB persistence, admin command, logging, tests.

## Prereqs
- Python 3.10+
- MongoDB (local `mongod` or MongoDB Atlas free tier)
- An internet-exposed HTTPS URL for webhooks (ngrok free tier or Cloudflare Tunnel)

## Setup
1. python -m venv .venv && source .venv/bin/activate
2. pip install -r requirements.txt
3. cp .env.example .env and fill values (see below)
4. Start MongoDB locally (or provide your Atlas URI in `MONGO_URI`).
5. Start the app: `make run`
6. Start tunnel (e.g. ngrok): `ngrok http 5000`
7. Set Telegram webhook: `BOT_TOKEN=<your token> make set-webhook PUBLIC_URL=https://<your>.ngrok-free.app`
8. DM your bot `/start` in Telegram. Use `/admin_status` from an admin ID.

## Environment variables
- **BOT_TOKEN**: Token from BotFather for your bot. Required.
- **DB_BACKEND**: `mongo` (default) or `sqlite`.
- **MONGO_URI**: e.g. `mongodb://localhost:27017/botzilla` or your Atlas URI.
- **SQLITE_PATH**: Only if using SQLite fallback.
- **ADMIN_IDS**: Comma-separated Telegram user IDs with admin rights.
- **DEVELOPER_IDS**: Comma-separated Telegram user IDs with developer rights.
- **PUBLIC_URL**: Your public HTTPS base URL used to register the webhook (e.g., ngrok URL).
- **LOG_LEVEL**: `INFO` (default), `DEBUG`, etc.

## Make a zip
- Linux/macOS: `make bundle` → `botzilla-m1-mongo.zip`
- Windows (PowerShell): `Compress-Archive -Path app.py,handlers,storage,scripts,tests,docs,README.md,requirements.txt,.env.example,Makefile -DestinationPath botzilla-m1-mongo.zip`
