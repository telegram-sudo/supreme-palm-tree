# 🌿 HazelAI Userbot

**Personal AI Auto-Reply Userbot** inspired by HazelUB style.

Jab tu offline ho aur koi tujhe private message kare, yeh AI uske style mein (gaali-galoch included) natural reply dega.

---

## ✨ Features

- ✅ **Personal Account Userbot** (Telethon/Pyrogram style via Kurigram)
- ✅ **AI Auto-Reply** (Groq - Llama 3.3 70B)
- ✅ **Per-user Memory** (har user ka alag conversation history)
- ✅ **Owner Special Treatment**
- ✅ **Natural Typing + Delay** (real insaan jaisa)
- ✅ **Modular Plugin System** (`mods/` folder)
- ✅ **Render Ready** (session string + Flask health check)
- ✅ **Clear memory & Notes** commands

---

## 🚀 Quick Setup

### 1. Requirements
- Python 3.10+
- Telegram API_ID + API_HASH → https://my.telegram.org
- Groq API Key → https://console.groq.com

### 2. Install

```bash
git clone <your-repo-url>
cd HazelAI-Userbot
pip install -r requirements.txt
```

### 3. Generate Session String (Local pe ek baar)

```bash
# .env file banao pehle
cp .env.example .env
# API_ID aur API_HASH daalo

python session_gen.py
```

Jo session string aaye usko `.env` mein `SESSION_STRING=` ke saamne paste karo.

### 4. Configure `.env`

```env
API_ID=123456
API_HASH=your_hash
SESSION_STRING=your_session_string
OWNER_ID=your_telegram_user_id
GROQ_API_KEY=gsk_xxxx
GROQ_MODEL=llama-3.3-70b-versatile
AUTO_REPLY_ENABLED=true
ONLY_PRIVATE=true
```

### 5. Run Locally

```bash
python main.py
```

---

## ☁️ Deploy on Render

1. New **Web Service** banao
2. Repo connect karo
3. Build Command:
   ```bash
   pip install -r requirements.txt
   ```
4. Start Command:
   ```bash
   python main.py
   ```
5. Environment Variables mein saari values daalo (API_ID, API_HASH, SESSION_STRING, OWNER_ID, GROQ_API_KEY etc.)

Render free tier pe bhi chal jayega (Flask health check already hai).

---

## 🎮 Commands (Owner only)

| Command | Description |
|---------|-------------|
| `.ping` | Check if alive |
| `.clear` (reply) | Clear memory of that user |
| `.clear <user_id>` | Clear memory by ID |
| `.note <user_id> <text>` | Save notes about a user |

---

## 🧠 How Memory Works

- Har user ka alag conversation history save hota hai (`data/memory.db`)
- Last 10 messages (configurable) yaad rakhta hai
- Owner ke liye alag system prompt apply hota hai

---

## 📁 Project Structure

```
HazelAI-Userbot/
├── main.py              # Entry point
├── config.py            # Settings
├── session_gen.py       # Generate session string
├── requirements.txt
├── .env.example
├── core/
│   ├── client.py        # Pyrogram/Kurigram client
│   ├── database.py      # SQLite memory
│   └── ai.py            # Groq AI logic
└── mods/
    └── ai_reply.py      # Auto-reply plugin
```

---

## ⚠️ Important Notes

- Userbot use karne se Telegram account ban ho sakta hai agar spam kiya.
- Personal use ke liye designed hai.
- Session string ko secret rakho (password jaisa).
- Pehli baar local pe `session_gen.py` chala ke session banao, phir Render pe daalo.

---

Made with ❤️ for personal AI auto-reply needs.