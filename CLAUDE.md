# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A customer-facing Streamlit app that onboards new Streamax fleet customers and TSP channel partners. Deploys directly to Streamlit Cloud from this repo (no build step). The whole portal is a single page rendered as one HTML document via `streamlit.components.v1.html`, with section navigation handled in browser JS — Streamlit only does the auth gate and role routing.

## Run / verify

```bash
pip install -r requirements.txt
streamlit run app.py

# Compile-check after any edit
python3 -m py_compile app.py login.py db.py staff.py welcome.py products.py installation.py training_academy.py ai_features.py platform_tutorials.py playbooks.py support.py

# Smoke pattern used throughout development
rm -f onboarding.db && (streamlit run app.py --server.headless true --server.port 8765 --browser.gatherUsageStats false > /tmp/sm.log 2>&1 &) \
  && sleep 5 && curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8765/ \
  && pkill -f "streamlit run app.py"
```

No test suite. Validate logic changes with an in-process smoke script that monkey-patches `streamlit` (see commits — every code-change commit was preceded by one).

## Test accounts (built-in, hardcoded in [login.py](login.py))

- `test` / `testme` → logs in as the seeded test client (`test@onboarding.local`, audience: fleet)
- `test_staff` / `testme` → opens the staff dashboard
- Any real client → email + password assigned by staff via the create-account form

The two `test*` usernames are recognised before the email-lookup path. Don't break that ordering.

## Architecture — the load-bearing pattern

**[app.py](app.py) is a thin shell.** It:
1. Renders Streamlit page config + a minimal CSS override (just so the Streamlit chrome around the `components.html` iframe stays dark).
2. Gates on `st.session_state['authenticated']`. Unauthenticated → `login.render_login()` and stop.
3. Routes by `user_role`: `staff` → `staff.render()` (a normal Streamlit page); `customer` → assembles the single-page portal and renders it via one `components.html(full_html, height=4200, scrolling=True)` call.

**The 8 customer-facing sections are pure-HTML modules.** Each (`welcome.py`, `products.py`, `installation.py`, `training_academy.py`, `ai_features.py`, `platform_tutorials.py`, `playbooks.py`, `support.py`) exports a single module-level string named `content` shaped like:

```python
content = r"""
<div id="welcome" class="content-section">   <!-- or "content-section hidden" for non-default -->
   ...inline HTML using the shared CSS classes from app.py...
</div>
"""
```

`app.py` concatenates `html_head + welcome_content + products_content + ... + html_tail`. The `<head>` block in `app.py` defines all shared CSS variables, glass-panel/card/CTA styles, and the `switchTab(tabId, this)` JS that hides/shows sections by toggling the `hidden` class. **Section switching is JS-only — there is no Streamlit rerun between tabs.** This is why every section ships its data inline and why you can't use Streamlit widgets inside a section's HTML.

If you need a real Streamlit widget inside a customer-facing section, either (a) render it above/below the `components.html` block and accept that it'll appear outside the styled container, or (b) keep it as a pure HTML placeholder and wire it to a backend later (this is what the proforma-invoice uploader at the top of [products.py](products.py) does).

**Section HTML expects these CSS classes/variables** (all defined in `app.py`'s `<style>`): `--primary-green` `#2AF598`, `--secondary-blue` `#009EFD`, `--bg-deep` `#050810`, `.card`, `.glass-panel`, `.section-header`, `.grid-2 / .grid-3 / .grid-4`, `.stmx-table`, `.badge-green / .badge-blue / .badge-amber`, `.checklist`, `.pipeline-container / .pipeline-step / .pipeline-icon`, `.cta-btn` (+ `.secondary`), `.fade-up`, `.gradient-text`, `.video-card`. Re-use them; don't redefine.

The staff dashboard is the exception — it renders as a normal Streamlit page (not inside `components.html`) and has its own CSS injected in [staff.py](staff.py).

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

1. Create `mysection.py` exporting `content = r"""<div id="mysection" class="content-section hidden">...</div>"""` (use `hidden` on every section except `welcome`, which is the default).
2. Import it in `app.py` next to the other section imports (the existing imports use try/except + fallback HTML so a missing section degrades gracefully; match that style).
3. Add `<button class="nav-btn" onclick="switchTab('mysection', this)">` to the nav block in `app.py`.
4. Append the content to the `full_html = ...` assembly.
5. If the new section is tall, bump the `height=4200` argument on `components.html`. The iframe doesn't auto-size to its content.

## Common pitfalls

- **Don't use `st.something` inside a section module.** It looks like it'd work, but the section's `content` is a string concatenated into one HTML doc rendered inside an iframe. No Streamlit context.
- **The `?logout=1` query param** is the only way to log out — both pills use a JS snippet that rewrites `window.parent.location` so the parent Streamlit page (not the iframe) navigates. Don't simplify that without testing it inside an iframe.
- **Sign-out clears `audience` too.** Anything saved per-session under `st.session_state` needs to be in the `_clear_pending` / logout key list, or it'll leak between users on the same tab.
- **Don't reintroduce `emailer.py` or the `login_codes` table** unless email-based auth is explicitly being added back. The schema migration would handle a re-add; the bigger trap is half-restoring it and leaving dead code in `login.py`.

## Sibling repos (relevant context)

- `../Sales Toolkit/salestoolkit/` — the internal sales toolkit. Its `terminology_db.py` is this portal's product-data upstream; its `app.py` / section-module pattern is the design language this portal mirrors.
- `../Sales Toolkit/auto email/` — the Streamax cold-email agent. Shares the same `streamax-knowledge` skill in its `.claude/skills/` directory (where to look up product specs, SafeGPT mechanics, value-propositions when authoring sections).
