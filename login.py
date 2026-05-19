"""Login UI for the Streamax Customer Onboarding Portal.

Two paths:

1. Customer email + 6-digit code (primary)
   - Customer enters their email.
   - Email is looked up in `customers` (staff-created in advance).
   - If found: 6-digit code generated, emailed via SMTP, customer enters
     code on the next screen. If SMTP isn't configured, the code is
     shown on screen (DEV mode).
   - If not found: shows "no account — contact your CSM" message.

2. Username + password (for built-in test accounts)
   - `test` / `testme`       → log in as the seeded test client
   - `test_staff` / `testme` → log in to the staff dashboard
   - Anything else → invalid

All successful logins are written to `login_events` so the staff
dashboard can show a recent-logins panel.
"""
import random
import re
import time
from datetime import datetime, timedelta

import streamlit as st

from db import (
    init_db,
    seed_test_accounts,
    save_code,
    verify_code,
    get_customer,
    mark_login,
    log_login,
    TEST_CLIENT_EMAIL,
)
from emailer import smtp_configured, send_login_code

init_db()
seed_test_accounts()

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Built-in credentials. Kept here (not in db) so they survive db wipes
# and are easy to find/rotate.
TEST_CLIENT_USERNAME = "test"
TEST_STAFF_USERNAME = "test_staff"
TEST_PASSWORD = "testme"
STAFF_EMAIL_LABEL = "test_staff@streamax.com"  # display-only identity for staff


def _inject_login_css() -> None:
    st.markdown(
        """
        <style>
        .stApp { background-color: #050810; background-image: radial-gradient(circle at 50% -20%, #0B1221, #050810); }
        [data-testid="stTextInput"],
        [data-testid="stTextInput"] > div,
        [data-testid="stTextInput"] > div > div,
        [data-testid="stTextInput"] [data-baseweb="input"],
        [data-testid="stTextInput"] [data-baseweb="base-input"] {
            background: rgba(20, 25, 40, 0.85) !important;
            background-color: rgba(20, 25, 40, 0.85) !important;
            background-image: none !important;
            color-scheme: dark !important;
            forced-color-adjust: none !important;
            border-radius: 8px !important;
        }
        [data-testid="stTextInput"] [data-baseweb="input"],
        [data-testid="stTextInput"] [data-baseweb="base-input"] {
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        [data-testid="stTextInput"] input {
            background: transparent !important;
            color: #2AF598 !important;
            -webkit-text-fill-color: #2AF598 !important;
            caret-color: #2AF598 !important;
        }
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextInput"] [data-baseweb="input"]:focus-within {
            border-color: #2AF598 !important;
            box-shadow: 0 0 0 1px #2AF598 !important;
            outline: none !important;
        }
        [data-testid="stTextInput"] input::placeholder {
            color: rgba(160, 174, 192, 0.55) !important;
            -webkit-text-fill-color: rgba(160, 174, 192, 0.55) !important;
        }
        [data-testid="stTextInput"] input:-webkit-autofill {
            -webkit-text-fill-color: #2AF598 !important;
            -webkit-box-shadow: 0 0 0 1000px rgba(20, 25, 40, 0.95) inset !important;
            transition: background-color 5000s ease-in-out 0s;
        }
        .stTextInput label, [data-testid="stTextInput"] label {
            color: #A0AEC0 !important;
        }
        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 30px;
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        .stButton>button {
            background: linear-gradient(135deg, #2AF598 0%, #009EFD 100%) !important;
            color: #050810 !important;
            font-weight: 700 !important;
            border: none;
            border-radius: 8px;
            width: 100%;
            padding: 0.6rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            box-shadow: 0 4px 15px rgba(42, 245, 152, 0.4);
            transform: translateY(-2px);
        }
        .login-hero { text-align: center; margin-bottom: 24px; }
        .login-hero h1 { color: white; font-size: 2.6rem; margin: 0; line-height: 1.15; }
        .login-hero p { color: #A0AEC0; font-size: 1rem; margin-top: 8px; }
        .gradient-text { background: linear-gradient(135deg, #2AF598 0%, #009EFD 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .dev-code-banner { background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.4); color: #fbbf24; padding: 14px 20px; border-radius: 10px; text-align: center; font-family: monospace; margin: 20px 0; }
        .login-toggle-row { text-align: center; margin-top: 18px; color: #A0AEC0; font-size: 0.85rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _gen_code() -> str:
    return f"{random.randint(0, 999999):06d}"


# --- Step 1a: customer email lookup --------------------------------------

def _step_request_code() -> None:
    st.markdown(
        """
        <div class="login-hero">
            <h1>Welcome to <span class="gradient-text">Streamax</span></h1>
            <p>Customer Onboarding Portal — sign in to start your journey</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        with st.form("request_code_form"):
            email = st.text_input("Your work email", placeholder="you@yourcompany.com")
            submitted = st.form_submit_button("Send my login code")

            if submitted:
                email = (email or "").strip().lower()
                if not EMAIL_RE.match(email):
                    st.error("Please enter a valid email address.")
                    return

                customer = get_customer(email)
                if not customer:
                    st.error(
                        "We don't recognise that email. Please contact your Streamax CSM "
                        "to be onboarded — your account needs to be set up before you can sign in."
                    )
                    return

                code = _gen_code()
                expires_at = (datetime.utcnow() + timedelta(minutes=15)).isoformat()
                save_code(email, code, expires_at)

                st.session_state["pending_email"] = email

                sent_ok = False
                send_error = None
                if smtp_configured():
                    try:
                        with st.spinner("Sending your code..."):
                            send_login_code(email, code)
                        sent_ok = True
                    except Exception as e:  # noqa: BLE001
                        send_error = str(e)

                if sent_ok:
                    st.session_state["dev_code_to_show"] = None
                    st.success(f"Code sent to {email}. Check your inbox.")
                else:
                    st.session_state["dev_code_to_show"] = code
                    if send_error:
                        st.warning(f"SMTP send failed ({send_error}). Showing code on screen for dev access.")
                    else:
                        st.info("SMTP not configured — showing code on screen for dev access.")

                st.session_state["login_step"] = "verify"
                time.sleep(0.4)
                st.rerun()

        # Toggle to credential mode
        st.markdown(
            "<div class='login-toggle-row'>Have a test or staff credential?</div>",
            unsafe_allow_html=True,
        )
        if st.button("Sign in with username & password", key="toggle_to_cred"):
            st.session_state["login_step"] = "credential"
            st.rerun()


# --- Step 1b: username + password (test client / staff) -------------------

def _step_credential() -> None:
    st.markdown(
        """
        <div class="login-hero">
            <h1><span class="gradient-text">Username</span> sign-in</h1>
            <p>Test and staff accounts only.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        with st.form("credential_form"):
            username = st.text_input("Username", placeholder="test or test_staff")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Sign in")

            if submitted:
                u = (username or "").strip().lower()
                p = password or ""

                if u == TEST_CLIENT_USERNAME and p == TEST_PASSWORD:
                    # Log in as the seeded test client
                    customer = get_customer(TEST_CLIENT_EMAIL)
                    audience = customer["audience"] if customer else "fleet"
                    company = customer["company"] if customer else "Test Client"
                    mark_login(TEST_CLIENT_EMAIL)
                    log_login(TEST_CLIENT_EMAIL, "customer", "test_bypass")
                    st.session_state["authenticated"] = True
                    st.session_state["user_role"] = "customer"
                    st.session_state["customer_email"] = TEST_CLIENT_EMAIL
                    st.session_state["customer_company"] = company
                    st.session_state["audience"] = audience
                    _clear_pending()
                    st.rerun()

                elif u == TEST_STAFF_USERNAME and p == TEST_PASSWORD:
                    log_login(STAFF_EMAIL_LABEL, "staff", "staff_credential")
                    st.session_state["authenticated"] = True
                    st.session_state["user_role"] = "staff"
                    st.session_state["staff_identity"] = TEST_STAFF_USERNAME
                    _clear_pending()
                    st.rerun()

                else:
                    st.error("Invalid username or password.")

        if st.button("← Back to email sign-in", key="back_to_email"):
            st.session_state["login_step"] = "request"
            st.rerun()


# --- Step 2: verify the 6-digit code -------------------------------------

def _step_verify_code() -> None:
    email = st.session_state.get("pending_email", "")
    st.markdown(
        f"""
        <div class="login-hero">
            <h1>Enter your <span class="gradient-text">6-digit code</span></h1>
            <p>We sent a code to <strong style="color:#2AF598;">{email}</strong>. It expires in 15 minutes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    dev_code = st.session_state.get("dev_code_to_show")
    if dev_code:
        st.markdown(
            f"<div class='dev-code-banner'>DEV MODE — your code is: <strong>{dev_code}</strong></div>",
            unsafe_allow_html=True,
        )

    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        with st.form("verify_code_form"):
            code = st.text_input("6-digit code", max_chars=6, placeholder="123456")
            verified = st.form_submit_button("Verify & enter portal")

            if verified:
                code = (code or "").strip()
                if not (code.isdigit() and len(code) == 6):
                    st.error("Please enter the 6-digit code.")
                    return
                if not verify_code(email, code):
                    st.error("That code is invalid or expired. Request a new one.")
                    return

                customer = get_customer(email)
                if not customer:
                    st.error("Account not found. Contact your CSM.")
                    return

                mark_login(email)
                log_login(email, "customer", "email_code")
                st.session_state["authenticated"] = True
                st.session_state["user_role"] = "customer"
                st.session_state["customer_email"] = email
                st.session_state["customer_company"] = customer["company"] or ""
                st.session_state["audience"] = customer["audience"] or "fleet"
                _clear_pending()
                st.rerun()

        if st.button("← Use a different email", key="back_to_request"):
            _clear_pending()
            st.rerun()


def _clear_pending() -> None:
    for k in ("pending_email", "dev_code_to_show", "login_step"):
        st.session_state.pop(k, None)


def render_login() -> None:
    _inject_login_css()
    st.write("<br>", unsafe_allow_html=True)
    step = st.session_state.get("login_step", "request")
    if step == "verify":
        _step_verify_code()
    elif step == "credential":
        _step_credential()
    else:
        _step_request_code()
