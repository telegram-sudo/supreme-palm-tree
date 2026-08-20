import asyncio
import os
import threading

from flask import Flask
from pyrogram import idle

from core.client import create_client
from core.database import db
from mods.ai_reply import register as register_ai_reply


# =========================
# Flask health check
# =========================

app_flask = Flask(__name__)


@app_flask.route("/")
def home():
    return "HazelAI Userbot is running ✅"


def run_flask():
    port = int(os.environ.get("PORT", "10000"))
    app_flask.run(
        host="0.0.0.0",
        port=port
    )


# =========================
# Telegram Userbot
# =========================

async def main():
    print("[HazelAI] main() started", flush=True)

    try:
        # -------------------------
        # Initialize database
        # -------------------------
        os.makedirs("data", exist_ok=True)

        print("[DB] Initializing database...", flush=True)

        await asyncio.wait_for(
            db.init(),
            timeout=10
        )

        print("[DB] Memory database ready", flush=True)

        # -------------------------
        # Create Telegram client
        # -------------------------
        print("[Telegram] Creating client...", flush=True)

        client = create_client()

        # -------------------------
        # Register modules
        # -------------------------
        print("[Telegram] Registering AI module...", flush=True)

        register_ai_reply(client)

        # -------------------------
        # Start Telegram
        # -------------------------
        print("[Telegram] Connecting to Telegram...", flush=True)

        await client.start()

        # -------------------------
        # Get account information
        # -------------------------
        me = await client.get_me()

        print(
            f"[HazelAI] Logged in as "
            f"{me.first_name} "
            f"(@{me.username}) | ID: {me.id}",
            flush=True
        )

        print(
            "[HazelAI] Userbot is running...",
            flush=True
        )

        # -------------------------
        # Keep Telegram running
        # -------------------------
        await idle()

        # -------------------------
        # Stop client cleanly
        # -------------------------
        await client.stop()

    except asyncio.TimeoutError:
        print(
            "[HazelAI] ERROR: Database initialization "
            "timed out after 10 seconds.",
            flush=True
        )
        raise

    except Exception as e:
        print(
            f"[HazelAI] FATAL ERROR: "
            f"{type(e).__name__}: {e}",
            flush=True
        )
        raise


# =========================
# Entry point
# =========================

if __name__ == "__main__":

    # Start Flask health server
    print(
        "[HazelAI] Starting Flask health server...",
        flush=True
    )

    threading.Thread(
        target=run_flask,
        daemon=True
    ).start()

    # Start Telegram userbot
    print(
        "[HazelAI] Starting Telegram event loop...",
        flush=True
    )

    asyncio.run(main())
