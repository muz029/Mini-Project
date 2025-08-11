import sqlite3
from typing import Optional

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
  telegram_id INTEGER PRIMARY KEY,
  username TEXT,
  first_name TEXT,
  last_name TEXT,
  profile_pic_url TEXT,
  status TEXT CHECK(status IN ('unverified','verified')) NOT NULL DEFAULT 'unverified',
  joined_at TEXT NOT NULL,
  security_hash TEXT
);
"""

class SQLiteStorage:
    def __init__(self, path: str = "botzilla.db"):
        self.path = path
        with sqlite3.connect(self.path) as c:
            c.execute(SCHEMA)

    def upsert_user(self, telegram_id: int, username: str, first_name: str, last_name: str,
                    profile_pic_url: str, joined_at: str, status: str = "unverified") -> None:
        with sqlite3.connect(self.path) as c:
            c.execute(
                """
                INSERT INTO users (telegram_id, username, first_name, last_name, profile_pic_url, status, joined_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(telegram_id) DO UPDATE SET
                  username=excluded.username,
                  first_name=excluded.first_name,
                  last_name=excluded.last_name
                """,
                (telegram_id, username, first_name, last_name, profile_pic_url, status, joined_at),
            )

    def get_user(self, telegram_id: int) -> Optional[dict]:
        with sqlite3.connect(self.path) as c:
            c.row_factory = sqlite3.Row
            cur = c.execute("SELECT * FROM users WHERE telegram_id=" + "?" + "", (telegram_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def update_status(self, telegram_id: int, status: str) -> None:
        with sqlite3.connect(self.path) as c:
            c.execute("UPDATE users SET status=? WHERE telegram_id=?", (status, telegram_id))

    def count_users(self) -> int:
        with sqlite3.connect(self.path) as c:
            cur = c.execute("SELECT COUNT(*) FROM users")
            return int(cur.fetchone()[0])
