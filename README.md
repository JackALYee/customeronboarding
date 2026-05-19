# Streamax Customer Onboarding Portal

A guided onboarding experience for new Streamax fleet customers and TSP / channel partners. Built with Streamlit; deploys directly from this git repo to Streamlit Cloud.

## What's in it

8 sections accessible from a single-page nav:

1. **Welcome** — 30-day roadmap, day-1 checklist, key contacts
2. **My Products** — dashcam lineup, MDVR range, C29N DMS, visibility line, Z5/Sentinel asset protection
3. **Installation** — 5-step universal install, per-vehicle-type playbooks, first-boot verification, sensor gateway
4. **Training Academy** — six role-based learning paths, lesson catalogue, webinars, certifications
5. **AI Features** — SafeGPT deep-dive, Evidence Cards, ADAS/DMS event types, alert tuning, five-layer fusion
6. **Platform Tutorials** — Essential/Pro/Enterprise tiers, CMS walkthrough, mobile app, TSP API + white-label
7. **Playbooks** — first-90-days plan, coaching cadence, driver buy-in, accident workflow, industry-specific
8. **Support** — ticket / live chat / hotline, FAQ, downloads, what's new, community

Customer-facing login: email + 6-digit code (no password). When SMTP isn't configured the code is shown on-screen so dev access still works.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Configure SMTP (so login codes are emailed)

Provide credentials via one of these (checked in order):

1. **Streamlit Cloud secrets** (`.streamlit/secrets.toml` for deploy):
   ```toml
   SMTP_HOST = "mail.streamax.com"
   SMTP_PORT = "465"
   SMTP_SSL = "true"
   SMTP_USER = "noreply@streamax.com"
   SMTP_PASS = "your-app-password"
   ```
2. **Environment variables** (same keys).
3. **`env.txt`** in the project root (gitignored). Same `KEY=value` format as the sibling auto-email project.

Without SMTP the portal still works — codes are surfaced in a "DEV MODE" banner on the verify-code screen.

## Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit entry — assembles the single-page HTML and gates on auth |
| `login.py` | Email + 6-digit code login UI (two-step) |
| `db.py` | SQLite helpers (`customers`, `login_codes`) — file is `onboarding.db` |
| `emailer.py` | SMTP send for the login code email (HTML + plaintext) |
| `welcome.py` through `support.py` | The 8 section modules — each exports a `content` HTML string |

Sections share a common dark-glass design language (matches `../Sales Toolkit/salestoolkit`): `#050810` background, `#2AF598` → `#009EFD` gradient accents, Inter font, Font Awesome icons.

## Add a new section

1. Create `mysection.py` that exports `content = r"""<div id="mysection" class="content-section hidden">...</div>"""`
2. Import in `app.py` (next to the other module imports).
3. Add a `<button class="nav-btn" onclick="switchTab('mysection', this)">` to the nav block.
4. Append `+ mysection_content` to the `full_html = ...` assembly.

## Deploy

Push to GitHub. In Streamlit Cloud, point to this repo, branch `main`, main file `app.py`. Set SMTP secrets in the Streamlit Cloud dashboard.
