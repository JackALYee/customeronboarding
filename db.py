"""SQLite helpers for the onboarding portal.

Tables:
- customers: known customers — staff-created (audience set at creation time)
- login_codes: short-lived 6-digit verification codes for email login
- login_events: append-only audit log of successful logins (for the staff dashboard)
"""
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "onboarding.db"

# Built-in test client account — used by the test login bypass.
# Pre-seeded so the staff dashboard sees a real customer row from day 1.
TEST_CLIENT_EMAIL = "test@onboarding.local"
TEST_CLIENT_COMPANY = "Test Client (built-in)"
TEST_CLIENT_AUDIENCE = "fleet"


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
                created_at TEXT,
                created_by TEXT,
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

            CREATE TABLE IF NOT EXISTS login_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                method TEXT NOT NULL,
                logged_in_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_login_events_email ON login_events(email);
            """
        )

    # Migrate older databases that pre-date `created_at` / `created_by`.
    with _conn() as con:
        cols = {r["name"] for r in con.execute("PRAGMA table_info(customers)")}
        if "created_at" not in cols:
            con.execute("ALTER TABLE customers ADD COLUMN created_at TEXT")
        if "created_by" not in cols:
            con.execute("ALTER TABLE customers ADD COLUMN created_by TEXT")


def seed_test_accounts() -> None:
    """Idempotently insert the built-in test client row so the staff
    dashboard shows it from day 1. The test_staff account is a hard-coded
    credential check in login.py — no row needed."""
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        existing = con.execute(
            "SELECT email FROM customers WHERE email = ?", (TEST_CLIENT_EMAIL,)
        ).fetchone()
        if not existing:
            con.execute(
                """INSERT INTO customers
                   (email, company, audience, created_at, created_by)
                   VALUES (?, ?, ?, ?, ?)""",
                (TEST_CLIENT_EMAIL, TEST_CLIENT_COMPANY, TEST_CLIENT_AUDIENCE, now, "system:seed"),
            )


# --- Login codes ----------------------------------------------------------

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


# --- Customers ------------------------------------------------------------

def get_customer(email: str):
    with _conn() as con:
        return con.execute("SELECT * FROM customers WHERE email = ?", (email.lower(),)).fetchone()


def create_customer(email: str, company: str, audience: str, created_by: str) -> bool:
    """Staff-side create. Returns False if the email already exists."""
    email = email.lower()
    now = datetime.utcnow().isoformat()
    audience = audience if audience in ("fleet", "tsp") else "fleet"
    with _conn() as con:
        existing = con.execute("SELECT email FROM customers WHERE email = ?", (email,)).fetchone()
        if existing:
            return False
        con.execute(
            """INSERT INTO customers
               (email, company, audience, created_at, created_by)
               VALUES (?, ?, ?, ?, ?)""",
            (email, company, audience, now, created_by),
        )
        return True


def update_customer_audience(email: str, audience: str) -> None:
    if audience not in ("fleet", "tsp"):
        return
    with _conn() as con:
        con.execute("UPDATE customers SET audience = ? WHERE email = ?", (audience, email.lower()))


def delete_customer(email: str) -> None:
    with _conn() as con:
        con.execute("DELETE FROM customers WHERE email = ?", (email.lower(),))


def mark_login(email: str) -> None:
    """Updates first_login_at (if null) + last_login_at."""
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        row = con.execute(
            "SELECT first_login_at FROM customers WHERE email = ?", (email.lower(),)
        ).fetchone()
        if not row:
            return
        if row["first_login_at"]:
            con.execute("UPDATE customers SET last_login_at = ? WHERE email = ?", (now, email.lower()))
        else:
            con.execute(
                "UPDATE customers SET first_login_at = ?, last_login_at = ? WHERE email = ?",
                (now, now, email.lower()),
            )


def list_customers():
    with _conn() as con:
        return list(
            con.execute(
                "SELECT email, company, audience, created_at, first_login_at, last_login_at "
                "FROM customers ORDER BY created_at DESC NULLS LAST, email"
            )
        )


# --- Login events (audit log) --------------------------------------------

def log_login(email: str, role: str, method: str) -> None:
    """role: 'customer' | 'staff'   method: 'email_code' | 'test_bypass' | 'staff_credential'"""
    with _conn() as con:
        con.execute(
            "INSERT INTO login_events (email, role, method, logged_in_at) VALUES (?, ?, ?, ?)",
            (email.lower(), role, method, datetime.utcnow().isoformat()),
        )


def recent_logins(limit: int = 50):
    with _conn() as con:
        return list(
            con.execute(
                "SELECT email, role, method, logged_in_at FROM login_events "
                "ORDER BY id DESC LIMIT ?",
                (limit,),
            )
        )


def count_logins() -> int:
    with _conn() as con:
        row = con.execute("SELECT COUNT(*) AS n FROM login_events").fetchone()
        return int(row["n"]) if row else 0
