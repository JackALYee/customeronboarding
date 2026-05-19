"""SQLite helpers for the onboarding portal.

Tables:
- customers: known customers, staff-created. Each has a password_hash.
- login_events: append-only audit log of successful logins.
"""
import hashlib
import hmac
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "onboarding.db"

# Built-in test client account — seeded on app start, used by the
# `test` / `testme` login bypass. Email is synthetic so it can't
# collide with a real customer.
TEST_CLIENT_EMAIL = "test@onboarding.local"
TEST_CLIENT_COMPANY = "Test Client (built-in)"
TEST_CLIENT_AUDIENCE = "fleet"
TEST_CLIENT_PASSWORD = "testme"


# --- Password hashing (PBKDF2-SHA256, stdlib only) ------------------------
#
# Format stored in DB: "pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>"
# Iterations are kept moderate so the staff dashboard and login UI stay
# snappy on Streamlit Cloud's free tier. Bump later if the threat model
# tightens.
_PBKDF2_ITERATIONS = 120_000


def hash_password(plain: str) -> str:
    salt = os.urandom(16)
    h = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt, _PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${_PBKDF2_ITERATIONS}${salt.hex()}${h.hex()}"


def verify_password(plain: str, stored: str) -> bool:
    if not stored or not stored.startswith("pbkdf2_sha256$"):
        return False
    try:
        _algo, iters_s, salt_hex, hash_hex = stored.split("$", 3)
        iters = int(iters_s)
        expected = bytes.fromhex(hash_hex)
        salt = bytes.fromhex(salt_hex)
    except (ValueError, AttributeError):
        return False
    computed = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt, iters)
    # Constant-time compare
    return hmac.compare_digest(computed, expected)


# --- Connection -----------------------------------------------------------

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
                password_hash TEXT,
                created_at TEXT,
                created_by TEXT,
                first_login_at TEXT,
                last_login_at TEXT
            );

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

    # Migrate older databases that pre-date the new columns.
    with _conn() as con:
        cols = {r["name"] for r in con.execute("PRAGMA table_info(customers)")}
        if "created_at" not in cols:
            con.execute("ALTER TABLE customers ADD COLUMN created_at TEXT")
        if "created_by" not in cols:
            con.execute("ALTER TABLE customers ADD COLUMN created_by TEXT")
        if "password_hash" not in cols:
            con.execute("ALTER TABLE customers ADD COLUMN password_hash TEXT")


def seed_test_accounts() -> None:
    """Idempotently insert the built-in test client row + ensure its
    password is set. The staff bypass (`test_staff` / `testme`) is a
    hardcoded credential check in login.py, no row needed."""
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        row = con.execute(
            "SELECT email, password_hash FROM customers WHERE email = ?", (TEST_CLIENT_EMAIL,)
        ).fetchone()
        if not row:
            con.execute(
                """INSERT INTO customers
                   (email, company, audience, password_hash, created_at, created_by)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    TEST_CLIENT_EMAIL,
                    TEST_CLIENT_COMPANY,
                    TEST_CLIENT_AUDIENCE,
                    hash_password(TEST_CLIENT_PASSWORD),
                    now,
                    "system:seed",
                ),
            )
        elif not row["password_hash"]:
            # Row exists from an older db without a password — set it now.
            con.execute(
                "UPDATE customers SET password_hash = ? WHERE email = ?",
                (hash_password(TEST_CLIENT_PASSWORD), TEST_CLIENT_EMAIL),
            )


# --- Customer helpers -----------------------------------------------------

def get_customer(email: str):
    with _conn() as con:
        return con.execute(
            "SELECT * FROM customers WHERE email = ?", (email.lower(),)
        ).fetchone()


def authenticate(email: str, password: str):
    """Return the customer row if email + password match, else None."""
    row = get_customer(email)
    if not row:
        return None
    if not verify_password(password, row["password_hash"] or ""):
        return None
    return row


def create_customer(email: str, company: str, audience: str, password: str, created_by: str) -> bool:
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
               (email, company, audience, password_hash, created_at, created_by)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (email, company, audience, hash_password(password), now, created_by),
        )
        return True


def reset_password(email: str, new_password: str) -> bool:
    with _conn() as con:
        cur = con.execute(
            "UPDATE customers SET password_hash = ? WHERE email = ?",
            (hash_password(new_password), email.lower()),
        )
        return cur.rowcount > 0


def update_customer_audience(email: str, audience: str) -> None:
    if audience not in ("fleet", "tsp"):
        return
    with _conn() as con:
        con.execute("UPDATE customers SET audience = ? WHERE email = ?", (audience, email.lower()))


def delete_customer(email: str) -> None:
    with _conn() as con:
        con.execute("DELETE FROM customers WHERE email = ?", (email.lower(),))


def mark_login(email: str) -> None:
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
    """role: 'customer' | 'staff'   method: 'password' | 'test_bypass' | 'staff_credential'"""
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
