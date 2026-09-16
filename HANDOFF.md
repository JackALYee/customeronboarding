# HANDOFF — Streamax Customer Onboarding on Cloudflare

Live since 2026-09-16. Deployed with `cloudflare_deploy_method.md` (Pages, direct upload).
This file holds this site's own facts; the method file holds the general procedure.

## Where it lives

| What | Value |
|---|---|
| Customer portal | https://www.streamax-trucking.com/customer (sign-in at `/customer/login/`) |
| Staff admin | https://www.streamax-trucking.com/admin (sign-in at `/admin/login/`) |
| Bare domain `/` | 302 → https://www.streamax.com (temporary, in `site/_redirects`; replace when the root gets its own page) |
| Apex `streamax-trucking.com` | attached to the project; `/customer*` and `/admin*` 301 → `www` (done in the page middlewares, `functions/_lib/http.js`) |
| Cloudflare account | `b377955e9eb4b1916473ebafa6ec2859` |
| Pages project | `streamax-onboarding` → `streamax-onboarding.pages.dev`, production branch `main` |
| Preview | `bash deploy.sh --preview "msg"` → https://preview.streamax-onboarding.pages.dev (separate KV) |
| Zone | `streamax-trucking.com` → `955c3863a05ba4c046cd9c6001f73746` |
| DNS | `www` and apex: proxied CNAME → `streamax-onboarding.pages.dev` (don't delete by hand; detach the domain instead) |
| KV (binding `KV`) | production `68a3a091d90141c4808ee2e6d412875f`, preview `097063aa5cb94f24bee00b34df84a190` |
| IDs in code | `cloudflare.json` (read by `tools/set_admin.py`), `deploy.sh` (account + project) |

## Token (`~/.cloudflare_token`) — what it can and can't do (verified 2026-09-16)

- ✅ Pages Edit · DNS Edit (streamax-trucking.com) · Workers KV Storage Edit
- ❌ D1 (why storage is KV, not D1) · Rulesets / Single Redirect (why apex→www is in Functions)
- ❔ Cache Purge — untested

## Your admin login

Admin `jack` exists with a **temporary** password, alongside a demo client
`demo@streamax-trucking.com` — both are in the git-ignored `credentials.md` (never committed, never
published). Replace the admin password with your own: same command, same username.

```bash
python3 tools/set_admin.py
```

It prompts for a username and a hidden password, hashes it locally and writes only the hash to KV.
Reusing a username resets that password and signs that admin out everywhere; `--list`,
`--delete NAME` and `--preview` also exist. Create client accounts from `/admin`.

There are **no built-in test accounts** (the old `test`/`testme` would be a public backdoor on a
real domain). The demo client is an ordinary account — delete or rename it whenever you like.

## Deploy

```bash
bash deploy.sh --dry-run                 # builds, then lists every file that would be public
bash deploy.sh --preview "what changed"  # test on preview first (its own KV)
bash deploy.sh "what changed"            # production
```

`deploy.sh` runs `tools/build_site.py` first (the 8 customer pages are generated from
`content/*.py`), stages ONLY `./site` minus `.cloudflareignore`, refuses to ship internal files
or guard words (`webbing`, `inventure`, `cango`, `fleetmind-dev`), and compiles `./functions`.

## Verify where it lands (method §4)

```bash
SITE=https://www.streamax-trucking.com
for p in / /customer/ /customer/login/ /admin/ /admin/login/ /api/customer/me /nope; do printf '%-18s %s\n' "$p" "$(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' "$SITE$p")"; done
```

Expected: `/` 302 streamax.com · `/customer/` 302 login · logins 200 · `/admin/` 302 login ·
API 401 · `/nope` 404. For a signed-in check, the pattern used on 2026-09-16 (random probe admin
via `STX_ADMIN_USER`/`STX_ADMIN_PASSWORD` env → create client via API → log in → fetch pages →
delete both) is in the session transcript; always delete probes afterwards.

## Security model (read before changing auth)

- Pages under `/customer/*` and `/admin/*` are gated **server-side** by `functions/*/_middleware.js`;
  gated HTML (and `/customer/search-index.json`) is never served to anonymous visitors, and is
  `Cache-Control: private, no-store`.
- Passwords: PBKDF2-SHA256, 100k iterations (Workers' Web Crypto maximum), format
  `pbkdf2_sha256$iter$salt$hash` — the same in `functions/_lib/auth.js` and `tools/set_admin.py`.
- Sessions: HMAC-signed cookies (`stx_session` 7 d, `stx_admin` 12 h), HttpOnly/Secure/SameSite=Lax,
  key in KV `config:session_key`. **Delete that key to sign everyone out** (it is recreated).
- Every page view re-reads the account: turning a client's access off, deleting it, or resetting
  its password (`session_epoch`) ends existing sessions immediately — not at cookie expiry.
- Writes to `/api/*` must be same-site JSON (`functions/api/_middleware.js`); failed logins are
  rate-limited per IP (10 / 15 min, best effort).

## Known limits

- **KV is eventually consistent (~60 s).** A brand-new client can take up to a minute to sign in
  from a far-away region; the admin list can lag the same way (the admin UI updates locally).
- KV free tier: 1,000 writes/day. A sign-in costs 2 writes, a failed one 1. Fine at this scale;
  bookkeeping writes are best effort, so a spent quota never blocks a valid sign-in.
- Google Fonts and Google Translate (language menu) don't load in mainland China; the portal
  falls back to system fonts and English. The morph's three.js races cdnjs vs npmmirror and falls
  back to a static logo if both fail.
- **Old deployments stay live at their hash URLs (method §7) and keep running their own Functions
  against the production KV.** The Phase 1 deployment `cdbae860` predated `session_epoch` — a probe
  showed a cookie issued before a password reset still worked there — so it was **deleted on
  2026-09-16** (host now 404s). Every remaining deployment post-dates the fix. Rule for the future:
  after any auth fix, delete the production deployments that predate it.

## Checklist (method §10)

- [x] Token permissions verified; account + zone IDs recorded (above)
- [x] Pages project `streamax-onboarding`, production branch `main`
- [x] `deploy.sh` + `.cloudflareignore`, project/account/guard words set
- [x] Dry run read; preview + production deployed; `pages.dev` checked
- [x] `www` + apex attached and active; apex → www (Functions) for `/customer`, `/admin`
- [x] `404.html` (root-absolute paths); `_redirects` for `/`; `robots.txt` disallows all (private portal)
- [x] Section 4 checks pass on the custom domain (2026-09-16)
- [x] First admin created 2026-09-16 (`jack`) with a **temporary** password, plus a demo client
      `demo@streamax-trucking.com` — both recorded in the git-ignored `credentials.md`; owner should
      reset the admin password with `python3 tools/set_admin.py`
- [x] Deleted deployment `cdbae860` (pre-revocation auth code) on 2026-09-16, owner approved
- [ ] After the re-platform commit is pushed: delete the old Streamlit Community Cloud app (it
      deployed from `main`/`app.py`, which no longer exists, so its next build fails)
