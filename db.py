"""SQLite helpers for the onboarding portal.

Two tables:
- customers: known customers (email, company, audience type, last login)
- login_codes: short-lived 6-digit verification codes
"""
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "onboarding.db"


@contextmanager
def _conn():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def init_db() -> None:
    with _conn() as con:
        con.executescript(
            """
            CREATE TABLE IF NOT EXISTS customers (
                email TEXT PRIMARY KEY,
                company TEXT,
                audience TEXT DEFAULT 'fleet',
                first_login_at TEXT,
                last_login_at TEXT
            );

            CREATE TABLE IF NOT EXISTS login_codes (
                email TEXT NOT NULL,
                code TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                used INTEGER DEFAULT 0
            );

            CREATE INDEX IF NOT EXISTS idx_login_codes_email ON login_codes(email);
            """
        )


def save_code(email: str, code: str, expires_at: str) -> None:
    with _conn() as con:
        con.execute(
            "INSERT INTO login_codes (email, code, created_at, expires_at, used) VALUES (?, ?, ?, ?, 0)",
            (email.lower(), code, datetime.utcnow().isoformat(), expires_at),
        )


def verify_code(email: str, code: str) -> bool:
    """Return True if the code matches an unused, non-expired entry. Marks it used."""
    email = email.lower()
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        row = con.execute(
            """SELECT rowid FROM login_codes
               WHERE email = ? AND code = ? AND used = 0 AND expires_at > ?
               ORDER BY rowid DESC LIMIT 1""",
            (email, code, now),
        ).fetchone()
        if not row:
            return False
        con.execute("UPDATE login_codes SET used = 1 WHERE rowid = ?", (row["rowid"],))
        return True


def upsert_customer(email: str, company: str, audience: str) -> None:
    email = email.lower()
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        existing = con.execute("SELECT email FROM customers WHERE email = ?", (email,)).fetchone()
        if existing:
            con.execute(
                "UPDATE customers SET company = ?, audience = ?, last_login_at = ? WHERE email = ?",
                (company, audience, now, email),
            )
        else:
            con.execute(
                "INSERT INTO customers (email, company, audience, first_login_at, last_login_at) VALUES (?, ?, ?, ?, ?)",
                (email, company, audience, now, now),
            )


def get_customer(email: str):
    with _conn() as con:
        return con.execute("SELECT * FROM customers WHERE email = ?", (email.lower(),)).fetchone()
