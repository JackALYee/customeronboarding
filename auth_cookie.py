"""Signed-cookie session persistence.

Streamlit's session_state lives only inside one websocket session — a full
page reload (e.g. clicking a `?lang=` or `?logout=1` link) starts a fresh
session and wipes it. This module carries the auth state across reloads in a
signed browser cookie so a language switch or refresh doesn't log the user out.

Trust model: anyone who can read the cookie can impersonate that session
(same as the SMTP-validated logins in the sibling salestoolkit) — adequate for
this onboarding portal, not for handling PII. Set AUTH_SECRET in secrets/env
for any real deployment; a built-in fallback is used otherwise.

Degrades gracefully: if extra_streamlit_components isn't installed, all calls
are no-ops and the app simply behaves as before (reload = logout).
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta

import streamlit as st

try:
    import extra_streamlit_components as stx
    _AVAILABLE = True
except Exception:  # noqa: BLE001
    _AVAILABLE = False

COOKIE_NAME = "stmx_onb"
COOKIE_DAYS = 7
_FALLBACK_SECRET = "stmx-onboarding-set-AUTH_SECRET-in-secrets"
_CM_KEY = "_stmx_cookie_mgr"

# Sticky guard set on sign-out. restore() refuses to re-hydrate while it's set,
# defeating the race where the async cookie-delete hasn't propagated before the
# next rerun reads the cookie back (which would silently re-authenticate).
LOGOUT_FLAG = "_stmx_logged_out"

# Session keys carried across reloads.
_PERSIST_KEYS = (
    "authenticated",
    "user_role",
    "customer_email",
    "customer_company",
    "audience",
    "staff_identity",
    "ui_lang",
)


def available() -> bool:
    return _AVAILABLE


# --- token signing --------------------------------------------------------

def _secret() -> str:
    try:
        s = st.secrets.get("AUTH_SECRET")
        if s:
            return str(s)
    except Exception:  # noqa: BLE001
        pass
    return os.environ.get("AUTH_SECRET", _FALLBACK_SECRET)


def _sign(payload: str) -> str:
    return hmac.new(_secret().encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()[:32]


def _make_token(data: dict) -> str:
    body = {"d": data, "exp": int((datetime.now() + timedelta(days=COOKIE_DAYS)).timestamp())}
    raw = base64.urlsafe_b64encode(json.dumps(body).encode("utf-8")).decode("ascii")
    return f"{raw}.{_sign(raw)}"


def _verify_token(token: str):
    if not token or "." not in token:
        return None
    raw, sig = token.rsplit(".", 1)
    if _sign(raw) != sig:
        return None
    try:
        body = json.loads(base64.urlsafe_b64decode(raw.encode("ascii")).decode("utf-8"))
    except Exception:  # noqa: BLE001
        return None
    if datetime.now().timestamp() > body.get("exp", 0):
        return None
    return body.get("d")


# --- cookie manager -------------------------------------------------------

def init() -> None:
    """Instantiate the cookie manager once for this run. Call near the top of
    app.py before restore()."""
    if not _AVAILABLE:
        return
    # Re-create the widget each run (Streamlit requires re-registration).
    st.session_state.pop(_CM_KEY, None)
    st.session_state[_CM_KEY] = stx.CookieManager(key="stmx_cookie_mgr")


def _cm():
    if not _AVAILABLE:
        return None
    if _CM_KEY not in st.session_state:
        init()
    return st.session_state.get(_CM_KEY)


# --- public API -----------------------------------------------------------

def restore() -> None:
    """Re-hydrate session_state from the cookie if not already authenticated."""
    if st.session_state.get("authenticated"):
        return
    if st.session_state.get(LOGOUT_FLAG):
        # User just signed out in this session — don't auto-restore from a
        # cookie value the browser hasn't dropped yet.
        return
    cm = _cm()
    if cm is None:
        return
    token = cm.get(COOKIE_NAME)
    data = _verify_token(token)
    if data:
        for k in _PERSIST_KEYS:
            if k in data and data[k] is not None:
                st.session_state[k] = data[k]


def persist() -> None:
    """Write current auth state to the cookie. No-op if not authenticated."""
    if not st.session_state.get("authenticated"):
        return
    cm = _cm()
    if cm is None:
        return
    # A fresh, valid auth clears the post-logout guard.
    st.session_state.pop(LOGOUT_FLAG, None)
    data = {k: st.session_state.get(k) for k in _PERSIST_KEYS if st.session_state.get(k) is not None}
    try:
        cm.set(COOKIE_NAME, _make_token(data), expires_at=datetime.now() + timedelta(days=COOKIE_DAYS))
    except Exception:  # noqa: BLE001
        pass


def clear() -> None:
    """Drop the auth cookie (sign-out)."""
    cm = _cm()
    if cm is None:
        return
    try:
        cm.set(COOKIE_NAME, "", expires_at=datetime.now() - timedelta(days=1))
    except Exception:  # noqa: BLE001
        pass
    try:
        cm.delete(COOKIE_NAME)
    except Exception:  # noqa: BLE001
        pass
