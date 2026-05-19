"""Staff dashboard — internal Streamax view.

Rendered when st.session_state['user_role'] == 'staff'. Provides:
- A "Create new client" form (email + company + audience).
- A list of all client accounts with their audience and login activity.
- A recent-logins audit table (all roles, all methods).
- Sign-out.

Reachable only via the username+password path in login.py (test_staff /
testme today; can later be extended to real staff credentials or SSO).
"""
import re

import streamlit as st

import db


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _inject_css() -> None:
    st.markdown(
        """
        <style>
        .stApp { background-color: #050810; background-image: radial-gradient(circle at 50% -20%, #0B1221, #050810); color: #FFFFFF; }
        .block-container { max-width: 1280px !important; padding-top: 2rem !important; padding-left: 2rem !important; padding-right: 2rem !important; }

        /* Inputs */
        [data-testid="stTextInput"],
        [data-testid="stTextInput"] > div,
        [data-testid="stTextInput"] > div > div,
        [data-testid="stTextInput"] [data-baseweb="input"],
        [data-testid="stTextInput"] [data-baseweb="base-input"],
        [data-testid="stSelectbox"] > div > div {
            background: rgba(20, 25, 40, 0.85) !important;
            background-color: rgba(20, 25, 40, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            color-scheme: dark !important;
        }
        [data-testid="stTextInput"] input { background: transparent !important; color: #2AF598 !important; -webkit-text-fill-color: #2AF598 !important; }
        [data-testid="stSelectbox"] svg { fill: #2AF598 !important; }
        [data-testid="stSelectbox"] [data-baseweb="select"] > div { color: #FFFFFF !important; }
        .stTextInput label, [data-testid="stTextInput"] label,
        .stSelectbox label, [data-testid="stSelectbox"] label,
        .stRadio label, [data-testid="stRadio"] label { color: #A0AEC0 !important; }

        .stButton>button {
            background: linear-gradient(135deg, #2AF598 0%, #009EFD 100%) !important;
            color: #050810 !important; font-weight: 700 !important;
            border: none; border-radius: 8px;
            padding: 0.55rem 1.2rem; transition: all 0.3s ease;
        }
        .stButton>button:hover { box-shadow: 0 4px 15px rgba(42, 245, 152, 0.35); transform: translateY(-2px); }
        .stButton.secondary>button { background: transparent !important; color: #2AF598 !important; border: 1px solid rgba(42,245,152,0.4) !important; }

        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(12px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
        }

        h1, h2, h3, h4, p, label { color: #FFFFFF; }
        h1 { font-size: 2.2rem; font-weight: 700; margin-top: 0; }
        h2 { font-size: 1.5rem; font-weight: 700; margin-top: 0; }
        h3 { font-size: 1.15rem; font-weight: 600; }
        .staff-subtitle { color: #A0AEC0; font-size: 0.95rem; margin-top: -8px; }
        .gradient-text { background: linear-gradient(135deg, #2AF598 0%, #009EFD 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

        .panel {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 22px;
        }

        .kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 22px; }
        .kpi { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 18px 22px; }
        .kpi-label { color: #A0AEC0; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1px; }
        .kpi-value { color: #2AF598; font-size: 1.8rem; font-weight: 800; margin-top: 4px; }

        .staff-pill { position: fixed; top: 14px; right: 24px; z-index: 9999; display: inline-flex; align-items: center; gap: 10px; background: rgba(10,15,30,0.85); border: 1px solid rgba(0,158,253,0.35); padding: 7px 14px; border-radius: 30px; backdrop-filter: blur(8px); font-size: 0.82rem; }
        .staff-pill .role-icon { color: #009EFD; }
        .staff-pill .role-label { color: #FFFFFF; font-weight: 600; }
        .staff-pill .role-tag { color: #009EFD; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; padding-left: 8px; border-left: 1px solid rgba(255,255,255,0.15); }

        /* Table */
        .stmx-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
        .stmx-table th { background: rgba(42,245,152,0.08); color: #2AF598; text-align: left; padding: 10px 12px; font-weight: 700; border-bottom: 2px solid rgba(42,245,152,0.25); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; }
        .stmx-table td { padding: 10px 12px; color: #cbd5e1; border-bottom: 1px solid rgba(255,255,255,0.05); vertical-align: top; }
        .stmx-table tr:hover td { background: rgba(255,255,255,0.02); color: #FFFFFF; }

        .badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
        .badge-fleet { background: rgba(42,245,152,0.15); color: #2AF598; border: 1px solid rgba(42,245,152,0.3); }
        .badge-tsp { background: rgba(0,158,253,0.15); color: #009EFD; border: 1px solid rgba(0,158,253,0.3); }
        .badge-grey { background: rgba(160,174,192,0.15); color: #A0AEC0; border: 1px solid rgba(160,174,192,0.3); }
        .muted { color: #64748b; font-style: italic; font-size: 0.85rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _human_dt(s: str | None) -> str:
    if not s:
        return "<span class='muted'>—</span>"
    # ISO format trimmed
    return s.split(".")[0].replace("T", " ") + " UTC"


def _audience_badge(a: str) -> str:
    if a == "tsp":
        return "<span class='badge badge-tsp'>TSP</span>"
    if a == "fleet":
        return "<span class='badge badge-fleet'>Fleet</span>"
    return "<span class='badge badge-grey'>—</span>"


def _create_client_form() -> None:
    st.markdown("<h3>➕ Create new client account</h3>", unsafe_allow_html=True)
    with st.form("create_client"):
        col1, col2 = st.columns([1.4, 1])
        with col1:
            email = st.text_input("Client email", placeholder="contact@theircompany.com")
            company = st.text_input("Company name", placeholder="e.g. Acme Logistics")
            password = st.text_input(
                "Initial password",
                type="password",
                placeholder="At least 6 characters",
                help="Share this with the client out-of-band so they can sign in. They can change it later.",
            )
        with col2:
            audience = st.selectbox(
                "Audience type",
                options=["fleet", "tsp"],
                format_func=lambda x: "Fleet Operator" if x == "fleet" else "TSP / Channel Partner",
            )
            st.write("")  # vertical space
            submitted = st.form_submit_button("Create account")

        if submitted:
            email = (email or "").strip().lower()
            company = (company or "").strip()
            pw = password or ""
            if not EMAIL_RE.match(email):
                st.error("Please enter a valid email.")
                return
            if not company:
                st.error("Please enter the company name.")
                return
            if len(pw) < 6:
                st.error("Password must be at least 6 characters.")
                return
            created_by = st.session_state.get("staff_identity", "staff")
            if db.create_customer(email, company, audience, pw, created_by):
                st.success(
                    f"Client account created for {email} ({company}, {audience}). "
                    "Share the password with them out-of-band."
                )
                st.rerun()
            else:
                st.warning(f"An account for {email} already exists.")


def _customers_panel() -> None:
    customers = db.list_customers()
    st.markdown(f"<h3>👥 Client accounts <span style='color:#A0AEC0; font-weight:400; font-size:0.85rem;'>({len(customers)} total)</span></h3>", unsafe_allow_html=True)

    if not customers:
        st.markdown("<p class='muted'>No client accounts yet. Use the form above to create one.</p>", unsafe_allow_html=True)
        return

    rows = []
    for c in customers:
        rows.append(
            f"<tr>"
            f"<td><strong style='color:#FFFFFF;'>{c['email']}</strong></td>"
            f"<td>{c['company'] or '—'}</td>"
            f"<td>{_audience_badge(c['audience'])}</td>"
            f"<td>{_human_dt(c['created_at'])}</td>"
            f"<td>{_human_dt(c['first_login_at'])}</td>"
            f"<td>{_human_dt(c['last_login_at'])}</td>"
            f"</tr>"
        )
    table_html = (
        "<table class='stmx-table'>"
        "<thead><tr>"
        "<th>Email</th><th>Company</th><th>Audience</th><th>Created</th><th>First login</th><th>Last login</th>"
        "</tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )
    st.markdown(f"<div class='panel'>{table_html}</div>", unsafe_allow_html=True)


def _recent_logins_panel() -> None:
    events = db.recent_logins(50)
    total = db.count_logins()
    st.markdown(f"<h3>🕒 Recent logins <span style='color:#A0AEC0; font-weight:400; font-size:0.85rem;'>(last 50 of {total})</span></h3>", unsafe_allow_html=True)

    if not events:
        st.markdown("<p class='muted'>No logins recorded yet.</p>", unsafe_allow_html=True)
        return

    rows = []
    for e in events:
        role_color = "#009EFD" if e["role"] == "staff" else "#2AF598"
        rows.append(
            f"<tr>"
            f"<td><strong style='color:{role_color};'>{e['role']}</strong></td>"
            f"<td>{e['email']}</td>"
            f"<td><span class='muted'>{e['method']}</span></td>"
            f"<td>{_human_dt(e['logged_in_at'])}</td>"
            f"</tr>"
        )
    table_html = (
        "<table class='stmx-table'>"
        "<thead><tr><th>Role</th><th>Identity</th><th>Method</th><th>When</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )
    st.markdown(f"<div class='panel'>{table_html}</div>", unsafe_allow_html=True)


def _kpis() -> None:
    customers = db.list_customers()
    fleet_n = sum(1 for c in customers if c["audience"] == "fleet")
    tsp_n = sum(1 for c in customers if c["audience"] == "tsp")
    logins = db.count_logins()
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi"><div class="kpi-label">Client accounts</div><div class="kpi-value">{len(customers)}</div></div>
            <div class="kpi"><div class="kpi-label">Fleet / TSP split</div><div class="kpi-value">{fleet_n} <span style="color:#A0AEC0; font-size:1rem;">fleet</span> · {tsp_n} <span style="color:#A0AEC0; font-size:1rem;">tsp</span></div></div>
            <div class="kpi"><div class="kpi-label">Logins recorded</div><div class="kpi-value">{logins}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    _inject_css()

    identity = st.session_state.get("staff_identity", "staff")
    st.markdown(
        f"""
        <div class="staff-pill">
            <i class="fa-solid fa-user-shield role-icon"></i>
            <span class="role-label">{identity}</span>
            <span class="role-tag">Staff</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <h1><span class="gradient-text">Streamax Staff</span> · Onboarding Portal Admin</h1>
        <p class="staff-subtitle">Manage client accounts, assign Fleet / TSP audience, and review login activity.</p>
        """,
        unsafe_allow_html=True,
    )

    # Sign-out button (top of page so it's easy to find)
    cols = st.columns([5, 1])
    with cols[1]:
        if st.button("Sign out", key="staff_signout"):
            for k in ("authenticated", "user_role", "staff_identity"):
                st.session_state.pop(k, None)
            st.rerun()

    _kpis()
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    _create_client_form()
    st.markdown("</div>", unsafe_allow_html=True)
    _customers_panel()
    _recent_logins_panel()
