from pyrogram import Client
from config import API_ID, API_HASH, SESSION_STRING

def create_client() -> Client:
    """Create and return the main userbot client."""
    if not SESSION_STRING:
        raise ValueError("SESSION_STRING is required. Generate it using session_gen.py")

    client = Client(
        name="hazelai_userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING,
        in_memory=True,  # Better for Render / cloud
        workers=4,
    )
    return client