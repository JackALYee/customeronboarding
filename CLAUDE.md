# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A customer-facing Streamlit app that onboards new Streamax fleet customers and TSP channel partners. Deploys directly to Streamlit Cloud from this repo (no build step). The whole portal is a single page rendered as one HTML document via `streamlit.components.v1.html`, with section navigation handled in browser JS — Streamlit only does the auth gate and role routing.

## Run / verify

```bash
pip install -r requirements.txt   # streamlit + extra-streamlit-components
streamlit run app.py

# Compile-check after any edit (all modules)
python3 -m py_compile app.py login.py db.py staff.py auth_cookie.py assets.py \
  welcome.py products.py installation.py training_academy.py ai_features.py \
  platform_tutorials.py playbooks.py support.py documentations.py

# Relaunch pattern — ALWAYS free the port first (see pitfalls: stale instances stick around)
lsof -ti :8501 | xargs kill -9 2>/dev/null; pkill -9 -f "streamlit run app.py"; sleep 2
streamlit run app.py --server.port 8501 --browser.gatherUsageStats false &
sleep 7 && curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8501/
```

No test suite. Validate logic changes with an in-process smoke script that monkey-patches `streamlit` before importing a module (`sys.modules['streamlit'] = MagicMock()`), then asserts on the produced `content` string / db behavior — every code-change commit in the history was preceded by one.

The Python that has Streamlit installed is `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3` — plain `python3` lacks it (fine for `py_compile`, not for importing app modules).

## Test accounts (built-in, hardcoded in [login.py](login.py))

- `test` / `testme` → logs in as the seeded test client (`test@onboarding.local`, audience: fleet)
- `test_staff` / `testme` → opens the staff dashboard
- Any real client → email + password assigned by staff via the create-account form

The two `test*` usernames are recognised before the email-lookup path. Don't break that ordering.

## Architecture — the load-bearing pattern

**[app.py](app.py) is a thin shell.** It:
1. Renders Streamlit page config + a minimal CSS override (just so the Streamlit chrome around the `components.html` iframe stays dark).
2. Gates on `st.session_state['authenticated']`. Unauthenticated → `login.render_login()` and stop.
3. Routes by `user_role`: `staff` → `staff.render()` (a normal Streamlit page); `customer` → assembles the single-page portal and renders it via one `components.html(full_html, height=1000, scrolling=True)` call. The `height` is a fallback — customer-portal-only CSS forces the iframe to `100vh` so it becomes the scroll container (see the iframe note below).

**The 8 customer-facing sections are HTML modules.** Nav order (in `app.py`): **Welcome · My Products · Installation · Platform Tutorials · AI Features · Training Academy · Playbooks · Support**. Each module (`welcome.py`, `products.py`, `installation.py`, `platform_tutorials.py`, `ai_features.py`, `training_academy.py`, `playbooks.py`, `support.py`) exports a module-level string `content` shaped like:

```python
content = r"""
<div id="welcome" class="content-section">   <!-- or "content-section hidden" for non-default -->
   ...inline HTML using the shared CSS classes from app.py...
</div>
"""
```

`app.py` concatenates `html_head + welcome_content + products_content + ... + html_tail`. The `<head>` block in `app.py` defines all shared CSS variables, glass-panel/card/CTA styles, and the `switchTab(tabId, this)` JS that hides/shows sections by toggling the `hidden` class. **Section switching is JS-only — there is no Streamlit rerun between tabs.** This is why every section ships its data inline and you can't use Streamlit widgets inside a section's HTML.

**Sections CAN include their own `<style>` and `<script>`** — everything is inside one `components.html` iframe, which executes scripts and has no `st.markdown` blank-line constraint. Several sections are full interactive sub-apps built this way (Python builds the HTML from a data table, then a scoped `<script>` wires up the interactivity, guarded by `root.dataset.*Init`):
- **[platform_tutorials.py](platform_tutorials.py)** — a clone of the FleetMind platform (the customer's white-label Streamax CMS): three top-bar rails (Vision / Subscription / Settings), accordion sidebar submenus, ~22 views, top-bar overlays (AI agent / notifications / help / account), and hover-tooltip explanations. Built from `GROUPS` + per-view builder functions; light-themed `.fm-*` styles scoped so the portal's dark theme doesn't leak.
- **[installation.py](installation.py)** — per-product accordions (grouped like products.py), each with a video placeholder + step-through guide (tick steps, progress bar) + checklist. Data in `GROUPS` + `GUIDES`; real guides where grounded in spec sheets, `placeholder` key where not (B2/B3/R-Watch/Sentinel).
- **[ai_features.py](ai_features.py)** — per-detection accordions (`_ADAS` + `_DMS` tables): each detection has a description, a sample-clip placeholder, and a parameter-config table. AEB config is a placeholder (safety-critical, not user-tunable).

If you need a real Streamlit *widget* inside a customer-facing section, either (a) render it above/below the `components.html` block (it'll sit outside the styled container), or (b) keep it as a pure HTML placeholder and wire it to a backend later (e.g. the proforma-invoice uploader atop [products.py](products.py)).

[documentations.py](documentations.py) exists on disk but is **orphaned** — it was added then removed from the nav/assembly; it's not imported. Re-wire it in `app.py` if you want it back.

**Palette is golden + purple glassmorphism** on a plum-dark base: `--gold` `#F4C95D`, `--purple` `#A06BFF`, gradient `gold → purple`, `--bg-deep` `#0c0a14`. (It was green/blue originally — recolored app-wide; don't reintroduce `#2AF598`/`#009EFD`.)

**Section HTML expects these CSS classes/variables** (all defined in `app.py`'s `<style>`): `--gold`, `--purple`, `--bg-deep`, `.card`, `.glass-panel`, `.section-header`, `.grid-2 / .grid-3 / .grid-4`, `.stmx-table`, `.badge-green / .badge-blue / .badge-amber`, `.checklist`, `.pipeline-container / .pipeline-step / .pipeline-icon`, `.cta-btn` (+ `.secondary`), `.fade-up`, `.gradient-text`, `.video-card`. Re-use them; don't redefine.

The staff dashboard is the exception — it renders as a normal Streamlit page (not inside `components.html`), with a fixed glass top bar, sticky tabs, and a `<details>` user dropdown (Language + Sign out); its CSS is injected in [staff.py](staff.py). A `<style>` injected via `st.markdown` must be ONE contiguous block — a blank line inside it ends the HTML passthrough and the rest leaks to the page as text.

**Session persistence + language** ([auth_cookie.py](auth_cookie.py)): a signed cookie (via `extra-streamlit-components`) carries auth across reloads so a `?lang=` switch or refresh doesn't log you out; a sticky `LOGOUT_FLAG` defeats the cookie-restore-race on sign-out. The customer portal translates in-iframe (its own Google-Translate modal); the staff page translates the parent doc via a 0-height `components.html` bridge, and defaults to English with NO engine loaded (and clears the shared `googtrans` cookie) so a customer-side language choice can't bleed in.

**The full-height-iframe CSS is customer-portal-only** — it's injected right before the portal's `components.html` and scoped to `[data-testid="stIFrame"]`, NOT in the global block. A global `.stApp iframe { height: 100vh }` would also blow up the hidden cookie-manager iframe on the login/staff pages.

## Authentication & DB ([db.py](db.py) + [login.py](login.py))

- SQLite at `onboarding.db` (gitignored). Two tables: `customers`, `login_events`.
- `init_db()` runs every import of `login.py`; it includes idempotent migrations that `ALTER TABLE` to add columns introduced after the schema first shipped (`password_hash`, `created_at`, `created_by`). Preserve those — older deploys still have older sqlite files.
- `seed_test_accounts()` also runs on every `login.py` import. It inserts the test client row + sets its password hash if missing. Don't move this into a one-shot script.
- Passwords use `pbkdf2_sha256$120000$<salt_hex>$<hash_hex>` via stdlib `hashlib.pbkdf2_hmac` + `hmac.compare_digest`. No bcrypt/argon2 dependency on purpose (keeps `requirements.txt` to one line: Streamlit). Don't swap algorithms without reading existing hashes first.
- `staff` is currently a hardcoded `test_staff`/`testme` credential check. There is no `staff` table — when real staff auth is needed, add one rather than expanding the hardcoded check.

## Content boundaries — the explicit rules

The portal is **customer-facing**. The auto-memory's `streamax-knowledge` skill contains both external-safe and internal content. When authoring or editing any customer-facing section, the following are out:

- **Pricing of any kind.** No dashcam costs ($90/$200/etc.), no platform tier $/vehicle/mo ($1/$3/$6), no TCO comparisons, no TSP margin economics. If commercial detail is relevant, say "talk to your CSM."
- **Internal vendor names.** Never name Webbing, Inventure, CANGO, or any other Streamax supplier. Earlier commits have already stripped these — don't reintroduce them.
- **Planning / pre-release products.** If a product isn't in `salestoolkit/terminology_db.py` (`TERMINOLOGY_DB`), it doesn't go in [products.py](products.py). At time of writing this excludes DS100, C6 Lite 3.0, AD Plus 3.0, C46A AHD, CM31/CMS, ADA family, AI-AVM/360.
- **Competitive-displacement language.** "Samsara/Motive sell direct, they're a threat to TSPs" framing is internal sales pitch and was deliberately softened in [platform_tutorials.py](platform_tutorials.py). Keep it partner-positive.

Public, white-paper-grade facts ARE in scope: Berg Insight #1, 5M+ vehicles, 100+ countries, regulatory standards (London DVS, EU GSR2, UN R46), industry-statistic costs like the mining "$500K–$2M per crusher incident" line, SafeGPT capability descriptions.

## Where product data comes from

[products.py](products.py) holds a **static snapshot** of 26 products + 48 Drive download URLs, copied from the sibling repo at `../Sales Toolkit/salestoolkit/terminology_db.py` (the `TERMINOLOGY_DB` list). The shape is `PRODUCTS_BY_GROUP` — a list of groups, each with `items` containing `name`, `desc`, and a list of `(label, url)` `files`.

The snapshot does NOT auto-update. If Streamaxpedia adds a product, changes a Drive link, or moves a model from planning to shipping, somebody has to update `PRODUCTS_BY_GROUP`. The product registry shape is deliberately friendly to future invoice-parsing — the upload placeholder at the top of the section is meant to eventually post a parsed product list and re-render the same registry filtered to the matched items.

If a refactor to import directly from `salestoolkit/terminology_db.py` at runtime is requested, both repos would need to co-deploy (Streamlit Cloud cannot follow `../`), so a build-time sync script is the more realistic path.

## Adding a new section

1. Create `mysection.py` exporting `content = r"""<div id="mysection" class="content-section hidden">...</div>"""` (use `hidden` on every section except `welcome`, the default).
2. Import it in `app.py` next to the other section imports (try/except + fallback HTML so a missing section degrades gracefully; match that style).
3. Add `<button class="nav-btn" data-tab="mysection" onclick="switchTab('mysection', this)">` to the `.nav-links` block. The `data-tab` is load-bearing — `switchTab` highlights the active button by `data-tab` when no element is passed (so CTAs elsewhere can call `switchTab('mysection')` without a fragile nav-index). Don't select nav buttons by index.
4. Append `+ mysection_content` to the `full_html = ...` assembly.
5. The iframe is forced to `100vh` (it scrolls internally), so you don't need to grow `height` for tall sections — but keep `scrolling=True`.

## Common pitfalls

- **Don't use `st.something` inside a section module.** It looks like it'd work, but the section's `content` is a string concatenated into one HTML doc rendered inside an iframe. No Streamlit context.
- **The `?logout=1` query param** is the only way to log out — both pills use a JS snippet that rewrites `window.parent.location` so the parent Streamlit page (not the iframe) navigates. Don't simplify that without testing it inside an iframe.
- **Sign-out clears `audience` too.** Anything saved per-session under `st.session_state` needs to be in the `_clear_pending` / logout key list, or it'll leak between users on the same tab.
- **Don't reintroduce `emailer.py` or the `login_codes` table** unless email-based auth is explicitly being added back. The schema migration would handle a re-add; the bigger trap is half-restoring it and leaving dead code in `login.py`.
- **Stale Streamlit instances hold port 8501.** A backgrounded `streamlit run app.py` survives across turns; a new launch then prints "Port 8501 is already in use" and exits, while `curl localhost:8501` still returns 200 from the *old* code — so you think your change shipped when it didn't. Always `lsof -ti :8501 | xargs kill -9; pkill -9 -f "streamlit run app.py"; sleep 2` before relaunching, and confirm the port is free.
- **A CSS `display` rule overrides the `hidden` attribute.** The FleetMind overlay panels broke because `.fm-notifs { display:flex }` kept them visible even with `hidden` set. When you toggle via `hidden`, add `.thing[hidden] { display:none !important; }`.
- **Reading a spec sheet:** the Drive links in `products.py` are real PDFs. `curl -sL "<uc?export=download&id=...>" -o /tmp/x.pdf`, then Read with the `pages` param. That's how the AD Plus 2.0 install flow (the basis for the dashcam guides) was grounded.
- **The mascot is a base64 data URI**, not a Drive hot-link — Drive blocks `<img>` embedding. `assets.py` reads `assets/mascot.png` and exposes `MASCOT_DATA_URI`; app.py / login.py fill a `__MASCOT_SRC__` placeholder. Keep `assets/mascot.png` committed.

## Sibling repos (relevant context)

- `../Sales Toolkit/salestoolkit/` — the internal sales toolkit. Its `terminology_db.py` is this portal's product-data upstream; its `app.py` / section-module pattern is the design language this portal mirrors.
- `../Sales Toolkit/auto email/` — the Streamax cold-email agent. Shares the same `streamax-knowledge` skill in its `.claude/skills/` directory (where to look up product specs, SafeGPT mechanics, value-propositions when authoring sections).
