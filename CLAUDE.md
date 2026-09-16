# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The Streamax **Customer Onboarding Portal** — a customer-facing site that onboards new fleet
customers and TSP channel partners, plus a staff admin to manage client accounts. It is a
**static site on Cloudflare Pages + Pages Functions + Workers KV**. There is no Streamlit, no
server process and no framework (re-platformed off Streamlit on 2026-09-16; that code lives only
in git history).

- Customer portal: https://www.streamax-trucking.com/customer — 8 pages, server-side gated
- Staff admin: https://www.streamax-trucking.com/admin
- Deploy facts (IDs, domains, token scope, first-admin setup): **[HANDOFF.md](HANDOFF.md)**
- General Cloudflare procedure: [cloudflare_deploy_method.md](cloudflare_deploy_method.md)

## Layout

```
content/            section sources: each module exports `content` (one section's HTML +
                    its own <style>/<script>). welcome.py products.py installation.py
                    platform_tutorials.py ai_features.py training_academy.py playbooks.py support.py
tools/build_site.py generates site/customer/*/index.html + site/customer/search-index.json
tools/set_admin.py  owner-run: create/reset/delete admin logins (hashes locally, writes KV)
tools/preview_server.py  local visual preview (no auth, demo data) on :8790
site/               EVERYTHING PUBLISHED. Hand-written: login pages, admin, 404, _headers,
                    _redirects, robots.txt, assets/ (css, js, img, morph). Generated: customer pages.
functions/          Pages Functions (never served as files)
  _lib/auth.js      PBKDF2 hashing, HMAC session cookies, session_epoch revocation
  _lib/store.js     KV data layer (customers, admins, login events, rate limits)
  _lib/http.js      json/redirect helpers, apex->www canonicalisation
  customer/_middleware.js, admin/_middleware.js   server-side page gates
  api/_middleware.js      same-site JSON-only writes
  api/customer/{login,logout,me}.js
  api/admin/{login,logout,me,events}.js, api/admin/customers/{index,[email]}.js
deploy.sh           build -> stage ./site minus .cloudflareignore -> guard -> wrangler deploy
```

## Commands

```bash
python3 tools/build_site.py                  # regenerate customer pages (deploy.sh does this too)
python3 tools/preview_server.py              # look at it: http://localhost:8790/customer/
bash deploy.sh --dry-run                     # list exactly what would be public
bash deploy.sh --preview "msg"               # deploy to preview (own KV) - test here first
bash deploy.sh "msg"                         # production - only when the owner says so
python3 tools/set_admin.py                   # owner creates/resets an admin (prompts)
wrangler pages functions build --outdir=/tmp/fn   # compile-check functions without deploying
for f in site/assets/js/*.js; do node --check "$f"; done   # syntax-check browser JS
```

(`node --check a.js b.js` only checks the first file — the rest become script arguments.)

No test suite. Verify a change on the **preview** deployment with real sign-ins: create a random
probe admin non-interactively (`STX_ADMIN_USER`/`STX_ADMIN_PASSWORD` env + `set_admin.py
--preview`), drive the API with curl cookie jars, then delete the probes. Never type a password
into a browser tool — the local preview server needs none.

## How the customer portal is built

- `tools/build_site.py` imports each `content/*.py`, and for every section: strips the legacy
  `hidden` class, rewrites `href="javascript:void(0)" onclick="switchTab('x')"` to real links,
  promotes the first `<h2>` to the page's single `<h1 class="page-title">` (+ eyebrow), fills the
  Welcome placeholders, auto-adds `id`s to h1–h4 and item titles (`.product-name`,
  `.inst-prod-name`, `.aif-feat-name`, `.pfn-name`, `.video-title`) and emits the search index.
  It aborts on any leftover `__PLACEHOLDER__` or `javascript:void`.
- The shared shell (nav, search dialog, language dialog, prev/next pager, footer) is in
  `build_site.py`. Section list + URLs + nav labels + eyebrows + icons: the `SECTIONS` table there.
- Assets are cache-busted with `?v=<content-hash>`. The morph is referenced **extensionless**
  (`/assets/morph/truck-to-logo?v=`) because Pages 308-redirects `*.html` and would drop `?v`.
- `site/assets/js/portal.js`: `switchTab()` shim → real URLs; fills `[data-slot=identity|audience|contacts]`
  from `/api/customer/me`; search (Ctrl/⌘K, `/`); mobile menu; deep links auto-open accordions
  (`.aif-feat`, `.pfn-feat`, `.inst-prod`, `details`); Google Translate language dialog.
- **Welcome** (`content/welcome.py`): a 1620vh light band with the scroll-driven particle morph
  (iframe `site/assets/morph/truck-to-logo.html`, driven by `postMessage`; skip button; scroll
  hint), then the hero `#stmx-onboarding-start`, stats, 30-day path, the 7-section "Explore"
  grid, Day-1 checks + Key Contacts. The particles are **dark ink on white**: the canvas uses
  `NormalBlending`, because additive blending only brightens and is invisible on a light page. The morph script's hooks are `.nav-tabs`,
  `#stmx-brand-morph`, `#stmx-morph-frame`, `#stmx-onboarding-start`, `#stmx-scroll-hint` — keep them.
- The FleetMind simulator (in `platform_tutorials.py`, between `<!-- simulator -->` markers) is a
  faithful clone of a separate product with its **own** palette (`#7c5cff` etc.) — don't restyle it
  to Streamax colours; the markers also keep it out of search. It is reusable outside this repo:
  `python3 tools/export_simulator.py` writes a self-contained `docs/ft-cloud-simulator.html`;
  see [docs/ft-cloud-simulator.md](docs/ft-cloud-simulator.md).

### Adding a section
1. `content/mysection.py` exporting `content = r"""<div id="mysection" class="content-section">…"""`,
   opening with an intro `<div class="card fade-up"><h2><i class="fa-solid fa-…"></i>Title</h2><p>…</p></div>`
   (that h2 becomes the page h1).
2. Add a row to `SECTIONS` in `tools/build_site.py`; add the id → URL to `ROUTES` in `portal.js`.
3. Rebuild, preview, deploy to preview, deploy.

## Design system (ui-ux-pro-max: Minimalism & Swiss, light)

- **Official Streamax colours only**: blue `#0070C0` (5.15:1 on white — text + buttons OK),
  green `#A0C000` (2.1:1 — **decorative only, never text**; text-safe green is `--green-700 #4D6B00`).
  Neutrals are slate. One font: **Plus Jakarta Sans**. Tokens + components: `site/assets/css/stx.css`.
- `site/assets/css/portal.css` maps the legacy dark-theme names the content still uses inline
  (`--gold`→blue, `--purple`→green-700, `--text-white`→ink, `--text-grey`→ink-3, `--glass-*`→surface/line).
  Prefer the real tokens in new content; don't reintroduce light-on-dark greys (`#cbd5e1`) or
  gold/purple literals.
- Use the **real logo image** (`/assets/img/streamax-logo.png`) on light backgrounds; a white mask
  of it only on dark/blue panels. Never recolour it otherwise.
- The admin + sign-in pages share `stx.css`; the admin adds `admin.css`.
- Reveal animations are opt-in (`html.js-reveal`, set by an inline head script) with a 3 s CSS
  failsafe, so content is never stuck invisible if JS fails. Respect `prefers-reduced-motion`.
- Checked: one-line nav at 1290–1920 px (menu below 1280), no horizontal scroll at 375 px on all
  pages, 2-line hero headline, icon-only buttons have accessible names.

## Auth & data (details + rationale in HANDOFF.md)

KV keys: `customer:<email>` (JSON; list-metadata = admin table row), `admin:<username>`,
`event:<inv-ts>:<rand>` (login log, 180-day TTL, metadata-only), `rl:<scope>:<ip>`,
`config:session_key`. Sessions are HMAC cookies; every gated request re-reads the account so
disable / delete / password reset (`session_epoch`) evict immediately. No built-in test accounts.

## Content boundaries — the explicit rules

The portal is **customer-facing**. The `streamax-knowledge` skill (sibling repo
`../Sales Toolkit/auto email/.claude/skills/streamax-knowledge/`) contains both external-safe and
internal content. When authoring or editing any customer-facing section, the following are out:

- **Pricing of any kind.** No dashcam costs, no platform tier $/vehicle/mo, no TCO comparisons, no
  TSP margin economics. If commercial detail is relevant, say "talk to your CSM."
- **Internal vendor names.** Never name Webbing, Inventure, CANGO, or any other Streamax supplier.
  Earlier commits stripped these and `deploy.sh` refuses to ship them — don't reintroduce them.
- **Planning / pre-release products.** If a product isn't in `salestoolkit/terminology_db.py`
  (`TERMINOLOGY_DB`), it doesn't go in `content/products.py`. At time of writing this excludes
  DS100, C6 Lite 3.0, AD Plus 3.0, C46A AHD, CM31/CMS, ADA family, AI-AVM/360.
- **Competitive-displacement language.** "Samsara/Motive sell direct, they're a threat to TSPs"
  framing is internal sales pitch and was deliberately softened in `content/platform_tutorials.py`.
  Keep it partner-positive.
- The FleetMind dev host (`fleetmind-dev`) and its demo credentials never appear in content (guarded).

Public, white-paper-grade facts ARE in scope: Berg Insight #1 (**video telematics hardware
provider**, 6 consecutive years — say it that precisely), 5M+ vehicles, 100+ countries, 500+
channel partners, regulatory standards (London DVS, EU GSR2, UN R46), industry-statistic costs like
the mining "$500K–$2M per crusher incident" line, SafeGPT capability descriptions. Source for company
numbers: the skill's `reference/company-snapshot.md` — quote it, don't paraphrase it upward.

## Where product data comes from

`content/products.py` holds a **static snapshot** of 26 products + 48 Drive download URLs, copied
from `../Sales Toolkit/salestoolkit/terminology_db.py` (`TERMINOLOGY_DB`). The shape is
`PRODUCTS_BY_GROUP` — groups, each with `items` of `name`, `desc` and `(label, url)` `files`.

The snapshot does NOT auto-update: when Streamaxpedia adds a product, changes a Drive link or
moves a model from planning to shipping, update `PRODUCTS_BY_GROUP`. Because the build now runs
locally, a build-time import from the sibling repo inside `tools/build_site.py` is feasible (only
the built HTML is uploaded) — that's the path if a live sync is ever requested. The upload
placeholder at the top of My Products is meant to eventually take a parsed invoice and show the
same registry filtered to the matched items (would need a Pages Function).

The Drive links are real PDFs: `curl -sL "<uc?export=download&id=…>" -o /tmp/x.pdf`, then Read
with the `pages` param. That's how the AD Plus 2.0 install flow (the basis for the dashcam guides)
was grounded.

## Pitfalls

- **`deploy.sh` only publishes `./site`.** New public files go there; source stays out.
- **wrangler never reads `.cloudflareignore`.** `deploy.sh` enforces it by staging with rsync —
  don't "simplify" it to `wrangler pages deploy site`. `--dry-run` shows what really ships.
- **Generated pages are overwritten** on every build — edit `content/*.py` or `build_site.py`, never
  `site/customer/*/index.html`.
- **KV is eventually consistent (~60 s)** — a new client may not sign in from far away for a minute;
  `list()` lags too. Don't "fix" by retrying in a loop.
- **A CSS `display` rule overrides the `hidden` attribute** — add `.x[hidden]{display:none!important}`.
- **The in-app Browser pane blocks subresources on external domains** and backgrounded tabs freeze
  transitions, so screenshots of production can look unstyled/faded. Verify production with curl;
  verify visuals on `tools/preview_server.py`.
- **After a deploy the edge can lag a few seconds** (one-off 522s were seen) — retry before concluding.
- **Workers' Web Crypto caps PBKDF2 at 100,000 iterations** — keep hashes at or below it.
- **Old deployments keep running their old Functions against the production KV** at their hash URLs
  (`<id>.streamax-onboarding.pages.dev`). An auth fix isn't complete until the production deployments
  that predate it are deleted (owner's OK; see HANDOFF.md known limits).
- **The nav holds exactly 8 sections on one line down to 1290 px** (measured). A 9th item needs the
  breakpoints in `portal.css` (1360 icon-only search, 1280 menu) re-measured, not guessed.
- **Video placeholders stay dark** (`#0B1220` + blue glow) on the light theme on purpose — they
  read as video frames. Same for the Welcome morph band and the FleetMind simulator.
- **The mascot and logo are plain files** in `site/assets/img/` now (the Streamlit-era base64
  data-URI workaround is gone) — reference them root-absolute (`/assets/img/…`).

## Sibling repos

- `../Sales Toolkit/salestoolkit/` — internal sales toolkit; `terminology_db.py` is the product-data upstream.
- `../Sales Toolkit/auto email/` — Streamax cold-email agent; holds the shared `streamax-knowledge` skill.
- `../SMB_Website/` — FleetSpring site; the reference implementation of the Cloudflare method.
- `../3D Files/` — source 3D models (`semi.glb` was baked into the morph's particle buffer offline).
