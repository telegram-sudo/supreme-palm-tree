"""
Generate Pyrogram / Kurigram session string.
Run this locally once:
    python session_gen.py
Then copy the session string into your .env / Render environment variables.
"""

from pyrogram import Client
from config import API_ID, API_HASH

async def main():
    async with Client(
        name="hazelai_gen",
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True,
    ) as app:
        session_string = await app.export_session_string()
        print("\n" + "=" * 50)
        print("YOUR SESSION STRING (copy this):")
        print("=" * 50)
        print(session_string)
        print("=" * 50)
        print("\nAdd this as SESSION_STRING in your .env or Render env vars.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())