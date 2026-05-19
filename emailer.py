"""SMTP helper — sends the 6-digit login code to a customer's email.

Credentials are loaded from (in order):
  1. st.secrets (preferred for Streamlit Cloud deploys)
  2. env vars
  3. a local env.txt next to this file (dev fallback, matches Sales Toolkit pattern)

If SMTP is not configured, the helper raises RuntimeError. In dev, the login
flow shows the code on screen so testing works without SMTP.
"""
import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

import streamlit as st


def _load_env_txt() -> dict:
    """Read env.txt if present. Returns dict of KEY=VALUE pairs."""
    out = {}
    p = Path(__file__).parent / "env.txt"
    if not p.exists():
        return out
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


_ENV_TXT = _load_env_txt()


def _get(key: str, default: str = "") -> str:
    # st.secrets > env var > env.txt > default
    try:
        v = st.secrets.get(key)
        if v:
            return str(v)
    except Exception:
        pass
    return os.environ.get(key, _ENV_TXT.get(key, default))


def smtp_configured() -> bool:
    return bool(_get("SMTP_HOST") and _get("SMTP_USER") and _get("SMTP_PASS"))


def send_login_code(to_email: str, code: str) -> None:
    host = _get("SMTP_HOST", "mail.streamax.com")
    port = int(_get("SMTP_PORT", "465"))
    use_ssl = _get("SMTP_SSL", "true").lower() in ("true", "1", "yes")
    user = _get("SMTP_USER")
    pwd = _get("SMTP_PASS")

    if not (user and pwd):
        raise RuntimeError("SMTP credentials not configured")

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = to_email
    msg["Subject"] = f"Your Streamax onboarding code: {code}"
    msg.set_content(
        f"""Hi,

Your Streamax Customer Onboarding Portal login code is:

    {code}

This code expires in 15 minutes. If you didn't request it, please ignore this email.

— The Streamax team
support@streamax.com
"""
    )
    msg.add_alternative(
        f"""<html><body style="font-family: 'Segoe UI', Arial, sans-serif; background: #f6f8fb; padding: 30px;">
  <div style="max-width: 480px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 32px; box-shadow: 0 4px 18px rgba(0,0,0,0.06);">
    <div style="text-align: center; margin-bottom: 24px;">
      <h1 style="background: linear-gradient(135deg, #2AF598, #009EFD); -webkit-background-clip: text; color: transparent; margin: 0; font-size: 1.6rem;">Streamax</h1>
      <p style="color: #64748b; font-size: 0.9rem; margin: 4px 0 0;">Customer Onboarding Portal</p>
    </div>
    <p style="color: #1e293b; font-size: 1rem;">Hi,</p>
    <p style="color: #475569;">Use this code to sign in to your Streamax Customer Onboarding Portal:</p>
    <div style="text-align: center; margin: 28px 0;">
      <div style="display: inline-block; padding: 16px 32px; background: linear-gradient(135deg, #050810, #0B1221); color: #2AF598; font-size: 2rem; font-weight: 800; letter-spacing: 0.4rem; border-radius: 12px; font-family: 'Courier New', monospace;">{code}</div>
    </div>
    <p style="color: #64748b; font-size: 0.85rem; text-align: center;">This code expires in 15 minutes.</p>
    <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0;">
    <p style="color: #94a3b8; font-size: 0.78rem; text-align: center; margin: 0;">Didn't request this? You can safely ignore this email.<br>Need help? <a href="mailto:support@streamax.com" style="color: #009EFD;">support@streamax.com</a></p>
  </div>
</body></html>""",
        subtype="html",
    )

    context = ssl.create_default_context()
    if use_ssl:
        with smtplib.SMTP_SSL(host, port, context=context, timeout=15) as server:
            server.login(user, pwd)
            server.send_message(msg)
    else:
        with smtplib.SMTP(host, port, timeout=15) as server:
            server.starttls(context=context)
            server.login(user, pwd)
            server.send_message(msg)
