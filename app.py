"""Streamax Customer Onboarding Portal.

Single-page Streamlit app. Customers authenticate via email + 6-digit code
(see login.py), then land on an 8-section onboarding journey rendered as
one HTML document via streamlit.components.v1.html.

Architecture mirrors the Sales Toolkit (../Sales Toolkit/salestoolkit/app.py):
- One html_head with shared CSS + nav + header
- Each section is a Python module exporting `content` (an HTML string)
- One html_tail with JS (switchTab, scroll observers)
- All concatenated and rendered once
"""
import html as _html

import streamlit as st
import streamlit.components.v1 as components

import db
import auth_cookie
from login import render_login
from staff import render as render_staff
from assets import MASCOT_DATA_URI

SUPPORTED_LANGS = ("en", "es", "pt", "fr")

# --- Section modules — each exports `content` (raw HTML) -------------------
try:
    from welcome import content as welcome_content
except ImportError as e:
    welcome_content = f"<div id='welcome' class='content-section'><h2 style='color:#ff4757;padding:40px;text-align:center;'>welcome.py: {e}</h2></div>"

try:
    from products import content as products_content
except ImportError as e:
    products_content = f"<div id='products' class='content-section hidden'><h2 style='color:#ff4757;padding:40px;text-align:center;'>products.py: {e}</h2></div>"

try:
    from installation import content as installation_content
except ImportError as e:
    installation_content = f"<div id='installation' class='content-section hidden'><h2 style='color:#ff4757;padding:40px;text-align:center;'>installation.py: {e}</h2></div>"

try:
    from training_academy import content as training_content
except ImportError as e:
    training_content = f"<div id='training' class='content-section hidden'><h2 style='color:#ff4757;padding:40px;text-align:center;'>training_academy.py: {e}</h2></div>"

try:
    from ai_features import content as ai_features_content
except ImportError as e:
    ai_features_content = f"<div id='ai-features' class='content-section hidden'><h2 style='color:#ff4757;padding:40px;text-align:center;'>ai_features.py: {e}</h2></div>"

try:
    from platform_tutorials import content as platform_content
except ImportError as e:
    platform_content = f"<div id='platform' class='content-section hidden'><h2 style='color:#ff4757;padding:40px;text-align:center;'>platform_tutorials.py: {e}</h2></div>"

try:
    from playbooks import content as playbooks_content
except ImportError as e:
    playbooks_content = f"<div id='playbooks' class='content-section hidden'><h2 style='color:#ff4757;padding:40px;text-align:center;'>playbooks.py: {e}</h2></div>"

try:
    from support import content as support_content
except ImportError as e:
    support_content = f"<div id='support' class='content-section hidden'><h2 style='color:#ff4757;padding:40px;text-align:center;'>support.py: {e}</h2></div>"



# --- Streamlit page config -------------------------------------------------
st.set_page_config(
    page_title="Streamax Customer Onboarding Portal",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden; height: 0 !important; min-height: 0 !important;}
    .block-container {
        padding: 0rem !important;
        margin: 0rem !important;
        max-width: 100% !important;
    }
    .stApp {
        background-color: #0c0a14;
        background-image: radial-gradient(circle at 50% -20%, #1c1330, #0c0a14);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Session state init ----------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- Cookie-based session persistence --------------------------------------
# Instantiate the cookie manager + re-hydrate session_state from the signed
# cookie BEFORE the auth gate, so a ?lang= reload (or a plain refresh) doesn't
# log the user out.
auth_cookie.init()
auth_cookie.restore()

# Handle ?logout=1
if st.query_params.get("logout") == "1":
    auth_cookie.clear()
    for k in ("authenticated", "user_role", "customer_email", "customer_company",
              "audience", "staff_identity", "ui_lang"):
        st.session_state.pop(k, None)
    st.session_state[auth_cookie.LOGOUT_FLAG] = True  # block cookie re-hydration
    st.query_params.clear()
    st.rerun()

# Handle ?lang=xx (UI language for the staff page; the customer portal uses its
# own in-iframe language modal). Kept in session + cookie so it survives reloads.
_qlang = st.query_params.get("lang")
if _qlang in SUPPORTED_LANGS:
    st.session_state["ui_lang"] = _qlang

# --- Gate ------------------------------------------------------------------
if not st.session_state["authenticated"]:
    render_login()
    st.stop()

# Authenticated → keep the cookie fresh.
auth_cookie.persist()

# --- Role routing: staff get the admin dashboard --------------------------
if st.session_state.get("user_role") == "staff":
    render_staff()
    st.stop()

# --- Authenticated as a customer: build the portal ------------------------
customer_email = st.session_state.get("customer_email", "Customer")
customer_company = st.session_state.get("customer_company", "")
audience = st.session_state.get("audience", "fleet")  # fleet | tsp

audience_label = "Fleet Operator" if audience == "fleet" else "TSP / Channel Partner"
identity_display = customer_company or customer_email

# Per-client key contacts → rendered into the Welcome section's placeholder.
# Each client may be assigned different personnel; staff set these in the
# staff dashboard. Falls back to DEFAULT_CONTACTS when unset.
_contacts = db.get_contacts(customer_email)
_contacts_rows = "".join(
    f"<tr><td><strong>{_html.escape(c['role'])}</strong></td>"
    f"<td>{_html.escape(c['contact'])}</td></tr>"
    for c in _contacts
    if c.get("role") or c.get("contact")
)
welcome_content = welcome_content.replace("__KEY_CONTACTS__", _contacts_rows)

html_head = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Streamax Customer Onboarding</title>

    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        :root {
            --bg-deep: #0c0a14;
            --bg-gradient: radial-gradient(circle at 50% -20%, #1c1330, #0c0a14);
            --gold: #F4C95D;
            --purple: #A06BFF;
            --text-white: #FFFFFF;
            --text-grey: #A89FB8;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: 1px solid rgba(255, 255, 255, 0.08);
            --card-radius: 16px;
            --font-main: 'Inter', sans-serif;
            --font-display: 'Sora', 'Inter', sans-serif;
            --glow-shadow: 0 0 20px rgba(244, 201, 93, 0.15);
            --gradient-text: linear-gradient(135deg, var(--gold) 0%, var(--purple) 100%);
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            /* Shadows tinted toward the plum background, never pure black */
            --shadow-soft: 0 10px 30px rgba(14, 9, 28, 0.45);
            --shadow-lift: 0 18px 44px rgba(14, 9, 28, 0.55);
            --edge-highlight: inset 0 1px 0 rgba(255, 255, 255, 0.07);
        }

        * { box-sizing: border-box; }
        html, body {
            margin: 0;
            padding: 0;
            background: var(--bg-deep);
            background-image: var(--bg-gradient);
            color: var(--text-white);
            font-family: var(--font-main);
            line-height: 1.6;
            min-height: 100vh;
        }

        .container { max-width: 1280px; margin: 0 auto; padding: 0 20px; position: relative; }

        /* --- Header --- */
        header { text-align: center; padding: 64px 0 34px; animation: fadeInDown 1s ease-out; }
        .header-subtitle { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.22em; color: var(--gold); margin-bottom: 14px; }
        .header-meta { margin-top: 10px; font-size: 0.9rem; color: var(--text-grey); opacity: 0.85; }
        .gradient-text { background: var(--gradient-text); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

        /* Mascot beside title */
        .header-title-row { display: flex; align-items: center; justify-content: center; gap: 28px; flex-wrap: wrap; }
        .header-title-row h1 { margin: 0; text-align: left; }
        @keyframes mascot-float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        .header-mascot {
            width: 120px; height: 120px; object-fit: contain; flex-shrink: 0;
            animation: mascot-float 4s ease-in-out infinite;
            filter: drop-shadow(0 12px 18px rgba(244, 201, 93, 0.18));
        }
        @media (max-width: 700px) {
            .header-title-row { gap: 14px; }
            .header-title-row h1 { text-align: center; font-size: 2rem !important; }
            .header-mascot { width: 84px; height: 84px; }
        }

        /* --- Navigation (sticky top bar, minimalist) --- */
        .nav-tabs {
            position: sticky;
            top: 0;
            z-index: 1000;
            background: rgba(5, 8, 16, 0.82);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.07);
            padding: 18px 24px 6px;
        }
        .nav-inner {
            max-width: 1320px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: nowrap;
        }
        .nav-links { display: flex; align-items: center; flex-wrap: wrap; }

        /* --- User menu (consolidated into the nav) --- */
        .nav-user { position: relative; flex-shrink: 0; }
        .user-trigger {
            display: inline-flex; align-items: center; gap: 10px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 30px; padding: 6px 12px 6px 6px;
            cursor: pointer; font-family: var(--font-main);
            transition: var(--transition);
        }
        .user-trigger:hover { border-color: rgba(244,201,93,0.4); background: rgba(255,255,255,0.07); }
        .user-avatar {
            width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0;
            display: flex; align-items: center; justify-content: center;
            background: linear-gradient(135deg, var(--gold), var(--purple));
            color: #0c0a14; font-size: 0.85rem;
        }
        .user-trigger .user-name { color: var(--text-white); font-weight: 600; font-size: 0.85rem; max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .user-trigger .user-chevron { color: var(--text-grey); font-size: 0.7rem; transition: transform 0.25s ease; }
        .nav-user.open .user-chevron { transform: rotate(180deg); }

        .user-dropdown {
            position: absolute; top: calc(100% + 10px); right: 0;
            min-width: 230px; z-index: 1200;
            background: rgba(13, 18, 33, 0.97);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 14px; padding: 8px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
            opacity: 0; visibility: hidden; transform: translateY(-8px);
            transition: opacity 0.2s ease, transform 0.2s ease, visibility 0.2s;
        }
        .nav-user.open .user-dropdown { opacity: 1; visibility: visible; transform: translateY(0); }
        .ud-header { padding: 12px 14px 14px; border-bottom: 1px solid rgba(255,255,255,0.07); margin-bottom: 6px; }
        .ud-name { color: var(--text-white); font-weight: 700; font-size: 0.92rem; margin-bottom: 4px; }
        .ud-tag { color: var(--purple); font-size: 0.66rem; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; }
        .ud-item {
            width: 100%; display: flex; align-items: center; gap: 12px;
            background: transparent; border: none; border-radius: 9px;
            padding: 11px 14px; cursor: pointer; text-align: left;
            color: var(--text-grey); font-family: var(--font-main); font-size: 0.88rem; font-weight: 500;
            text-decoration: none; transition: var(--transition);
        }
        .ud-item i { width: 16px; text-align: center; font-size: 0.95rem; }
        .ud-item span { flex: 1; }
        .ud-item:hover { background: rgba(255,255,255,0.06); color: var(--text-white); }
        .ud-item .ud-current { flex: 0; color: var(--gold); font-size: 0.78rem; font-weight: 600; }
        .ud-signout:hover { background: rgba(255,107,107,0.10); color: #ff6b6b; }
        .ud-signout:hover i { color: #ff6b6b; }

        /* --- Language modal --- */
        .lang-overlay {
            position: fixed; inset: 0; z-index: 2000;
            display: flex; align-items: center; justify-content: center;
            background: rgba(3, 6, 14, 0.72);
            backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
            opacity: 0; visibility: hidden; transition: opacity 0.25s ease, visibility 0.25s;
            padding: 20px;
        }
        .lang-overlay.open { opacity: 1; visibility: visible; }
        .lang-modal {
            width: 100%; max-width: 520px; position: relative;
            background: linear-gradient(160deg, rgba(18,24,40,0.98), rgba(8,12,22,0.98));
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 20px; padding: 32px 30px 30px;
            box-shadow: 0 30px 80px rgba(0,0,0,0.6);
            transform: translateY(16px) scale(0.98); transition: transform 0.28s cubic-bezier(0.4,0,0.2,1);
        }
        .lang-overlay.open .lang-modal { transform: translateY(0) scale(1); }
        .lang-modal h3 { font-size: 1.45rem; margin-bottom: 6px; color: var(--text-white); }
        .lang-modal .lang-sub { color: var(--text-grey); font-size: 0.9rem; margin: 0 0 24px; }
        .lang-modal-close {
            position: absolute; top: 18px; right: 18px;
            width: 34px; height: 34px; border-radius: 50%;
            background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
            color: var(--text-grey); cursor: pointer; font-size: 0.95rem; transition: var(--transition);
            display: flex; align-items: center; justify-content: center;
        }
        .lang-modal-close:hover { color: var(--text-white); background: rgba(255,255,255,0.1); transform: rotate(90deg); }
        .lang-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
        @media (max-width: 480px) { .lang-grid { grid-template-columns: 1fr; } }
        .lang-card {
            display: flex; align-items: center; gap: 14px;
            background: rgba(255,255,255,0.03); border: 1.5px solid rgba(255,255,255,0.08);
            border-radius: 14px; padding: 16px 18px; cursor: pointer;
            font-family: var(--font-main); text-align: left; transition: var(--transition);
        }
        .lang-card:hover { border-color: rgba(244,201,93,0.5); background: rgba(244,201,93,0.06); transform: translateY(-2px); }
        .lang-card.selected { border-color: var(--gold); background: rgba(244,201,93,0.10); box-shadow: var(--glow-shadow); }
        .lang-card .lang-flag { font-size: 1.8rem; line-height: 1; }
        .lang-card .lang-meta { display: flex; flex-direction: column; }
        .lang-card .lang-label { color: var(--text-white); font-weight: 700; font-size: 0.98rem; }
        .lang-card .lang-native { color: var(--text-grey); font-size: 0.8rem; }
        .lang-card .lang-check { margin-left: auto; color: var(--gold); font-size: 1rem; opacity: 0; transition: opacity 0.2s ease; }
        .lang-card.selected .lang-check { opacity: 1; }

        /* Hide Google Translate injected chrome — we drive it from our own UI */
        .goog-te-banner-frame, .goog-te-gadget, #goog-gt-tt, .goog-te-balloon-frame { display: none !important; }
        .skiptranslate { display: none !important; }
        body { top: 0 !important; }
        .goog-text-highlight { background: none !important; box-shadow: none !important; }
        #google_translate_element { display: none !important; }
        .nav-btn {
            background: transparent;
            border: none;
            color: var(--text-grey);
            padding: 18px 18px;
            font-family: var(--font-main);
            font-weight: 500;
            font-size: 0.92rem;
            letter-spacing: 0.2px;
            cursor: pointer;
            position: relative;
            transition: color 0.25s ease;
        }
        .nav-btn::after {
            content: '';
            position: absolute;
            left: 18px; right: 18px; bottom: 0;
            height: 2px; border-radius: 2px;
            background: linear-gradient(90deg, var(--gold), var(--purple));
            transform: scaleX(0);
            transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .nav-btn:hover { color: var(--text-white); }
        .nav-btn.active { color: var(--text-white); }
        .nav-btn.active::after { transform: scaleX(1); }

        /* --- Glass cards --- */
        .card {
            background: linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.02));
            border: var(--glass-border); border-radius: var(--card-radius);
            padding: 30px; margin-bottom: 24px; backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
            transition: var(--transition); box-shadow: var(--shadow-soft), var(--edge-highlight);
            position: relative; overflow: hidden;
        }
        .card:hover { border-color: rgba(244,201,93,0.28); box-shadow: var(--shadow-lift), var(--edge-highlight); transform: translateY(-3px); }

        .glass-panel {
            background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.018));
            border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 24px;
            transition: var(--transition); box-shadow: var(--edge-highlight);
        }
        .glass-panel:hover { border-color: rgba(244,201,93,0.22); box-shadow: var(--shadow-soft), var(--edge-highlight); transform: translateY(-2px); }

        /* Glassmorphism fallback — solid fills when the OS asks for less transparency */
        @media (prefers-reduced-transparency: reduce) {
            .card, .glass-panel { background: #171226; backdrop-filter: none; -webkit-backdrop-filter: none; }
            .nav-tabs { background: #0b0814; backdrop-filter: none; -webkit-backdrop-filter: none; }
        }

        h1, h2, h3, h4 { color: var(--text-white); margin-top: 0; font-family: var(--font-display); letter-spacing: -0.015em; }
        h1 { letter-spacing: -0.03em; }
        h2 { font-size: 1.85rem; margin-bottom: 16px; font-weight: 700; letter-spacing: -0.02em; }
        h3 { font-size: 1.3rem; margin-bottom: 12px; font-weight: 600; }
        h4 { font-size: 1.05rem; margin-bottom: 8px; font-weight: 600; }
        p { color: var(--text-grey); }
        a { color: var(--purple); text-decoration: none; }
        a:hover { color: var(--gold); }

        .section-header { font-family: var(--font-display); margin-top: 44px; margin-bottom: 22px; border-left: 3px solid var(--gold); padding-left: 16px; font-size: 1.5rem; font-weight: 700; letter-spacing: -0.02em; color: var(--text-white); }

        /* --- Sections --- */
        .content-section { animation: fadeIn 0.5s ease-out; }
        .content-section.hidden { display: none; }

        /* --- Animations --- */
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
        .fade-up { opacity: 0; transform: translateY(20px); transition: all 0.6s ease-out; }
        .fade-up.visible { opacity: 1; transform: translateY(0); }

        /* Honor the OS reduced-motion preference: kill loops + entrance motion */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.001ms !important; animation-iteration-count: 1 !important;
                transition-duration: 0.001ms !important; scroll-behavior: auto !important;
            }
            .fade-up { opacity: 1 !important; transform: none !important; }
            .card:hover, .glass-panel:hover { transform: none !important; }
        }

        /* --- CTA button --- */
        .cta-btn {
            display: inline-flex; align-items: center; gap: 10px;
            background: linear-gradient(135deg, #F4C95D 0%, #A06BFF 100%);
            color: #0c0a14 !important; font-weight: 700; font-size: 0.95rem;
            padding: 13px 30px; border-radius: 30px; text-decoration: none; letter-spacing: -0.01em;
            transition: all 0.3s ease; border: none; cursor: pointer;
            box-shadow: 0 10px 24px rgba(160,107,255,0.22);
        }
        .cta-btn:hover { transform: translateY(-2px); box-shadow: 0 16px 34px rgba(160,107,255,0.34); color: #0c0a14 !important; }
        .cta-btn.secondary {
            background: transparent; color: var(--gold) !important;
            border: 1px solid rgba(244,201,93,0.4); box-shadow: none;
        }
        .cta-btn.secondary:hover { background: rgba(244,201,93,0.08); color: var(--gold) !important; }

        /* --- Pipeline (roadmap) --- */
        /* padding-top gives the hover-scaled icon + glow room so overflow-x:auto
           (needed for horizontal scroll) doesn't clip them at the top. The
           connector line top is shifted by the same amount to stay centered. */
        .pipeline-container { display: flex; justify-content: space-between; align-items: flex-start; position: relative; margin: 8px 0 10px; overflow-x: auto; overflow-y: hidden; padding: 30px 0 20px; gap: 12px; }
        .pipeline-line { position: absolute; top: 54px; left: 40px; right: 40px; height: 2px; background: linear-gradient(90deg, var(--gold), var(--purple)); opacity: 0.4; z-index: 1; }
        .pipeline-step { position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; text-align: center; min-width: 130px; flex: 1; }
        .pipeline-icon { width: 50px; height: 50px; border-radius: 50%; background: var(--bg-deep); border: 2px solid var(--gold); display: flex; justify-content: center; align-items: center; font-size: 1.2rem; color: var(--gold); margin-bottom: 12px; box-shadow: 0 0 15px rgba(244,201,93,0.15); transition: var(--transition); }
        .pipeline-step:hover .pipeline-icon { transform: scale(1.1); box-shadow: 0 0 25px rgba(244,201,93,0.4); }
        .pipeline-step:nth-child(even) .pipeline-icon { border-color: var(--purple); color: var(--purple); }
        .pipeline-title { color: var(--text-white); font-size: 0.85rem; font-weight: 700; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px; }
        .pipeline-desc { color: var(--text-grey); font-size: 0.78rem; line-height: 1.4; }

        /* --- Grid helpers --- */
        .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
        @media (max-width: 900px) {
            .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
            header { padding: 40px 0 20px; }
            .nav-tabs { padding: 0 10px; }
            .nav-inner { justify-content: center; }
            .nav-btn { padding: 13px 10px; font-size: 0.78rem; }
            .nav-btn::after { left: 10px; right: 10px; }
            .user-trigger .user-name { max-width: 110px; font-size: 0.78rem; }
        }

        /* --- Tables --- */
        .stmx-table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.92rem; }
        .stmx-table th { background: rgba(244,201,93,0.08); color: var(--gold); text-align: left; padding: 12px 14px; font-weight: 700; border-bottom: 2px solid rgba(244,201,93,0.25); }
        .stmx-table td { padding: 11px 14px; color: var(--text-grey); border-bottom: 1px solid rgba(255,255,255,0.05); }
        .stmx-table tr:hover td { background: rgba(255,255,255,0.02); color: var(--text-white); }

        /* --- Badges --- */
        .badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
        .badge-green { background: rgba(244,201,93,0.15); color: var(--gold); border: 1px solid rgba(244,201,93,0.3); }
        .badge-blue { background: rgba(160,107,255,0.15); color: var(--purple); border: 1px solid rgba(160,107,255,0.3); }
        .badge-amber { background: rgba(251,191,36,0.12); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }

        /* --- Checklist --- */
        .checklist { list-style: none; padding: 0; margin: 0; }
        .checklist li { padding: 10px 0 10px 32px; position: relative; color: var(--text-grey); border-bottom: 1px solid rgba(255,255,255,0.04); }
        .checklist li:last-child { border-bottom: none; }
        .checklist li::before { content: '\f00c'; font-family: 'Font Awesome 6 Free'; font-weight: 900; position: absolute; left: 6px; top: 12px; color: var(--gold); font-size: 0.85rem; }
        .checklist li strong { color: var(--text-white); }

        /* --- Video placeholder --- */
        .video-card { background: linear-gradient(135deg, rgba(160,107,255,0.08), rgba(244,201,93,0.04)); border: 1px solid rgba(160,107,255,0.2); border-radius: 12px; padding: 20px; display: flex; gap: 16px; align-items: center; transition: var(--transition); cursor: pointer; margin-bottom: 12px; }
        .video-card:hover { border-color: var(--gold); transform: translateX(4px); }
        .video-thumb { width: 64px; height: 64px; border-radius: 8px; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: var(--gold); font-size: 1.5rem; }
        .video-meta { flex: 1; }
        .video-title { color: var(--text-white); font-weight: 600; margin-bottom: 4px; font-size: 0.98rem; }
        .video-sub { color: var(--text-grey); font-size: 0.8rem; }
    </style>
</head>
<body>

    <!-- STICKY NAV (very top) — tabs + consolidated user menu -->
    <nav class="nav-tabs">
        <div class="nav-inner">
            <div class="nav-links">
                <button class="nav-btn active" data-tab="welcome" onclick="switchTab('welcome', this)">Welcome</button>
                <button class="nav-btn" data-tab="products" onclick="switchTab('products', this)">My Products</button>
                <button class="nav-btn" data-tab="installation" onclick="switchTab('installation', this)">Installation</button>
                <button class="nav-btn" data-tab="platform" onclick="switchTab('platform', this)">Platform Tutorials</button>
                <button class="nav-btn" data-tab="ai-features" onclick="switchTab('ai-features', this)">AI Features</button>
                <button class="nav-btn" data-tab="training" onclick="switchTab('training', this)">Training Academy</button>
                <button class="nav-btn" data-tab="playbooks" onclick="switchTab('playbooks', this)">Playbooks</button>
                <button class="nav-btn" data-tab="support" onclick="switchTab('support', this)">Support</button>
            </div>

            <div class="nav-user" id="nav-user">
                <button class="user-trigger" onclick="toggleUserMenu(event)" aria-haspopup="true">
                    <span class="user-avatar"><i class="fa-solid fa-user"></i></span>
                    <span class="user-name">__IDENTITY__</span>
                    <i class="fa-solid fa-chevron-down user-chevron"></i>
                </button>
                <div class="user-dropdown" id="user-dropdown" role="menu">
                    <div class="ud-header">
                        <div class="ud-name">__IDENTITY__</div>
                        <div class="ud-tag">__AUDIENCE__</div>
                    </div>
                    <button class="ud-item" role="menuitem" onclick="openLangModal()" translate="no">
                        <i class="fa-solid fa-globe"></i>
                        <span>Language</span>
                        <span class="ud-current" id="ud-current-lang">English</span>
                    </button>
                    <a class="ud-item ud-signout" role="menuitem" href="?logout=1" translate="no" onclick="
                        (function(evt) {
                            evt.preventDefault();
                            var base = '';
                            try { if (document.referrer) base = document.referrer; } catch (e) {}
                            if (!base) { try { base = window.parent.location.href; } catch (e) {} }
                            if (!base) base = window.location.href;
                            var url = base.split('?')[0].split('#')[0] + '?logout=1';
                            try { window.parent.location.href = url; }
                            catch (e) {
                                try { window.top.location.href = url; }
                                catch (e2) { window.location.href = url; }
                            }
                        })(event);
                        return false;
                    "><i class="fa-solid fa-right-from-bracket"></i><span>Sign out</span></a>
                </div>
            </div>
        </div>
    </nav>

    <!-- LANGUAGE MODAL -->
    <div class="lang-overlay" id="lang-overlay" onclick="if (event.target === this) closeLangModal()">
        <div class="lang-modal" translate="no">
            <button class="lang-modal-close" onclick="closeLangModal()" aria-label="Close"><i class="fa-solid fa-xmark"></i></button>
            <h3>Choose your language</h3>
            <p class="lang-sub">The portal will switch instantly — no reload needed.</p>
            <div class="lang-grid">
                <button class="lang-card selected" data-lang="en" onclick="selectLanguage('en', this)">
                    <span class="lang-flag">🇬🇧</span>
                    <span class="lang-meta"><span class="lang-label">English</span><span class="lang-native">Default</span></span>
                    <i class="fa-solid fa-circle-check lang-check"></i>
                </button>
                <button class="lang-card" data-lang="es" onclick="selectLanguage('es', this)">
                    <span class="lang-flag">🇪🇸</span>
                    <span class="lang-meta"><span class="lang-label">Spanish</span><span class="lang-native">Español</span></span>
                    <i class="fa-solid fa-circle-check lang-check"></i>
                </button>
                <button class="lang-card" data-lang="pt" onclick="selectLanguage('pt', this)">
                    <span class="lang-flag">🇧🇷</span>
                    <span class="lang-meta"><span class="lang-label">Portuguese</span><span class="lang-native">Português</span></span>
                    <i class="fa-solid fa-circle-check lang-check"></i>
                </button>
                <button class="lang-card" data-lang="fr" onclick="selectLanguage('fr', this)">
                    <span class="lang-flag">🇫🇷</span>
                    <span class="lang-meta"><span class="lang-label">French</span><span class="lang-native">Français</span></span>
                    <i class="fa-solid fa-circle-check lang-check"></i>
                </button>
            </div>
        </div>
    </div>

    <!-- Hidden Google Translate engine — driven by the modal above -->
    <div id="google_translate_element"></div>

    <!-- HEADER / HERO -->
    <header>
        <div class="container">
            <div class="header-subtitle fade-up">Streamax Customer Onboarding</div>
            <div class="header-title-row fade-up">
                <img src="__MASCOT_SRC__"
                     alt="Streamax Mascot" class="header-mascot"
                     onerror="this.style.display='none';">
                <h1 style="font-size: 2.8rem; line-height: 1.15;">
                    Welcome to the <span class="gradient-text">Streamax</span> family
                </h1>
            </div>
            <div class="header-meta fade-up">Your guided journey — from unboxing to fleet-wide AI safety</div>
            <div class="header-meta fade-up" style="font-size: 0.75rem; opacity: 0.6;">v1.0 • For fleets &amp; TSP partners • support@streamax.com</div>
        </div>
    </header>

    <div class="container">
"""

html_tail = r"""
    </div>

    <script>
        function switchTab(tabId, btnElement) {
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            var navBtn = btnElement || document.querySelector('.nav-btn[data-tab="' + tabId + '"]');
            if (navBtn) navBtn.classList.add('active');

            document.querySelectorAll('.content-section').forEach(s => s.classList.add('hidden'));
            const target = document.getElementById(tabId);
            if (target) {
                target.classList.remove('hidden');
                target.querySelectorAll('.fade-up').forEach(el => {
                    el.classList.remove('visible');
                    setTimeout(() => el.classList.add('visible'), 50);
                });
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }

        function observeElements() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
            }, { threshold: 0.1 });
            document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));
        }

        /* ---- User menu dropdown ---- */
        function toggleUserMenu(e) {
            e.stopPropagation();
            document.getElementById('nav-user').classList.toggle('open');
        }
        document.addEventListener('click', function (e) {
            var nu = document.getElementById('nav-user');
            if (nu && !nu.contains(e.target)) nu.classList.remove('open');
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                closeLangModal();
                var nu = document.getElementById('nav-user');
                if (nu) nu.classList.remove('open');
            }
        });

        /* ---- Language modal ---- */
        var LANG_LABELS = { en: 'English', es: 'Español', pt: 'Português', fr: 'Français' };

        function openLangModal() {
            document.getElementById('nav-user').classList.remove('open');
            document.getElementById('lang-overlay').classList.add('open');
        }
        function closeLangModal() {
            var ov = document.getElementById('lang-overlay');
            if (ov) ov.classList.remove('open');
        }

        function selectLanguage(lang, cardEl) {
            document.querySelectorAll('.lang-card').forEach(c => c.classList.remove('selected'));
            if (cardEl) cardEl.classList.add('selected');
            var cur = document.getElementById('ud-current-lang');
            if (cur) cur.textContent = LANG_LABELS[lang] || 'English';
            try { localStorage.setItem('portal_lang', lang); } catch (e) {}
            applyTranslation(lang);
            setTimeout(closeLangModal, 280);
        }

        /* Drive the hidden Google Translate combo. Retry until it's injected. */
        function applyTranslation(lang) {
            var tries = 0;
            var iv = setInterval(function () {
                var combo = document.querySelector('.goog-te-combo');
                tries++;
                if (combo) {
                    combo.value = lang;
                    combo.dispatchEvent(new Event('change'));
                    clearInterval(iv);
                } else if (tries > 50) {
                    clearInterval(iv);
                }
            }, 150);
        }

        /* ---- Google Translate engine init (called by the injected script) ---- */
        function googleTranslateElementInit() {
            new google.translate.TranslateElement(
                { pageLanguage: 'en', includedLanguages: 'en,es,pt,fr', autoDisplay: false },
                'google_translate_element'
            );
            // Re-apply a previously chosen language on reload
            try {
                var saved = localStorage.getItem('portal_lang');
                if (saved && saved !== 'en' && LANG_LABELS[saved]) {
                    var card = document.querySelector('.lang-card[data-lang="' + saved + '"]');
                    if (card) {
                        document.querySelectorAll('.lang-card').forEach(c => c.classList.remove('selected'));
                        card.classList.add('selected');
                    }
                    var cur = document.getElementById('ud-current-lang');
                    if (cur) cur.textContent = LANG_LABELS[saved];
                    applyTranslation(saved);
                }
            } catch (e) {}
        }

        document.addEventListener('DOMContentLoaded', () => {
            observeElements();
            const first = document.getElementById('welcome');
            if (first) first.querySelectorAll('.fade-up').forEach(el => el.classList.add('visible'));
        });
    </script>
    <script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</body>
</html>
"""

# Substitute identity + asset placeholders
html_head_filled = (
    html_head
    .replace("__MASCOT_SRC__", MASCOT_DATA_URI)
    .replace("__IDENTITY__", identity_display)
    .replace("__AUDIENCE__", audience_label)
)

full_html = (
    html_head_filled
    + welcome_content
    + products_content
    + installation_content
    + platform_content
    + ai_features_content
    + training_content
    + playbooks_content
    + support_content
    + html_tail
)

# Customer-portal-only CSS: make the portal iframe the full-viewport scroll
# container so its sticky nav pins to the top. Scoped to title="st.iframe"
# (components.html) so it never touches the hidden cookie-manager iframe — and
# only injected here, on the customer page (not on login/staff).
st.markdown(
    """
    <style>
    .stApp { overflow: hidden; }
    /* Kill all of Streamlit's default top/side spacing so the portal iframe
       sits flush at y=0 — otherwise stMainBlockContainer's ~6rem top padding
       leaves an empty strip above the sticky nav. */
    [data-testid="stHeader"], header[data-testid="stHeader"] { display: none !important; height: 0 !important; }
    [data-testid="stAppViewContainer"] > .main, [data-testid="stMain"] { padding: 0 !important; }
    [data-testid="stMainBlockContainer"], .stMainBlockContainer, .block-container { padding: 0.6rem 0 0 0 !important; margin: 0 !important; max-width: 100% !important; }
    [data-testid="stVerticalBlock"] { gap: 0 !important; }
    [data-testid="stElementContainer"] { margin: 0 !important; }
    [data-testid="stIFrame"] { height: 100vh !important; line-height: 0; margin: 0 !important; }
    [data-testid="stIFrame"] iframe, .stApp iframe[title="st.iframe"] { height: 100vh !important; width: 100% !important; border: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Height is a fallback — the CSS above forces the iframe to 100vh so it becomes
# the scroll container and the sticky nav inside it actually pins to the top.
components.html(full_html, height=1000, scrolling=True)
