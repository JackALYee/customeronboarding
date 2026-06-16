"""Login UI — single password-based credential form.

One form, two account types:
- `test` / `testme`       → seeded test client
- `test_staff` / `testme` → staff dashboard
- <email> / <password>    → real client whose account was created by staff

All successful logins are written to `login_events`.
"""
import streamlit as st

from db import (
    init_db,
    seed_test_accounts,
    authenticate,
    get_customer,
    mark_login,
    log_login,
    TEST_CLIENT_EMAIL,
)
from assets import MASCOT_DATA_URI

init_db()
seed_test_accounts()

# Built-in usernames recognised by the credential form (in addition to
# real client emails). Test password is `testme` for both.
TEST_CLIENT_USERNAME = "test"
TEST_STAFF_USERNAME = "test_staff"
TEST_PASSWORD = "testme"
STAFF_EMAIL_LABEL = "test_staff@streamax.com"  # display-only identity for staff


def _inject_login_css() -> None:
    st.markdown(
        """
        <style>
        .stApp { background-color: #0c0a14; background-image: radial-gradient(circle at 50% -20%, #1c1330, #0c0a14); }
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
            color: #F4C95D !important;
            -webkit-text-fill-color: #F4C95D !important;
            caret-color: #F4C95D !important;
        }
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextInput"] [data-baseweb="input"]:focus-within {
            border-color: #F4C95D !important;
            box-shadow: 0 0 0 1px #F4C95D !important;
            outline: none !important;
        }
        [data-testid="stTextInput"] input::placeholder {
            color: rgba(160, 174, 192, 0.55) !important;
            -webkit-text-fill-color: rgba(160, 174, 192, 0.55) !important;
        }
        [data-testid="stTextInput"] input:-webkit-autofill {
            -webkit-text-fill-color: #F4C95D !important;
            -webkit-box-shadow: 0 0 0 1000px rgba(20, 25, 40, 0.95) inset !important;
            transition: background-color 5000s ease-in-out 0s;
        }
        .stTextInput label, [data-testid="stTextInput"] label {
            color: #A89FB8 !important;
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
            background: linear-gradient(135deg, #F4C95D 0%, #A06BFF 100%) !important;
            color: #0c0a14 !important;
            font-weight: 700 !important;
            border: none;
            border-radius: 8px;
            width: 100%;
            padding: 0.6rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            box-shadow: 0 4px 15px rgba(244, 201, 93, 0.4);
            transform: translateY(-2px);
        }
        .login-hero { text-align: center; margin-bottom: 24px; }
        @keyframes mascot-float-login { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        .login-mascot { width: 130px; height: 130px; object-fit: contain; margin: 0 auto 16px; display: block;
            animation: mascot-float-login 4s ease-in-out infinite;
            filter: drop-shadow(0 12px 18px rgba(244, 201, 93, 0.18)); }
        .login-hero h1 { color: white; font-size: 2.6rem; margin: 0; line-height: 1.15; }
        .login-hero p { color: #A89FB8; font-size: 1rem; margin-top: 8px; }
        .gradient-text { background: linear-gradient(135deg, #F4C95D 0%, #A06BFF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .login-helptext { color: #64748b; font-size: 0.8rem; text-align: center; margin-top: 18px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_login() -> None:
    _inject_login_css()
    st.write("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="login-hero">
            <img src="{MASCOT_DATA_URI}"
                 alt="Streamax Mascot" class="login-mascot"
                 onerror="this.style.display='none';">
            <h1>Welcome to <span class="gradient-text">Streamax</span></h1>
            <p>Customer Onboarding Portal — sign in to start your journey</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        with st.form("login_form"):
            username = st.text_input(
                "Email or username",
                placeholder="you@yourcompany.com",
            )
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Sign in")

            if submitted:
                u = (username or "").strip().lower()
                p = password or ""

                if not u or not p:
                    st.error("Please enter both your email/username and password.")
                    return

                # --- Built-in staff bypass --------------------------------
                if u == TEST_STAFF_USERNAME and p == TEST_PASSWORD:
                    log_login(STAFF_EMAIL_LABEL, "staff", "staff_credential")
                    st.session_state["authenticated"] = True
                    st.session_state["user_role"] = "staff"
                    st.session_state["staff_identity"] = TEST_STAFF_USERNAME
                    st.rerun()

                # --- Built-in test client bypass -------------------------
                if u == TEST_CLIENT_USERNAME and p == TEST_PASSWORD:
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
                    st.rerun()

                # --- Real client login by email + password ---------------
                if "@" in u:
                    customer = authenticate(u, p)
                    if customer:
                        mark_login(u)
                        log_login(u, "customer", "password")
                        st.session_state["authenticated"] = True
                        st.session_state["user_role"] = "customer"
                        st.session_state["customer_email"] = u
                        st.session_state["customer_company"] = customer["company"] or ""
                        st.session_state["audience"] = customer["audience"] or "fleet"
                        st.rerun()
                    else:
                        # Don't reveal whether the email exists.
                        st.error("Invalid email or password. If you don't have an account yet, contact your Streamax CSM.")
                        return

                # Fell through — not a built-in user and not an email
                st.error("Invalid username or password.")

        st.markdown(
            "<div class='login-helptext'>Don't have an account? Contact your Streamax CSM to be onboarded.</div>",
            unsafe_allow_html=True,
        )
