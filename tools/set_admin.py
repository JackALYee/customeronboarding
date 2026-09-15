#!/usr/bin/env python3
"""Create / reset / remove staff (admin) logins for /admin - run by the owner.

    python3 tools/set_admin.py                 create or reset an admin (prompts; password hidden)
    python3 tools/set_admin.py --list          list admin usernames
    python3 tools/set_admin.py --delete NAME   remove an admin
    python3 tools/set_admin.py --init          only make sure the session-signing key exists
    add --preview to any of the above to target the Preview environment's KV

The password is hashed HERE (PBKDF2-SHA256, 100,000 iterations - the same format
functions/_lib/auth.js verifies) and only the hash is written to Workers KV. The
plain password never leaves this machine and is never printed.

Uses the Cloudflare API token in ~/.cloudflare_token (needs Workers KV Storage: Edit)
and the IDs in cloudflare.json. Standard library only.
"""
import argparse
import getpass
import hashlib
import json
import os
import re
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "cloudflare.json").read_text())
API = "https://api.cloudflare.com/client/v4"
ITERATIONS = 100_000  # Workers' Web Crypto caps PBKDF2 at 100k
MIN_PASSWORD = 8
USERNAME_RE = re.compile(r"^[a-z0-9._-]{3,40}$")


def token() -> str:
    path = Path.home() / ".cloudflare_token"
    if not path.exists():
        sys.exit("No API token at ~/.cloudflare_token (see cloudflare_deploy_method.md, section 1).")
    return path.read_text().strip()


def kv_url(namespace: str, key: str = "", keys: bool = False) -> str:
    base = f"{API}/accounts/{CONFIG['account_id']}/storage/kv/namespaces/{namespace}"
    if keys:
        return f"{base}/keys"
    return f"{base}/values/{urllib.parse.quote(key, safe='')}"


def call(method: str, url: str, body: bytes | None = None, ctype: str = "application/octet-stream"):
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {token()}")
    if body is not None:
        req.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def kv_get(ns: str, key: str):
    status, data = call("GET", kv_url(ns, key))
    return data.decode() if status == 200 else None


def kv_put(ns: str, key: str, value: str) -> None:
    status, data = call("PUT", kv_url(ns, key), value.encode())
    if status != 200:
        sys.exit(f"KV write failed ({status}): {data[:200]!r}")


def kv_delete(ns: str, key: str) -> bool:
    status, _ = call("DELETE", kv_url(ns, key))
    return status == 200


def kv_list(ns: str, prefix: str):
    status, data = call("GET", kv_url(ns, keys=True) + "?prefix=" + urllib.parse.quote(prefix))
    if status != 200:
        sys.exit(f"KV list failed ({status}): {data[:200]!r}")
    return [k["name"] for k in json.loads(data)["result"]]


def hash_password(plain: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt, ITERATIONS)
    return f"pbkdf2_sha256${ITERATIONS}${salt.hex()}${digest.hex()}"


def ensure_session_key(ns: str) -> None:
    if kv_get(ns, "config:session_key"):
        print("Session-signing key: present.")
        return
    kv_put(ns, "config:session_key", secrets.token_hex(32))  # random; never displayed
    print("Session-signing key: created.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--preview", action="store_true", help="target the Preview environment's KV")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--delete", metavar="USERNAME")
    ap.add_argument("--init", action="store_true")
    args = ap.parse_args()
    ns = CONFIG["kv_preview_id"] if args.preview else CONFIG["kv_production_id"]
    env_label = "PREVIEW" if args.preview else "PRODUCTION"

    if args.list:
        names = [n.split(":", 1)[1] for n in kv_list(ns, "admin:")]
        print(f"{env_label} admins: " + (", ".join(names) if names else "(none)"))
        return
    if args.delete:
        user = args.delete.strip().lower()
        print(f"Removed admin '{user}' from {env_label}." if kv_delete(ns, f"admin:{user}") else "Not found.")
        return

    ensure_session_key(ns)
    if args.init:
        return

    # Non-interactive mode (for scripted checks): STX_ADMIN_USER / STX_ADMIN_PASSWORD.
    user = os.environ.get("STX_ADMIN_USER") or input(f"[{env_label}] Admin username: ")
    user = user.strip().lower()
    if not USERNAME_RE.match(user):
        sys.exit("Username: 3-40 characters of a-z, 0-9, dot, dash or underscore.")
    pw = os.environ.get("STX_ADMIN_PASSWORD")
    if pw is None:
        pw = getpass.getpass("Password (hidden): ")
        if pw != getpass.getpass("Repeat password: "):
            sys.exit("Passwords didn't match - nothing changed.")
    if len(pw) < MIN_PASSWORD:
        sys.exit(f"Password must be at least {MIN_PASSWORD} characters - nothing changed.")

    existed = kv_get(ns, f"admin:{user}") is not None
    record = {
        "username": user,
        "password_hash": hash_password(pw),
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "session_epoch": int(datetime.now(timezone.utc).timestamp()),  # signs out old sessions
    }
    kv_put(ns, f"admin:{user}", json.dumps(record))
    print(f"{'Reset password for' if existed else 'Created'} admin '{user}' in {env_label}. Sign in at /admin/login/")


if __name__ == "__main__":
    main()
