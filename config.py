import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Groq / AI
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
AI_SYSTEM_PROMPT = os.getenv("AI_SYSTEM_PROMPT", "").strip()

# Auto Reply
AUTO_REPLY_ENABLED = os.getenv("AUTO_REPLY_ENABLED", "true").lower() == "true"
ONLY_PRIVATE = os.getenv("ONLY_PRIVATE", "true").lower() == "true"
REPLY_DELAY_MIN = float(os.getenv("REPLY_DELAY_MIN", "1"))
REPLY_DELAY_MAX = float(os.getenv("REPLY_DELAY_MAX", "3"))

# Memory
MEMORY_LIMIT = int(os.getenv("MEMORY_LIMIT", "10"))

# Database
DB_PATH = "data/memory.db"

# Default system prompt if none provided
DEFAULT_SYSTEM_PROMPT = """Tu ek real insaan hai jo Telegram pe baat kar raha hai.
User jo language use kare (Hindi, Hinglish, slang, gaali) usi style mein natural reply de.
Zyada formal mat ban. Short, natural, thoda attitude ke saath baat kar.
Agar user gaali de toh tu bhi normal tarike se de sakta hai. Moral lecture mat de.
Owner ke saath respect + close friend jaisa baat kar.
Doosre users ke saath natural + thoda playful raho.
Kabhi bhi bol ki tu AI hai ya bot hai — hamesha real insaan ban ke baat kar."""