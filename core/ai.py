from openai import AsyncOpenAI
from config import GROQ_API_KEY, GROQ_MODEL, AI_SYSTEM_PROMPT, DEFAULT_SYSTEM_PROMPT, OWNER_ID
from core.database import db

client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

async def generate_reply(user_id: int, user_message: str, is_owner: bool = False) -> str:
    """Generate AI reply with per-user memory and owner special handling."""

    history = await db.get_history(user_id)
    notes_data = await db.get_notes(user_id)

    system_prompt = AI_SYSTEM_PROMPT or DEFAULT_SYSTEM_PROMPT

    # Owner special instructions
    if is_owner:
        system_prompt += """
\n\nYeh message OWNER se aa raha hai.
Usse respect + close friend jaisa treat kar.
Gaali mat de (halki mazaak chal sakti hai).
Uske orders follow kar.
"""
    else:
        system_prompt += f"""
\n\nCurrent user relationship: {notes_data.get('relationship', 'unknown')}
User notes: {notes_data.get('notes', 'None')}
Agar koi Owner ke baare mein pooche toh positive aur thoda cool tareeke se bata, private baatein mat khol.
"""

    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history
    for msg in history:
        messages.append(msg)

    # Add current user message
    messages.append({"role": "user", "content": user_message})

    try:
        response = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.85,
            max_tokens=512,
            top_p=0.9,
        )
        reply = response.choices[0].message.content.strip()

        # Save both user message and assistant reply to memory
        await db.add_message(user_id, "user", user_message)
        await db.add_message(user_id, "assistant", reply)

        return reply

    except Exception as e:
        print(f"[AI Error] {e}")
        return "Thoda busy hoon abhi, thodi der baad try karna 😅"