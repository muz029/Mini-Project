import os
import sys
import requests

TOKEN = os.getenv("BOT_TOKEN")
PUBLIC_URL = os.getenv("PUBLIC_URL")  # e.g., https://abcd-1234.ngrok-free.app

if not TOKEN or not PUBLIC_URL:
    print("BOT_TOKEN and PUBLIC_URL env vars are required", file=sys.stderr)
    sys.exit(1)

url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
resp = requests.post(url, json={"url": f"{PUBLIC_URL}/webhook"})
print(resp.status_code, resp.text)
