import aiosqlite
import json
from config import DB_PATH, MEMORY_LIMIT

class MemoryDB:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    user_id INTEGER PRIMARY KEY,
                    messages TEXT NOT NULL DEFAULT '[]',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_notes (
                    user_id INTEGER PRIMARY KEY,
                    notes TEXT NOT NULL DEFAULT '',
                    relationship TEXT DEFAULT 'unknown'
                )
            """)
            await db.commit()

    async def get_history(self, user_id: int) -> list:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT messages FROM conversations WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return json.loads(row[0])
                return []

    async def add_message(self, user_id: int, role: str, content: str):
        history = await self.get_history(user_id)
        history.append({"role": role, "content": content})

        # Keep only last N messages
        if len(history) > MEMORY_LIMIT * 2:  # user + assistant pairs
            history = history[-(MEMORY_LIMIT * 2):]

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO conversations (user_id, messages, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(user_id) DO UPDATE SET
                    messages = excluded.messages,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (user_id, json.dumps(history, ensure_ascii=False)),
            )
            await db.commit()

    async def clear_history(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM conversations WHERE user_id = ?", (user_id,)
            )
            await db.commit()

    async def set_notes(self, user_id: int, notes: str, relationship: str = "unknown"):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO user_notes (user_id, notes, relationship)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    notes = excluded.notes,
                    relationship = excluded.relationship
                """,
                (user_id, notes, relationship),
            )
            await db.commit()

    async def get_notes(self, user_id: int) -> dict:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT notes, relationship FROM user_notes WHERE user_id = ?",
                (user_id,),
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return {"notes": row[0], "relationship": row[1]}
                return {"notes": "", "relationship": "unknown"}


# Global instance
db = MemoryDB()