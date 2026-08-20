import traceback

from openai import AsyncOpenAI

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    AI_SYSTEM_PROMPT,
    DEFAULT_SYSTEM_PROMPT,
    OWNER_ID,
)

from core.database import db


# =========================
# Groq / OpenAI-compatible client
# =========================

client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


# =========================
# Generate AI reply
# =========================

async def generate_reply(
    user_id: int,
    user_message: str,
    is_owner: bool = False
) -> str:

    """Generate AI reply per-user and owner special handling."""

    history = await db.get_history(user_id)
    notes = await db.get_notes(user_id)

    system_prompt = (
        AI_SYSTEM_PROMPT
        or DEFAULT_SYSTEM_PROMPT
    )

    # -------------------------
    # Owner special instructions
    # -------------------------

    if is_owner:

        system_prompt += """
You are talking to your owner.

Use respect + close friend jaisa treat kar.

Galat mat de (halka mazaki hai).

Uske orders follow kar.
"""

    else:

        system_prompt += f"""
Current user relationship:
{notes.get('relationship', 'unknown')}

User notes:
{notes.get('notes', 'None')}

Agar Owner ke baare mein pooche to positive aur thoda cod tareeke se bata,
private baatein mat khol.
"""

    # -------------------------
    # Build messages
    # -------------------------

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # Add conversation history
    for msg in history:
        messages.append(msg)

    # Add current user message
    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # -------------------------
    # Save user message FIRST
    # -------------------------

    try:
        await db.add_message(
            user_id,
            "user",
            user_message
        )

    except Exception as e:
        print(
            f"[DB Error] Could not save user message: "
            f"{type(e).__name__}: {e}",
            flush=True
        )

    # -------------------------
    # Ask Groq
    # -------------------------

    try:

        print(
            f"[AI] Sending request | "
            f"user_id={user_id} | "
            f"model={GROQ_MODEL}",
            flush=True
        )

        response = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.85,
            max_tokens=512,
            top_p=0.9,
        )

        reply = (
            response.choices[0]
            .message
            .content
            .strip()
        )

        # -------------------------
        # Save assistant reply
        # -------------------------

        try:

            await db.add_message(
                user_id,
                "assistant",
                reply
            )

        except Exception as e:

            print(
                f"[DB Error] Could not save AI reply: "
                f"{type(e).__name__}: {e}",
                flush=True
            )

        print(
            f"[AI] Reply generated successfully | "
            f"user_id={user_id}",
            flush=True
        )

        return reply

    # -------------------------
    # AI error
    # -------------------------

    except Exception as e:

        print(
            "==============================",
            flush=True
        )

        print(
            "[AI ERROR]",
            flush=True
        )

        print(
            f"Type: {type(e).__name__}",
            flush=True
        )

        print(
            f"Message: {e}",
            flush=True
        )

        traceback.print_exc()

        print(
            "==============================",
            flush=True
        )

        return (
            "Thoda busy hoon abhi, "
            "thodi der baad try karna 😅"
        )
