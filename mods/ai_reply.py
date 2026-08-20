import asyncio
import random

from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatAction

from config import (
    OWNER_ID,
    AUTO_REPLY_ENABLED,
    ONLY_PRIVATE,
    REPLY_DELAY_MIN,
    REPLY_DELAY_MAX,
)

from core.ai import generate_reply
from core.database import db


def register(app: Client):
    """Register AI auto-reply handlers."""

    @app.on_message(
        filters.incoming
        & filters.private
        & ~filters.bot
        & ~filters.service
    )
    async def auto_reply_handler(client: Client, message: Message):

        if not AUTO_REPLY_ENABLED:
            return

        if ONLY_PRIVATE and message.chat.type.name != "PRIVATE":
            return

        # Ignore messages from self
        if message.from_user and message.from_user.is_self:
            return

        user_id = (
            message.from_user.id
            if message.from_user
            else message.chat.id
        )

        text = message.text or message.caption or ""

        if not text.strip():
            return

        is_owner = user_id == OWNER_ID

        # Natural delay (looks more human)
        delay = random.uniform(
            REPLY_DELAY_MIN,
            REPLY_DELAY_MAX
        )

        await asyncio.sleep(delay)

        # Show typing
        await client.send_chat_action(
            message.chat.id,
            ChatAction.TYPING
        )

        await asyncio.sleep(
            random.uniform(0.8, 1.0)
        )

        reply = await generate_reply(
            user_id,
            text,
            is_owner=is_owner
        )

        if reply:
            await message.reply(reply)

    @app.on_message(
        filters.command(
            "clear",
            prefixes=[".", "/", "!"]
        )
        & filters.me
    )
    async def clear_memory(
        client: Client,
        message: Message
    ):
        """Clear conversation memory for a user.
        Usage: .clear (reply to user) or .clear <user_id>
        """

        if (
            message.reply_to_message
            and message.reply_to_message.from_user
        ):
            target = message.reply_to_message.from_user.id

        else:
            parts = message.text.split(maxsplit=1)

            if len(parts) < 2:
                await message.reply(
                    "Usage: `.clear` (reply) or `.clear <user_id>`"
                )
                return

            try:
                target = int(parts[1])

            except ValueError:
                await message.reply("Invalid user_id")
                return

        await db.clear_history(target)

        await message.reply(
            f"🧹 Memory cleared for `{target}`"
        )

    @app.on_message(
        filters.command(
            "note",
            prefixes=[".", "/", "!"]
        )
        & filters.me
    )
    async def set_note(
        client: Client,
        message: Message
    ):
        """Set notes for a user.
        Usage: .note <user_id> <notes>
        """

        parts = message.text.split(maxsplit=2)

        if len(parts) < 3:
            await message.reply(
                "Usage: `.note <user_id> <notes>`"
            )
            return

        try:
            target = int(parts[1])

        except ValueError:
            await message.reply("Invalid user_id")
            return

        notes = parts[2]

        await db.set_notes(target, notes)

        await message.reply(
            f"📝 Notes saved for `{target}`"
        )

    @app.on_message(
        filters.command(
            "ping",
            prefixes=[".", "/", "!"]
        )
        & filters.me
    )
    async def ping(
        client: Client,
        message: Message
    ):
        await message.reply(
            "🏓 Pong! HazelAI is alive."
        )

    print("[Mod] AI Auto-Reply loaded")
