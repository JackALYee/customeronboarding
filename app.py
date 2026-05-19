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
import streamlit as st
import streamlit.components.v1 as components

from login import render_login
from staff import render as render_staff

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
    header {visibility: hidden;}
    .block-container {
        padding: 0rem !important;
        margin: 0rem !important;
        max-width: 100% !important;
    }
    .stApp {
        background-color: #050810;
        background-image: radial-gradient(circle at 50% -20%, #0B1221, #050810);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Session state init ----------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Handle ?logout=1
if st.query_params.get("logout") == "1":
    for k in ("authenticated", "user_role", "customer_email", "customer_company", "audience", "staff_identity"):
        st.session_state.pop(k, None)
    st.query_params.clear()
    st.rerun()

# --- Gate ------------------------------------------------------------------
if not st.session_state["authenticated"]:
    render_login()
    st.stop()

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

html_head = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Streamax Customer Onboarding</title>

    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        :root {
            --bg-deep: #050810;
            --bg-gradient: radial-gradient(circle at 50% -20%, #0B1221, #050810);
            --primary-green: #2AF598;
            --secondary-blue: #009EFD;
            --text-white: #FFFFFF;
            --text-grey: #A0AEC0;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: 1px solid rgba(255, 255, 255, 0.08);
            --card-radius: 16px;
            --font-main: 'Inter', sans-serif;
            --glow-shadow: 0 0 20px rgba(42, 245, 152, 0.15);
            --gradient-text: linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-blue) 100%);
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
        header { text-align: center; padding: 60px 0 30px; animation: fadeInDown 1s ease-out; }
        .header-subtitle { font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-green); margin-bottom: 10px; }
        .header-meta { margin-top: 10px; font-size: 0.85rem; color: var(--text-grey); opacity: 0.8; }
        .gradient-text { background: var(--gradient-text); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

        /* --- User identity pill --- */
        .user-pill { position: fixed; top: 18px; right: 24px; z-index: 9999; display: flex; align-items: center; gap: 10px; background: rgba(10,15,30,0.85); border: 1px solid rgba(42,245,152,0.25); padding: 8px 16px; border-radius: 30px; backdrop-filter: blur(10px); }
        .user-pill .user-icon { color: var(--primary-green); font-size: 1.1rem; }
        .user-pill .user-identity { color: var(--text-white); font-weight: 600; font-size: 0.85rem; max-width: 220px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .user-pill .audience-tag { color: var(--secondary-blue); font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; padding-left: 8px; border-left: 1px solid rgba(255,255,255,0.15); }
        .user-pill .signout-btn { color: var(--text-grey); font-size: 0.78rem; padding: 4px 12px; border-radius: 20px; text-decoration: none; border: 1px solid rgba(255,255,255,0.1); transition: var(--transition); }
        .user-pill .signout-btn:hover { color: #ff6b6b; border-color: #ff6b6b; background: rgba(255,107,107,0.08); }

        /* --- Navigation tabs --- */
        .nav-tabs { display: flex; justify-content: center; gap: 12px; margin-bottom: 40px; flex-wrap: wrap; padding: 0 10px; }
        .nav-btn {
            background: rgba(255,255,255,0.05); border: var(--glass-border); color: var(--text-grey);
            padding: 11px 20px; border-radius: 30px; cursor: pointer; font-weight: 600;
            transition: var(--transition); backdrop-filter: blur(5px); font-family: var(--font-main);
            display: inline-flex; align-items: center; gap: 8px; font-size: 0.88rem;
        }
        .nav-btn:hover { background: rgba(255,255,255,0.1); color: var(--text-white); transform: translateY(-2px); }
        .nav-btn.active { background: rgba(42,245,152,0.1); border-color: var(--primary-green); color: var(--primary-green); box-shadow: var(--glow-shadow); }

        /* --- Glass cards --- */
        .card {
            background: var(--glass-bg); border: var(--glass-border); border-radius: var(--card-radius);
            padding: 30px; margin-bottom: 24px; backdrop-filter: blur(12px); transition: var(--transition);
            position: relative; overflow: hidden;
        }
        .card:hover { border-color: rgba(42,245,152,0.25); box-shadow: 0 10px 30px rgba(0,0,0,0.3); transform: translateY(-3px); }

        .glass-panel { background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 24px; transition: var(--transition); }
        .glass-panel:hover { border-color: rgba(42,245,152,0.2); }

        h1, h2, h3, h4 { color: var(--text-white); margin-top: 0; }
        h2 { font-size: 1.8rem; margin-bottom: 16px; font-weight: 700; }
        h3 { font-size: 1.3rem; margin-bottom: 12px; font-weight: 600; }
        h4 { font-size: 1.05rem; margin-bottom: 8px; font-weight: 600; }
        p { color: var(--text-grey); }
        a { color: var(--secondary-blue); text-decoration: none; }
        a:hover { color: var(--primary-green); }

        .section-header { margin-top: 36px; margin-bottom: 20px; border-left: 4px solid var(--primary-green); padding-left: 16px; font-size: 1.45rem; color: var(--text-white); }

        /* --- Sections --- */
        .content-section { animation: fadeIn 0.5s ease-out; }
        .content-section.hidden { display: none; }

        /* --- Animations --- */
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
        .fade-up { opacity: 0; transform: translateY(20px); transition: all 0.6s ease-out; }
        .fade-up.visible { opacity: 1; transform: translateY(0); }

        /* --- CTA button --- */
        .cta-btn {
            display: inline-flex; align-items: center; gap: 10px;
            background: linear-gradient(135deg, #2AF598 0%, #009EFD 100%);
            color: #050810 !important; font-weight: 700; font-size: 0.95rem;
            padding: 12px 28px; border-radius: 30px; text-decoration: none;
            transition: all 0.3s ease; border: none; cursor: pointer;
            box-shadow: 0 8px 20px rgba(42,245,152,0.18);
        }
        .cta-btn:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(42,245,152,0.28); color: #050810 !important; }
        .cta-btn.secondary {
            background: transparent; color: var(--primary-green) !important;
            border: 1px solid rgba(42,245,152,0.4); box-shadow: none;
        }
        .cta-btn.secondary:hover { background: rgba(42,245,152,0.08); color: var(--primary-green) !important; }

        /* --- Pipeline (roadmap) --- */
        .pipeline-container { display: flex; justify-content: space-between; align-items: flex-start; position: relative; margin: 30px 0 10px; overflow-x: auto; padding-bottom: 20px; gap: 12px; }
        .pipeline-line { position: absolute; top: 24px; left: 40px; right: 40px; height: 2px; background: linear-gradient(90deg, var(--primary-green), var(--secondary-blue)); opacity: 0.4; z-index: 1; }
        .pipeline-step { position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; text-align: center; min-width: 130px; flex: 1; }
        .pipeline-icon { width: 50px; height: 50px; border-radius: 50%; background: var(--bg-deep); border: 2px solid var(--primary-green); display: flex; justify-content: center; align-items: center; font-size: 1.2rem; color: var(--primary-green); margin-bottom: 12px; box-shadow: 0 0 15px rgba(42,245,152,0.15); transition: var(--transition); }
        .pipeline-step:hover .pipeline-icon { transform: scale(1.1); box-shadow: 0 0 25px rgba(42,245,152,0.4); }
        .pipeline-step:nth-child(even) .pipeline-icon { border-color: var(--secondary-blue); color: var(--secondary-blue); }
        .pipeline-title { color: var(--text-white); font-size: 0.85rem; font-weight: 700; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px; }
        .pipeline-desc { color: var(--text-grey); font-size: 0.78rem; line-height: 1.4; }

        /* --- Grid helpers --- */
        .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
        @media (max-width: 900px) {
            .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
            header { padding: 40px 0 20px; }
            .user-pill { top: 8px; right: 12px; padding: 6px 10px; gap: 6px; }
            .user-pill .user-identity { max-width: 100px; font-size: 0.72rem; }
            .user-pill .audience-tag { display: none; }
            .nav-btn { padding: 9px 14px; font-size: 0.78rem; }
        }

        /* --- Tables --- */
        .stmx-table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.92rem; }
        .stmx-table th { background: rgba(42,245,152,0.08); color: var(--primary-green); text-align: left; padding: 12px 14px; font-weight: 700; border-bottom: 2px solid rgba(42,245,152,0.25); }
        .stmx-table td { padding: 11px 14px; color: var(--text-grey); border-bottom: 1px solid rgba(255,255,255,0.05); }
        .stmx-table tr:hover td { background: rgba(255,255,255,0.02); color: var(--text-white); }

        /* --- Badges --- */
        .badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
        .badge-green { background: rgba(42,245,152,0.15); color: var(--primary-green); border: 1px solid rgba(42,245,152,0.3); }
        .badge-blue { background: rgba(0,158,253,0.15); color: var(--secondary-blue); border: 1px solid rgba(0,158,253,0.3); }
        .badge-amber { background: rgba(251,191,36,0.12); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }

        /* --- Checklist --- */
        .checklist { list-style: none; padding: 0; margin: 0; }
        .checklist li { padding: 10px 0 10px 32px; position: relative; color: var(--text-grey); border-bottom: 1px solid rgba(255,255,255,0.04); }
        .checklist li:last-child { border-bottom: none; }
        .checklist li::before { content: '\f00c'; font-family: 'Font Awesome 6 Free'; font-weight: 900; position: absolute; left: 6px; top: 12px; color: var(--primary-green); font-size: 0.85rem; }
        .checklist li strong { color: var(--text-white); }

        /* --- Video placeholder --- */
        .video-card { background: linear-gradient(135deg, rgba(0,158,253,0.08), rgba(42,245,152,0.04)); border: 1px solid rgba(0,158,253,0.2); border-radius: 12px; padding: 20px; display: flex; gap: 16px; align-items: center; transition: var(--transition); cursor: pointer; margin-bottom: 12px; }
        .video-card:hover { border-color: var(--primary-green); transform: translateX(4px); }
        .video-thumb { width: 64px; height: 64px; border-radius: 8px; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: var(--primary-green); font-size: 1.5rem; }
        .video-meta { flex: 1; }
        .video-title { color: var(--text-white); font-weight: 600; margin-bottom: 4px; font-size: 0.98rem; }
        .video-sub { color: var(--text-grey); font-size: 0.8rem; }
    </style>
</head>
<body>

    <!-- USER PILL -->
    <div class="user-pill">
        <i class="fa-solid fa-circle-user user-icon"></i>
        <span class="user-identity">__IDENTITY__</span>
        <span class="audience-tag">__AUDIENCE__</span>
        <a href="?logout=1" class="signout-btn" onclick="
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
        "><i class="fa-solid fa-right-from-bracket"></i> Sign out</a>
    </div>

    <!-- HEADER -->
    <header>
        <div class="container">
            <div class="header-subtitle fade-up">Streamax Customer Onboarding</div>
            <h1 class="fade-up" style="font-size: 2.8rem; line-height: 1.15; margin: 0;">
                Welcome to the <span class="gradient-text">Streamax</span> family
            </h1>
            <div class="header-meta fade-up">Your guided journey — from unboxing to fleet-wide AI safety</div>
            <div class="header-meta fade-up" style="font-size: 0.75rem; opacity: 0.6;">v1.0 • For fleets &amp; TSP partners • support@streamax.com</div>
        </div>
    </header>

    <div class="container">
        <!-- NAVIGATION -->
        <nav class="nav-tabs fade-up">
            <button class="nav-btn active" onclick="switchTab('welcome', this)"><i class="fa-solid fa-hand-wave"></i> Welcome</button>
            <button class="nav-btn" onclick="switchTab('products', this)"><i class="fa-solid fa-box"></i> My Products</button>
            <button class="nav-btn" onclick="switchTab('installation', this)"><i class="fa-solid fa-screwdriver-wrench"></i> Installation</button>
            <button class="nav-btn" onclick="switchTab('training', this)"><i class="fa-solid fa-graduation-cap"></i> Training Academy</button>
            <button class="nav-btn" onclick="switchTab('ai-features', this)"><i class="fa-solid fa-robot"></i> AI Features</button>
            <button class="nav-btn" onclick="switchTab('platform', this)"><i class="fa-solid fa-chart-line"></i> Platform Tutorials</button>
            <button class="nav-btn" onclick="switchTab('playbooks', this)"><i class="fa-solid fa-book-open"></i> Playbooks</button>
            <button class="nav-btn" onclick="switchTab('support', this)"><i class="fa-solid fa-life-ring"></i> Support</button>
        </nav>
"""

html_tail = r"""
    </div>

    <script>
        function switchTab(tabId, btnElement) {
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            if (btnElement) btnElement.classList.add('active');

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

        document.addEventListener('DOMContentLoaded', () => {
            observeElements();
            if (window.lucide) lucide.createIcons();
            // Reveal initial section fade-ups
            const first = document.getElementById('welcome');
            if (first) first.querySelectorAll('.fade-up').forEach(el => el.classList.add('visible'));
        });
    </script>
</body>
</html>
"""

# Substitute identity placeholders
html_head_filled = (
    html_head
    .replace("__IDENTITY__", identity_display)
    .replace("__AUDIENCE__", audience_label)
)

full_html = (
    html_head_filled
    + welcome_content
    + products_content
    + installation_content
    + training_content
    + ai_features_content
    + platform_content
    + playbooks_content
    + support_content
    + html_tail
)

components.html(full_html, height=4200, scrolling=True)
