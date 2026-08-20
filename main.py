import asyncio
import os
from pyrogram import idle
from core.client import create_client
from core.database import db
from mods.ai_reply import register as register_ai_reply

# Optional: keep alive for Render free tier
from flask import Flask
import threading

app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "HazelAI Userbot is running ✅"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)


async def main():
    # Initialize database
    os.makedirs("data", exist_ok=True)
    await db.init()
    print("[DB] Memory database ready")

    # Create client
    client = create_client()

    # Load mods
    register_ai_reply(client)

    # Start
    await client.start()
    me = await client.get_me()
    print(f"[HazelAI] Logged in as {me.first_name} (@{me.username}) | ID: {me.id}")
    print("[HazelAI] Userbot is running... Press Ctrl+C to stop.")

    await idle()
    await client.stop()


if __name__ == "__main__":
    # Start Flask in background (for Render health check)
    threading.Thread(target=run_flask, daemon=True).start()

    # Run userbot
    asyncio.run(main())