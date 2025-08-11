# Implementation Guide (Milestone 1)

## Key components
- **Flask (free, open source):** exposes `/webhook` for Telegram to POST updates.
- **python-telegram-bot (free, open source):** handles Telegram updates & commands.
- **MongoDB:** stores user profiles. Use local `mongod` (free) or Atlas (free tier available).
- **ngrok / Cloudflare Tunnel:** provides a public HTTPS URL to your local app so Telegram can reach it.

## Why a webhook?
Telegram needs a public HTTPS endpoint to push updates. Polling works too, but webhooks are lower-latency and production-friendly.

## Free vs paid
- **Flask / python-telegram-bot:** free, permissive licenses.
- **MongoDB:** free locally; Atlas has a free tier.
- **ngrok:** has a free tier with a temporary URL (rotates on restart). Alternatives: **Cloudflare Tunnel** (free), **LocalTunnel** (free). Pick any; steps are similar.

## Environment variables explained
- **BOT_TOKEN:** Secret token Telegram uses to authenticate requests to the Bot API on your behalf. Obtain it from **BotFather**.
- **DB_BACKEND:** Choose your DB layer. Default is `mongo`.
- **MONGO_URI:** Connection string to your MongoDB (local or Atlas). Example: `mongodb://localhost:27017/botzilla`.
- **SQLITE_PATH:** Path to SQLite file if you pick `sqlite` backend (not needed for Mongo).
- **ADMIN_IDS / DEVELOPER_IDS:** Numeric Telegram user IDs who can access restricted commands. Separate by commas.
- **PUBLIC_URL:** Public base URL where your app is reachable. Used only when calling `setWebhook`.
- **LOG_LEVEL:** Controls verbosity of logs.

## How to obtain values
1. **BOT_TOKEN:** Chat with `@BotFather` in Telegram → `/newbot` → follow prompts → copy the token.
2. **ADMIN_IDS / DEVELOPER_IDS:** Your numeric Telegram user ID. If you don't know it, start a chat with `@userinfobot` or add a temporary handler to print `update.effective_user.id`.
3. **MONGO_URI:**
   - Local: `mongodb://localhost:27017/botzilla` (ensure `mongod` is running).
   - Atlas: Create a free cluster → get the connection string → replace `<username>`/`<password>`.
4. **PUBLIC_URL:**
   - ngrok: run `ngrok http 5000` → copy the generated `https://...ngrok-free.app` URL.
   - Cloudflare Tunnel: run `cloudflared tunnel --url http://localhost:5000` (see docs), copy the public URL.

## Running locally
1. Create and activate a venv; install requirements.
2. Copy `.env.example` → `.env` and fill values.
3. Run `make run` to start Flask + PTB.
4. Start your tunnel and set the webhook.
5. Test `/start` and `/admin_status`.

## Security notes
- Never commit `.env` with secrets.
- Logs are JSON and omit secrets by design.
- Admin commands are gated by ID allowlists.

## Troubleshooting
- **Webhook not firing:** check tunnel is running and `PUBLIC_URL` matches; verify `/healthz` returns 200.
- **Mongo connection errors:** ensure `mongod` is running or correct Atlas IP allowlist.
- **403 on /admin_status:** confirm your Telegram numeric ID is in `ADMIN_IDS`.
