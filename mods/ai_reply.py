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
    """Register EAGLESPY AI auto-reply handlers."""

    @app.on_message(
        filters.incoming
        & filters.private
        & ~filters.bot
        & ~filters.service
    )
    async def auto_reply_handler(client: Client, message: Message):

        print(
            f"[DEBUG] Message received | "
            f"chat_id={message.chat.id} | "
            f"type={message.chat.type} | "
            f"text={message.text!r}",
            flush=True
        )

        if not AUTO_REPLY_ENABLED:
            print(
                "[DEBUG] Auto-reply disabled by config",
                flush=True
            )
            return

        if ONLY_PRIVATE and message.chat.type.name != "PRIVATE":
            print(
                "[DEBUG] Message rejected: not private",
                flush=True
            )
            return

        # Ignore messages from self
        if message.from_user and message.from_user.is_self:
            print(
                "[DEBUG] Message rejected: self message",
                flush=True
            )
            return

        user_id = (
            message.from_user.id
            if message.from_user
            else message.chat.id
        )

        text = message.text or message.caption or ""

        if not text.strip():
            print(
                "[DEBUG] Message rejected: empty text",
                flush=True
            )
            return

        is_owner = user_id == OWNER_ID

        print(
            f"[DEBUG] Processing message | "
            f"user_id={user_id} | "
            f"is_owner={is_owner}",
            flush=True
        )

        # Natural delay
        delay = random.uniform(
            REPLY_DELAY_MIN,
            REPLY_DELAY_MAX
        )

        print(
            f"[DEBUG] Waiting {delay:.2f}s before reply",
            flush=True
        )

        await asyncio.sleep(delay)

        # Show typing
        print(
            "[DEBUG] Sending typing action",
            flush=True
        )

        await client.send_chat_action(
            message.chat.id,
            ChatAction.TYPING
        )

        await asyncio.sleep(
            random.uniform(0.8, 1.0)
        )

        print(
            "[DEBUG] Calling generate_reply()",
            flush=True
        )

        reply = await generate_reply(
            user_id,
            text,
            is_owner=is_owner
        )

        print(
            f"[DEBUG] generate_reply() returned: "
            f"{reply!r}",
            flush=True
        )

        if reply:
            await message.reply(reply)

            print(
                "[DEBUG] Reply sent successfully",
                flush=True
            )

    # =========================
    # Clear memory
    # =========================

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
        """Clear conversation memory for a user."""

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
                await message.reply(
                    "Invalid user_id"
                )
                return

        await db.clear_history(target)

        await message.reply(
            f"🧹 Memory cleared for `{target}`"
        )

    # =========================
    # Notes
    # =========================

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
        """Set notes for a user."""

        parts = message.text.split(maxsplit=2)

        if len(parts) < 3:
            await message.reply(
                "Usage: `.note <user_id> <notes>`"
            )
            return

        try:
            target = int(parts[1])

        except ValueError:
            await message.reply(
                "Invalid user_id"
            )
            return

        notes = parts[2]

        await db.set_notes(
            target,
            notes
        )

        await message.reply(
            f"📝 Notes saved for `{target}`"
        )

    # =========================
    # Ping
    # =========================

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
            "🏓 Pong! EAGLESPY is alive."
        )

    print(
        "[Mod] EAGLESPY AI Auto-Reply loaded",
        flush=True
    )
