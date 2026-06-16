"""Staff dashboard — internal Streamax admin view.

Rendered when st.session_state['user_role'] == 'staff'. Styled to match the
customer portal's golden/purple glassmorphism rather than the default
Streamlit look — every native widget is restyled, the page chrome is hidden,
and the contacts editor uses a glass textarea (one "Role | contact" per line)
instead of the default data-editor grid.

Organised into three tabs: Clients · Key contacts · Activity.

Reachable only via the username+password path in login.py (test_staff /
testme today; can later be extended to real staff credentials or SSO).
"""
import html as _html
import json as _json
import re

import streamlit as st
import streamlit.components.v1 as components

import db

SUPPORTED_LANGS = (("en", "EN"), ("es", "ES"), ("pt", "PT"), ("fr", "FR"))


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _inject_css() -> None:
    # NOTE: keep this a single contiguous block — a BLANK LINE inside a
    # st.markdown <style> terminates the HTML passthrough and the rest of the
    # CSS leaks onto the page as text. No empty lines below.
    css = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
:root { --gold:#F4C95D; --purple:#A06BFF; --grad:linear-gradient(135deg,#F4C95D 0%,#A06BFF 100%); --glass:rgba(255,255,255,0.04); --glass-brd:rgba(255,255,255,0.10); --txt:#ECE7F5; --muted:#A89FB8; --faint:#6f6885; }
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { display:none !important; }
header { visibility:hidden; height:0 !important; }
.stApp { background:#0c0a14; background-image: radial-gradient(circle at 12% -10%, rgba(160,107,255,0.16), transparent 42%), radial-gradient(circle at 92% 0%, rgba(244,201,93,0.10), transparent 40%), radial-gradient(circle at 50% -20%, #1c1330, #0c0a14); color:var(--txt); font-family:'Inter',sans-serif; }
.block-container { max-width:1180px !important; padding-top:2.4rem !important; padding-left:2rem !important; padding-right:2rem !important; }
h1,h2,h3,h4,p,label,span,div { font-family:'Inter',sans-serif; }
h1 { font-size:1.85rem; font-weight:800; margin:0; letter-spacing:-0.01em; color:var(--txt); }
h3 { font-size:1.08rem; font-weight:700; margin:0 0 4px; color:var(--txt); }
.staff-subtitle { color:var(--muted); font-size:0.92rem; margin-top:2px; }
.section-help { color:var(--faint); font-size:0.84rem; margin:0 0 16px; }
.muted { color:var(--faint); font-size:0.85rem; }
.grad-text { background:var(--grad); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }
hr.rule { border:none; border-top:1px solid rgba(255,255,255,0.08); margin:18px 0 24px; }
.whoami { text-align:right; color:var(--muted); font-size:0.82rem; margin-bottom:8px; }
.whoami strong { color:var(--txt); font-weight:600; }
.whoami .tag { display:inline-block; margin-left:8px; padding:2px 9px; border-radius:7px; font-size:0.64rem; font-weight:700; letter-spacing:0.8px; text-transform:uppercase; color:#1a1024; background:var(--grad); }
.stButton > button, [data-testid="stFormSubmitButton"] > button { background:var(--glass) !important; color:var(--txt) !important; border:1px solid var(--glass-brd) !important; border-radius:10px !important; font-weight:600 !important; padding:0.5rem 1.15rem !important; backdrop-filter:blur(8px); box-shadow:none !important; transition:all .2s ease !important; }
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover { background:rgba(255,255,255,0.08) !important; border-color:rgba(244,201,93,0.45) !important; transform:translateY(-1px); }
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] > button[kind="primary"] { background:var(--grad) !important; color:#1a1024 !important; border:none !important; font-weight:700 !important; }
.stButton > button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] > button[kind="primary"]:hover { box-shadow:0 8px 22px rgba(160,107,255,0.30) !important; transform:translateY(-1px); }
[data-testid="stTextInput"] [data-baseweb="input"], [data-testid="stTextInput"] [data-baseweb="base-input"], [data-testid="stSelectbox"] [data-baseweb="select"] > div, .stTextArea textarea { background:rgba(255,255,255,0.04) !important; border:1px solid var(--glass-brd) !important; border-radius:10px !important; color:var(--txt) !important; }
[data-testid="stTextInput"] input { color:var(--txt) !important; -webkit-text-fill-color:var(--txt) !important; }
[data-testid="stTextInput"] [data-baseweb="input"]:focus-within, .stTextArea textarea:focus { border-color:rgba(244,201,93,0.55) !important; box-shadow:0 0 0 1px rgba(244,201,93,0.35) !important; }
.stTextArea textarea { font-family:'Inter',ui-monospace,monospace !important; font-size:0.9rem !important; line-height:1.7 !important; }
.stTextInput label, [data-testid="stTextInput"] label, .stSelectbox label, [data-testid="stSelectbox"] label, .stTextArea label { color:var(--muted) !important; font-weight:500; }
[data-testid="stForm"] { background:var(--glass); border:1px solid var(--glass-brd); border-radius:16px; padding:24px; backdrop-filter:blur(14px); box-shadow:0 10px 30px rgba(0,0,0,0.3); }
[data-baseweb="tab-list"] { gap:10px; border-bottom:1px solid rgba(255,255,255,0.08) !important; background:transparent !important; }
button[data-baseweb="tab"] { background:transparent !important; color:var(--muted) !important; font-weight:600 !important; padding:12px 6px !important; }
button[data-baseweb="tab"]:hover { color:var(--txt) !important; }
button[data-baseweb="tab"][aria-selected="true"] { color:var(--txt) !important; }
[data-baseweb="tab-highlight"] { background:var(--grad) !important; height:2px !important; }
[data-baseweb="tab-border"] { background:transparent !important; }
[data-baseweb="tab-panel"] { padding-top:24px; }
.kpi-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin:2px 0 6px; }
.kpi { background:var(--glass); border:1px solid var(--glass-brd); border-radius:14px; padding:18px 20px; backdrop-filter:blur(12px); transition:all .25s ease; }
.kpi:hover { border-color:rgba(244,201,93,0.28); transform:translateY(-2px); }
.kpi-label { color:var(--faint); font-size:0.72rem; text-transform:uppercase; letter-spacing:0.9px; }
.kpi-value { font-size:1.7rem; font-weight:800; margin-top:6px; }
.kpi-value .unit { color:var(--faint); font-size:0.85rem; font-weight:500; }
.card { background:var(--glass); border:1px solid var(--glass-brd); border-radius:14px; padding:8px 10px; backdrop-filter:blur(12px); }
.stmx-table { width:100%; border-collapse:collapse; font-size:0.86rem; }
.stmx-table th { color:var(--faint); text-align:left; padding:11px 12px; font-weight:600; border-bottom:1px solid rgba(255,255,255,0.08); font-size:0.7rem; text-transform:uppercase; letter-spacing:0.5px; }
.stmx-table td { padding:11px 12px; color:#cabfe0; border-bottom:1px solid rgba(255,255,255,0.05); vertical-align:top; }
.stmx-table tr:last-child td { border-bottom:none; }
.stmx-table tr:hover td { background:rgba(255,255,255,0.02); color:var(--txt); }
.badge { display:inline-block; padding:2px 9px; border-radius:7px; font-size:0.66rem; font-weight:700; letter-spacing:0.3px; }
.badge-fleet { color:var(--gold); background:rgba(244,201,93,0.12); border:1px solid rgba(244,201,93,0.28); }
.badge-tsp { color:var(--purple); background:rgba(160,107,255,0.14); border:1px solid rgba(160,107,255,0.30); }
.badge-grey { color:var(--muted); background:rgba(168,159,184,0.10); border:1px solid rgba(168,159,184,0.22); }
.preview-label { color:var(--faint); font-size:0.75rem; text-transform:uppercase; letter-spacing:0.9px; margin:18px 0 8px; }
.preview-card { background:rgba(255,255,255,0.03); border:1px solid var(--glass-brd); border-radius:14px; padding:22px 24px; backdrop-filter:blur(12px); max-width:560px; }
.preview-card h4 { font-size:1.05rem; font-weight:700; color:var(--txt); margin:0 0 12px; }
.preview-card .sla { font-size:0.8rem; margin-top:12px; color:var(--muted); }
.topbar { position:fixed; top:0; left:0; right:0; height:56px; z-index:1000; background:rgba(12,10,20,0.85); backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px); border-bottom:1px solid rgba(255,255,255,0.08); }
.topbar-inner { max-width:1180px; margin:0 auto; height:100%; padding:0 2rem; display:flex; align-items:center; justify-content:space-between; }
.topbar .brand { font-weight:800; font-size:1.1rem; color:var(--txt); }
.usermenu { position:relative; }
.usermenu summary { list-style:none; cursor:pointer; display:inline-flex; align-items:center; gap:10px; padding:6px 12px 6px 6px; border:1px solid var(--glass-brd); border-radius:30px; background:var(--glass); transition:border-color .2s ease; }
.usermenu summary:hover { border-color:rgba(244,201,93,0.45); }
.usermenu summary::-webkit-details-marker { display:none; }
.usermenu .avatar { width:28px; height:28px; border-radius:50%; background:var(--grad); display:flex; align-items:center; justify-content:center; color:#1a1024; font-size:0.8rem; }
.usermenu .uname { font-size:0.85rem; font-weight:600; color:var(--txt); }
.usermenu .chev { color:var(--muted); font-size:0.7rem; transition:transform .2s ease; }
.usermenu[open] .chev { transform:rotate(180deg); }
.usermenu-pop { position:absolute; top:calc(100% + 10px); right:0; min-width:240px; background:rgba(20,15,30,0.97); border:1px solid var(--glass-brd); border-radius:14px; padding:12px; box-shadow:0 20px 50px rgba(0,0,0,0.5); backdrop-filter:blur(18px); }
.um-id { padding:6px 8px 12px; border-bottom:1px solid rgba(255,255,255,0.08); margin-bottom:10px; }
.um-id-name { color:var(--txt); font-weight:700; font-size:0.9rem; }
.um-id-tag { color:var(--purple); font-size:0.64rem; font-weight:700; letter-spacing:0.8px; text-transform:uppercase; margin-top:2px; }
.um-label { color:var(--faint); font-size:0.68rem; text-transform:uppercase; letter-spacing:1px; margin:4px 6px 8px; }
.um-langs { display:flex; gap:6px; margin-bottom:10px; }
.um-langs .lang-pill { flex:1; text-align:center; padding:7px 0; border-radius:8px; border:1px solid var(--glass-brd); color:var(--muted); text-decoration:none; font-size:0.78rem; font-weight:700; }
.um-langs .lang-pill:hover { color:var(--txt); border-color:rgba(244,201,93,0.45); }
.um-langs .lang-pill.active { background:var(--grad); color:#1a1024; border:none; }
.um-divider { height:1px; background:rgba(255,255,255,0.08); margin:6px 0; }
.um-item { display:flex; align-items:center; gap:10px; padding:10px 8px; border-radius:9px; color:var(--muted); text-decoration:none; font-size:0.88rem; font-weight:500; }
.um-item:hover { background:rgba(255,255,255,0.06); color:var(--txt); }
.um-item.signout:hover { background:rgba(255,107,107,0.10); color:#ff6b6b; }
[data-baseweb="tab-list"] { position:sticky; top:56px; z-index:900; background:rgba(12,10,20,0.92); backdrop-filter:blur(10px); }
.block-container { padding-top:80px !important; }
</style>
"""
    st.markdown(css, unsafe_allow_html=True)


def _human_dt(s) -> str:
    if not s:
        return "<span class='muted'>—</span>"
    return s.split(".")[0].replace("T", " ") + " UTC"


def _audience_badge(a: str) -> str:
    if a == "tsp":
        return "<span class='badge badge-tsp'>TSP</span>"
    if a == "fleet":
        return "<span class='badge badge-fleet'>Fleet</span>"
    return "<span class='badge badge-grey'>—</span>"


# --- Tab: Clients ---------------------------------------------------------

def _create_client_form() -> None:
    st.markdown("<h3>New client</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p class='section-help'>Create an account, then share the password with the client out-of-band.</p>",
        unsafe_allow_html=True,
    )
    with st.form("create_client"):
        col1, col2 = st.columns([1.4, 1])
        with col1:
            email = st.text_input("Client email", placeholder="contact@theircompany.com")
            company = st.text_input("Company name", placeholder="e.g. Acme Logistics")
            password = st.text_input(
                "Initial password", type="password",
                placeholder="At least 6 characters", help="The client can change it later.",
            )
        with col2:
            audience = st.selectbox(
                "Audience type", options=["fleet", "tsp"],
                format_func=lambda x: "Fleet Operator" if x == "fleet" else "TSP / Channel Partner",
            )
            st.write("")
            submitted = st.form_submit_button("Create account", type="primary")

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
                st.success(f"Created account for {email} ({company}).")
                st.rerun()
            else:
                st.warning(f"An account for {email} already exists.")


def _customers_panel() -> None:
    customers = db.list_customers()
    st.markdown(
        f"<h3>All clients <span class='muted' style='font-weight:400;'>· {len(customers)}</span></h3>",
        unsafe_allow_html=True,
    )
    if not customers:
        st.markdown("<p class='muted'>No client accounts yet.</p>", unsafe_allow_html=True)
        return

    rows = "".join(
        "<tr>"
        f"<td><strong style='color:var(--txt);'>{c['email']}</strong></td>"
        f"<td>{c['company'] or '—'}</td>"
        f"<td>{_audience_badge(c['audience'])}</td>"
        f"<td>{_human_dt(c['created_at'])}</td>"
        f"<td>{_human_dt(c['first_login_at'])}</td>"
        f"<td>{_human_dt(c['last_login_at'])}</td>"
        "</tr>"
        for c in customers
    )
    st.markdown(
        "<div class='card'><table class='stmx-table'><thead><tr>"
        "<th>Email</th><th>Company</th><th>Audience</th><th>Created</th><th>First login</th><th>Last login</th>"
        f"</tr></thead><tbody>{rows}</tbody></table></div>",
        unsafe_allow_html=True,
    )


# --- Tab: Key contacts ----------------------------------------------------

def _contacts_to_text(contacts) -> str:
    return "\n".join(f"{c['role']} | {c['contact']}" for c in contacts)


def _parse_contacts_text(text: str):
    out = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        if "|" in line:
            role, contact = line.split("|", 1)
        else:
            role, contact = line, ""
        role, contact = role.strip(), contact.strip()
        if role or contact:
            out.append({"role": role, "contact": contact})
    return out


def _contacts_editor() -> None:
    st.markdown("<h3>Key contacts</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p class='section-help'>Set the contacts each client sees on their Welcome page. "
        "One per line, formatted as <strong>Role | contact</strong>. "
        "Each client can be assigned different personnel.</p>",
        unsafe_allow_html=True,
    )

    customers = db.list_customers()
    if not customers:
        st.markdown("<p class='muted'>Create a client first.</p>", unsafe_allow_html=True)
        return

    options = {f"{(c['company'] or '—')} — {c['email']}": c["email"] for c in customers}
    label = st.selectbox("Client", list(options.keys()), key="contacts_client_select")
    email = options[label]

    nonce_key = f"contacts_nonce::{email}"
    nonce = st.session_state.get(nonce_key, 0)

    current = db.get_contacts(email)
    text = st.text_area(
        "Contacts",
        value=_contacts_to_text(current),
        height=200,
        key=f"contacts_text::{email}::{nonce}",
        label_visibility="collapsed",
    )

    # Live preview — a faithful replica of the "Key contacts" card the client
    # sees on their Welcome page. Values are HTML-escaped (the client page
    # escapes too), so role/contact text can never break the markup.
    parsed = _parse_contacts_text(text)
    prev_rows = "".join(
        f"<tr><td style='width:40%;'><strong style='color:var(--txt);'>{_html.escape(p['role']) or '—'}</strong></td>"
        f"<td style='color:#cabfe0;'>{_html.escape(p['contact']) or '—'}</td></tr>"
        for p in parsed
    ) or "<tr><td style='color:var(--faint);'>No contacts yet — add one above.</td></tr>"
    st.markdown(
        "<div class='preview-label'>Preview — exactly what the client sees on their Welcome page</div>"
        "<div class='preview-card'>"
        "<h4><i class='fa-solid fa-headset' style='color:var(--purple); margin-right:6px;'></i> Key contacts</h4>"
        f"<table class='stmx-table'><tbody>{prev_rows}</tbody></table>"
        "<p class='sla'>Response SLA: 4 business hours for Essential, 2 hours for Pro, 30 min for Enterprise.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        if st.button("Save contacts", key=f"save_contacts::{email}", type="primary"):
            db.set_contacts(email, parsed)
            st.success(f"Saved {len(parsed)} contact(s).")
    with c2:
        if st.button("Reset to default", key=f"reset_contacts::{email}"):
            db.set_contacts(email, db.DEFAULT_CONTACTS)
            st.session_state[nonce_key] = nonce + 1  # re-seed the textarea
            st.rerun()


# --- Tab: Activity --------------------------------------------------------

def _recent_logins_panel() -> None:
    events = db.recent_logins(50)
    total = db.count_logins()
    st.markdown(
        f"<h3>Recent logins <span class='muted' style='font-weight:400;'>· last 50 of {total}</span></h3>",
        unsafe_allow_html=True,
    )
    if not events:
        st.markdown("<p class='muted'>No logins recorded yet.</p>", unsafe_allow_html=True)
        return

    rows = ""
    for e in events:
        role_badge = (
            "<span class='badge badge-tsp'>staff</span>"
            if e["role"] == "staff"
            else "<span class='badge badge-grey'>customer</span>"
        )
        rows += (
            "<tr>"
            f"<td>{role_badge}</td>"
            f"<td>{e['email']}</td>"
            f"<td><span class='muted'>{e['method']}</span></td>"
            f"<td>{_human_dt(e['logged_in_at'])}</td>"
            "</tr>"
        )
    st.markdown(
        "<div class='card'><table class='stmx-table'><thead><tr>"
        "<th>Role</th><th>Identity</th><th>Method</th><th>When</th>"
        f"</tr></thead><tbody>{rows}</tbody></table></div>",
        unsafe_allow_html=True,
    )


# --- Overview -------------------------------------------------------------

def _kpis() -> None:
    customers = db.list_customers()
    fleet_n = sum(1 for c in customers if c["audience"] == "fleet")
    tsp_n = sum(1 for c in customers if c["audience"] == "tsp")
    logins = db.count_logins()
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi"><div class="kpi-label">Client accounts</div><div class="kpi-value grad-text">{len(customers)}</div></div>
            <div class="kpi"><div class="kpi-label">Fleet / TSP split</div><div class="kpi-value" style="color:var(--txt);">{fleet_n} <span class="unit">fleet</span> &nbsp;·&nbsp; {tsp_n} <span class="unit">tsp</span></div></div>
            <div class="kpi"><div class="kpi-label">Logins recorded</div><div class="kpi-value grad-text">{logins}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _topbar(identity: str, lang: str) -> None:
    pills = "".join(
        f"<a class='lang-pill{' active' if code == lang else ''}' target='_self' href='?lang={code}'>{label}</a>"
        for code, label in SUPPORTED_LANGS
    )
    safe_id = _html.escape(identity)
    st.markdown(
        "<div class='topbar'><div class='topbar-inner'>"
        "<div class='brand'><span class='grad-text'>Streamax</span> Staff</div>"
        "<details class='usermenu'>"
        "<summary>"
        "<span class='avatar'><i class='fa-solid fa-user'></i></span>"
        f"<span class='uname'>{safe_id}</span>"
        "<i class='fa-solid fa-chevron-down chev'></i>"
        "</summary>"
        "<div class='usermenu-pop'>"
        f"<div class='um-id'><div class='um-id-name'>{safe_id}</div><div class='um-id-tag'>Staff</div></div>"
        "<div class='um-label'>Language</div>"
        f"<div class='um-langs'>{pills}</div>"
        "<div class='um-divider'></div>"
        "<a class='um-item signout' target='_self' href='?logout=1'><i class='fa-solid fa-right-from-bracket'></i> Sign out</a>"
        "</div></details>"
        "</div></div>",
        unsafe_allow_html=True,
    )


def _apply_lang_bridge(lang: str) -> None:
    """Translate the PARENT document (the staff page) to `lang`, from a
    0-height helper iframe.

    English is the default and means *no translation*: we DON'T load the
    Google Translate engine and we clear any leftover `googtrans` cookie
    (Google scopes it to localhost, which the customer portal shares — a
    Spanish choice there must never bleed into the staff page). The engine
    is only injected when a non-English language is explicitly chosen."""
    if lang == "en":
        components.html(
            "<script>(function(){try{var p=window.parent,h=p.location.hostname,"
            "ex='=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';"
            "p.document.cookie='googtrans'+ex;"
            "p.document.cookie='googtrans'+ex+';domain='+h;"
            "p.document.cookie='googtrans'+ex+';domain=.'+h;"
            "}catch(e){}})();</script>",
            height=0,
        )
        return
    components.html(
        "<script>(function(){try{"
        "var p=window.parent,pdoc=p.document;"
        "if(!pdoc.getElementById('stmx_gt')){"
        "var d=pdoc.createElement('div');d.id='stmx_gt';d.style.display='none';pdoc.body.appendChild(d);"
        "p.googleTranslateElementInit=function(){new p.google.translate.TranslateElement("
        "{pageLanguage:'en',includedLanguages:'en,es,pt,fr',autoDisplay:false},'stmx_gt');};"
        "var s=pdoc.createElement('script');"
        "s.src='https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';"
        "pdoc.body.appendChild(s);"
        "var stl=pdoc.createElement('style');"
        "stl.innerHTML='.goog-te-banner-frame,.skiptranslate{display:none!important;}body{top:0!important;}"
        ".goog-text-highlight{background:none!important;box-shadow:none!important;}';"
        "pdoc.head.appendChild(stl);}"
        "var lang=" + _json.dumps(lang) + ";"
        "var n=0,iv=p.setInterval(function(){var c=pdoc.querySelector('.goog-te-combo');n++;"
        "if(c){c.value=lang;c.dispatchEvent(new Event('change'));p.clearInterval(iv);}"
        "else if(n>60){p.clearInterval(iv);}},200);"
        "}catch(e){}})();</script>",
        height=0,
    )


def render() -> None:
    _inject_css()

    identity = st.session_state.get("staff_identity", "staff")
    lang = st.session_state.get("ui_lang", "en")

    _topbar(identity, lang)

    st.markdown(
        "<h1><span class='grad-text'>Streamax</span> Staff</h1>"
        "<p class='staff-subtitle'>Onboarding portal administration</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr class='rule'>", unsafe_allow_html=True)
    _kpis()

    tab_clients, tab_contacts, tab_activity = st.tabs(["Clients", "Key contacts", "Activity"])
    with tab_clients:
        _create_client_form()
        st.write("")
        _customers_panel()
    with tab_contacts:
        _contacts_editor()
    with tab_activity:
        _recent_logins_panel()

    # Apply the chosen UI language to this (parent) page via Google Translate.
    _apply_lang_bridge(lang)
