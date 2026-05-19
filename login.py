"""Customer-facing email + 6-digit code login.

Flow:
  Step 1 — Customer enters email + company + selects audience (Fleet / TSP)
           and clicks "Send code". A 6-digit code is generated, saved, and
           emailed.
  Step 2 — Customer enters the code. If valid, session_state.authenticated = True
           and the portal renders.

In dev / no-SMTP environments, the code is shown directly on screen so the
flow works without configuring email.
"""
import random
import re
import time
from datetime import datetime, timedelta

import streamlit as st

from db import init_db, save_code, verify_code, upsert_customer
from emailer import smtp_configured, send_login_code

init_db()

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


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
        .stTextInput label, [data-testid="stTextInput"] label,
        .stRadio label, [data-testid="stRadio"] label,
        .stSelectbox label, [data-testid="stSelectbox"] label {
            color: #A0AEC0 !important;
        }
        [data-testid="stRadio"] > div {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            padding: 12px 16px;
            border-radius: 12px;
        }
        [data-testid="stRadio"] label p { color: #FFFFFF !important; }
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
        </style>
        """,
        unsafe_allow_html=True,
    )


def _gen_code() -> str:
    return f"{random.randint(0, 999999):06d}"


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
            company = st.text_input("Company name", placeholder="e.g. Acme Logistics")
            audience = st.radio(
                "I am a...",
                ["Fleet Operator (we run trucks/buses/taxis)", "TSP / Channel Partner (we resell telematics)"],
                index=0,
            )
            submitted = st.form_submit_button("Send my login code")

            if submitted:
                email = (email or "").strip().lower()
                company = (company or "").strip()
                if not EMAIL_RE.match(email):
                    st.error("Please enter a valid email address.")
                    return
                if not company:
                    st.error("Please enter your company name.")
                    return

                aud_key = "fleet" if audience.startswith("Fleet") else "tsp"
                code = _gen_code()
                expires_at = (datetime.utcnow() + timedelta(minutes=15)).isoformat()
                save_code(email, code, expires_at)

                # Stash pending identity for step 2
                st.session_state["pending_email"] = email
                st.session_state["pending_company"] = company
                st.session_state["pending_audience"] = aud_key

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
                    # Dev fallback — surface the code so login works without SMTP
                    st.session_state["dev_code_to_show"] = code
                    if send_error:
                        st.warning(f"SMTP send failed ({send_error}). Showing code on screen for dev access.")
                    else:
                        st.info("SMTP not configured — showing code on screen for dev access.")

                st.session_state["login_step"] = "verify"
                time.sleep(0.5)
                st.rerun()


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
                    st.error("That code is invalid or expired. Request a new one below.")
                    return

                company = st.session_state.get("pending_company", "")
                audience = st.session_state.get("pending_audience", "fleet")
                upsert_customer(email, company, audience)

                st.session_state["authenticated"] = True
                st.session_state["customer_email"] = email
                st.session_state["customer_company"] = company
                st.session_state["audience"] = audience
                # Clean pending keys
                for k in ("pending_email", "pending_company", "pending_audience", "dev_code_to_show", "login_step"):
                    st.session_state.pop(k, None)
                st.rerun()

        if st.button("← Use a different email", key="back_to_request"):
            for k in ("pending_email", "pending_company", "pending_audience", "dev_code_to_show", "login_step"):
                st.session_state.pop(k, None)
            st.rerun()


def render_login() -> None:
    _inject_login_css()
    st.write("<br>", unsafe_allow_html=True)
    step = st.session_state.get("login_step", "request")
    if step == "verify":
        _step_verify_code()
    else:
        _step_request_code()
