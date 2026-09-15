# Deploying a local website to Cloudflare Pages through the API

> **A reusable method.** Consolidated 2026-09-16 from the FleetSpring site (fleetspring.net),
> where every step below was run and verified on 2026-09-15. The tested reference implementation
> lives in `/Users/jiachenyi/Desktop/Streamax/SMB_Website/` (`deploy.sh`, `.cloudflareignore`,
> `functions/`, and `HANDOFF.md` § 9).
>
> **To use it in another session:** "Read
> `/Users/jiachenyi/Desktop/Streamax/SMB_Website/cloudflare_deploy_method.md` and put this site on
> Cloudflare with it." Keep each site's own facts (account ID, project name, zone ID, domains) in
> that project's `HANDOFF.md` or `CLAUDE.md`, not here.

## 0. What this is, and when to use it

A static site — HTML, CSS, JavaScript, images — plus, optionally, a small backend (Pages
Functions), published by **direct upload** from the local folder with `wrangler` and an API token.
No Git integration and no build step are needed. You get: a `<project>.pages.dev` URL, your own
domain with HTTPS, a public hash URL per deployment (instant rollback), preview deployments with
separate settings, and server code in `functions/`.

| Route | Use it when | Deploy command |
|---|---|---|
| **Pages, direct upload** (this method) | A folder of pages, maybe a few API endpoints, `_redirects` and `404.html` handled by the platform | `bash deploy.sh` → `wrangler pages deploy <staging-dir>` |
| Workers with static assets | The site is mostly a Worker, or you already have a `wrangler.jsonc` | `npx wrangler deploy` beside `wrangler.jsonc` |

The Smart City site (elitesemicon-smartcity.com) uses the Workers route; its project memory has
that command. Everything below is the Pages route.

## 1. Once per machine

1. **wrangler:** `brew install cloudflare-wrangler` (or `npm install -g wrangler`), then
   `wrangler --version`. Tested with 4.90.1.
2. **An API token — the owner creates it.** dash.cloudflare.com → My Profile → API Tokens → Create
   Token → Custom token:

   | Permission | Scope | Why | |
   |---|---|---|---|
   | Account → Cloudflare Pages → Edit | the account | create projects, deploy, domains, variables, deployments | required |
   | Zone → DNS → Edit | the site's zone | custom-domain CNAMEs, TXT records | required for a custom domain |
   | Zone → Cache Purge → Purge | the site's zone | evict stale copies of removed files (section 8) | strongly recommended |
   | Zone → Single Redirect → Edit | the site's zone | the www → apex rule (section 2.5) | optional |
   | Zone → Zone Settings → Edit | the site's zone | settings such as Always Use HTTPS | optional |

   A missing permission shows up as `{"code":10000,"message":"Authentication error"}`.
3. **Store it outside every project**, readable only by you — the owner runs this, not Claude:
   ```bash
   echo 'PASTE_TOKEN_HERE' > ~/.cloudflare_token && chmod 600 ~/.cloudflare_token
   ```
4. **Check it and look up the IDs** (read-only; the helper `cf` is defined in section 9):
   ```bash
   cf "$API/user/tokens/verify"            # "status": "active"
   cf "$API/accounts"                      # → account ID
   cf "$API/zones?name=example.com"        # → zone ID (the zone must already be on Cloudflare)
   ```

**Rules for Claude with keys:** never ask for a token or secret in chat, never type one into a
file or a command, never print one. Read the token only inside a command, as
`"$(cat ~/.cloudflare_token)"`. Secrets for the site (section 5) are entered by the owner.

## 2. Once per site

### 2.1 Create the Pages project

```bash
CLOUDFLARE_API_TOKEN="$(cat ~/.cloudflare_token)" wrangler pages project create my-site --production-branch=main
# or: cf -X POST "$API/accounts/$A/pages/projects" --data '{"name":"my-site","production_branch":"main"}'
```

Create it explicitly: `wrangler pages deploy` to a project that does not exist stops and asks, and
an unattended session cannot answer.

### 2.2 Add the two files that make deploys safe

Copy **`deploy.sh`** (Appendix A) and **`.cloudflareignore`** (Appendix B) into the site's root. In
`deploy.sh`, set `PROJECT_NAME`, `ACCOUNT_ID` and, if some words must never be published (a parent
brand, client names, internal code names), `GUARD_WORDS=("word one" "word two")`.

Why a script at all: **wrangler does not read `.cloudflareignore`** — it skips only `.DS_Store`,
`.git` and `node_modules`. Running `wrangler pages deploy .` publishes everything else in the
folder, internal notes included. `deploy.sh` copies the folder minus the ignore list into a
staging folder, refuses to continue if an internal file or a guarded word is still in it, and
deploys that folder.

### 2.3 First deploy

```bash
bash deploy.sh --dry-run          # read the list: every file here becomes public
bash deploy.sh "First deploy"
```

The output ends with the deployment's own URL (`https://<hash>.my-site.pages.dev`); the site is
also at `https://my-site.pages.dev`.

### 2.4 Your own domain

When the zone is on Cloudflare in the same account:

```bash
cf -X POST "$API/accounts/$A/pages/projects/$P/domains" --data '{"name":"example.com"}'
cf -X POST "$API/accounts/$A/pages/projects/$P/domains" --data '{"name":"www.example.com"}'
cf "$API/zones/$Z/dns_records?type=CNAME"                    # expect proxied CNAMEs → my-site.pages.dev
cf "$API/accounts/$A/pages/projects/$P/domains/example.com"  # repeat until "status": "active"
```

If a CNAME to `my-site.pages.dev` is missing, create it proxied (section 9). Once the domain is
attached, never delete its DNS record by hand; detach the domain from the project instead. For a
zone hosted elsewhere, only subdomains work: add the CNAME at that DNS provider. An apex domain
needs the zone on Cloudflare.

### 2.5 One address: www → apex

Otherwise `www` serves a duplicate of the site. Create a redirect rule — in the dashboard (the
domain → Rules → Redirect Rules), or through the API as in section 9. Keep the path and query string,
and use status 301.

### 2.6 Files Pages treats specially

- **`404.html`** in the root: unknown URLs get it with a real **404** status. Without it, Pages
  answers every unknown URL with the homepage and **200** — a "soft 404" that search engines
  penalize. It can be served at any depth, so every path in it must be root-absolute (`/css/…`).
- **`_redirects`**: `<from> <to> <status>` per line, `#` comments, splats (`/old/* /new/:splat 301`).
  It is evaluated **before** static files are looked up, and it is not served as a file itself.
- **`_headers`** (optional): extra response headers per path.
- **Extensionless URLs:** Pages answers `page.html` with a 308 redirect to `/page`. Write canonical
  links, `og:url`, JSON-LD and `sitemap.xml` in the extensionless form (`https://example.com/page`)
  so that none of them is a redirect.

### 2.7 Optional extras

- Search Console: add the verification TXT record through the DNS API (section 9).
- Email for the domain: Cloudflare Email Routing (dashboard → the domain → Email) forwards
  `hello@…` to an inbox. It receives mail only; sending needs a provider.
- DMARC: a TXT record `_dmarc` with `v=DMARC1; p=none; rua=mailto:…`.

## 3. Every change: the deploy loop

1. `bash deploy.sh --dry-run` — read the list; count and names should be what you expect.
2. Run the project's own checks (links, content rules).
3. `bash deploy.sh "what changed"` — **only when the owner says so.** Show the dry-run summary
   first. A standing "deploy after each change" is valid only for the session it was given in.
4. Verify it where it lands (section 4).

## 4. Verify where it lands

A green "Deployment complete!" is not proof, and neither is an API "success". Check the public result:

```bash
SITE=https://example.com
for p in / /about /contact /no-such-page; do printf '%-16s %s\n' "$p" "$(curl -s -o /dev/null -w '%{http_code}' "$SITE$p")"; done
curl -sI "$SITE/old-path" | grep -i '^location'          # a redirect from _redirects
curl -s  "$SITE/REMOVED-FILE.md" | head -c 80            # something you removed — see section 8
```

- **Check the custom domain itself**, not only `pages.dev`: they can disagree (section 8).
- To compare bytes with the local files, fetch from `pages.dev` or the deployment's hash URL. Zone
  features rewrite the HTML on the custom domain — Email Address Obfuscation, bot-detection scripts
  — so it never matches the file exactly.
- The edge can lag for a few seconds after a deploy. Retry before concluding anything.
- Then look at the changed page in a real browser, at desktop and at phone width.

## 5. A small backend: Pages Functions

- Put server code in **`functions/`** in the site root. `functions/api/quote.js` answers
  `/api/quote`. Export `onRequestGet`, `onRequestPost` and so on; the handler receives
  `{ request, env }`.
- wrangler compiles `./functions` **from the folder it runs in** (in its own code:
  `path.join(process.cwd(), "functions")`), so `deploy.sh` runs from the site root, while the
  static files come from staging. Keep `/functions/` in `.cloudflareignore` so the source is never
  served as files. A good deploy prints `Compiled Worker successfully` and `Uploading Functions bundle`.
- Only files that export `onRequest…` become routes. Shared helpers can live in `functions/_lib/`
  and be imported; they never become URLs.
- **Settings and secrets** live in the project, per environment (*Production* and *Preview*), under
  dashboard → Workers & Pages → the project → Settings → Variables and Secrets. Or use
  `wrangler pages secret put NAME --project-name=my-site`, which prompts, so the owner types the
  value. Or use the API (section 9). **Changes apply only to new deployments: redeploy afterwards.**
- Build features "dark": deployed and working, but switched off by a variable
  (`CHECKOUT_ENABLED=true` to open), unlinked and `noindex`. Then launching is configuration, not a
  code change.
- Local run: `wrangler pages dev . --port 8788 --binding NAME=value`. It emulates `_redirects`,
  `404.html` and Functions, and it also serves the internal files, so it is local only.
- The runtime compatibility date comes from the project's settings (`GET` the project to see it).

## 6. Preview deployments

`bash deploy.sh --preview "msg"` deploys to branch `preview`: it is served at
`https://preview.my-site.pages.dev` with the **Preview** variables, and production is untouched.
It is the place for test keys (for example Stripe test mode) and for showing work before it goes
live. Preview URLs are public but unlisted.

## 7. Rollback and clean-up

- **Rollback:** dashboard → Deployments → ⋯ → Rollback, or
  `cf -X POST "$API/accounts/$A/pages/projects/$P/deployments/<id>/rollback"` (production
  deployments only). It does **not** change the local folder; reconcile by hand, or use git.
- **Every deployment stays public at its hash URL**, including old ones holding content you have since
  removed (old prices, internal files). Delete those — list, then
  `DELETE …/deployments/<id>?force=true` (section 9). **This is destructive and needs the owner's
  explicit OK.** The current production deployment cannot be deleted. A deleted deployment's URL can
  keep answering at the edge for hours; check it again later.

## 8. Gotchas — each one cost real time

1. **wrangler ignores `.cloudflareignore`.** Only the staging step in `deploy.sh` enforces it.
2. **Removing a file from the deployment does not unpublish it.** For up to 7 days after it was last
   served, the custom domain can still answer for a removed file — `cache-control: public,
   s-maxage=604800` and a growing `age` header — while `pages.dev` shows it gone. It is answered
   before `404.html`. Fix it with a `_redirects` line per file (evaluated first) or a cache purge by
   URL (section 9).
3. **No `404.html` means soft 404s:** every unknown URL returns the homepage with 200.
4. **`page.html` 308-redirects to `/page`.** Keep canonicals and sitemaps extensionless.
5. **The custom domain's HTML is not your file.** Email obfuscation rewrites visible addresses and
   `mailto:` links (build addresses in JavaScript if a script needs them). Compare against
   `pages.dev`.
6. **Variables and secrets reach new deployments only.** Redeploy after changing them.
7. **A guard that skips files is not a guard.** `grep -I` treats any file containing a NUL byte as
   binary and skips it — every image, and any page with a stray NUL. Use `grep -a`, and prove each
   guard by planting a file it must catch.
8. **For Claude: tool inputs decode `\uXXXX` escapes** into the real characters. A regex written
   with `\u`-escapes ends up holding control bytes, which makes grep call the file binary. Write
   `\x..` escapes instead, and scan for control characters after writing.
9. **This Mac's shell (zsh):** `grep` is ugrep, which prints paths without `./` and rejects complex
   patterns, so use `/usr/bin/grep` in scripts. zsh does not split unquoted variables into words.
   macOS `sed` has no `\s`.
10. **A proxy is set in the environment.** wrangler warns and uses it; for a direct comparison use
    `curl --noproxy '*'`.
11. **Testing forms with curl:** `-F 'field=(…)'` gives `(` a special meaning. Use `--form-string`.
12. **If the guard fires on a file that "isn't public anyway"** (for example a `_redirects` line
    naming a guarded word), change the file. Don't loosen the guard.

## 9. API cheat sheet

```bash
T="$(cat ~/.cloudflare_token)"; API=https://api.cloudflare.com/client/v4
A=<account-id>; Z=<zone-id>; P=<pages-project-name>
cf() { curl -s -H "Authorization: Bearer $T" -H "Content-Type: application/json" "$@"; }
# pipe any call into `python3 -m json.tool` to read it
```

| Task | Call |
|---|---|
| Token status | `cf "$API/user/tokens/verify"` |
| Account ID / zone ID | `cf "$API/accounts"` · `cf "$API/zones?name=example.com"` |
| Project (settings, variables, production deployment) | `cf "$API/accounts/$A/pages/projects/$P"` |
| Create project | `cf -X POST "$API/accounts/$A/pages/projects" --data '{"name":"my-site","production_branch":"main"}'` |
| Deployments | `cf "$API/accounts/$A/pages/projects/$P/deployments?per_page=25&page=1"` |
| Delete a deployment ⚠️ | `cf -X DELETE "$API/accounts/$A/pages/projects/$P/deployments/<id>?force=true"` |
| Roll back production | `cf -X POST "$API/accounts/$A/pages/projects/$P/deployments/<id>/rollback"` |
| Custom domains | `cf "$API/accounts/$A/pages/projects/$P/domains"` · add: `-X POST … --data '{"name":"example.com"}'` |
| DNS records | `cf "$API/zones/$Z/dns_records"` · add: `cf -X POST "$API/zones/$Z/dns_records" --data '{"type":"CNAME","name":"www","content":"my-site.pages.dev","proxied":true}'` |
| Purge files from the cache | `cf -X POST "$API/zones/$Z/purge_cache" --data '{"files":["https://example.com/old.md"]}'` |

**Set a plain variable** (merges with what exists; set a key to `null` to delete it). A secret is the
same call with `"type":"secret_text"`, run by the owner:

```bash
cf -X PATCH "$API/accounts/$A/pages/projects/$P" \
  --data '{"deployment_configs":{"production":{"env_vars":{"CHECKOUT_ENABLED":{"type":"plain_text","value":"false"}}}}}'
```

**www → apex redirect.** Read the phase first: a PUT replaces every rule in it, so include any rules
already there.

```bash
cf "$API/zones/$Z/rulesets/phases/http_request_dynamic_redirect/entrypoint"   # 404 = no rules yet
cf -X PUT "$API/zones/$Z/rulesets/phases/http_request_dynamic_redirect/entrypoint" --data '{
  "rules": [{
    "description": "www to apex",
    "expression": "(http.host eq \"www.example.com\")",
    "action": "redirect",
    "action_parameters": { "from_value": {
      "target_url": { "expression": "concat(\"https://example.com\", http.request.uri.path)" },
      "status_code": 301,
      "preserve_query_string": true } }
  }] }'
```

## 10. New-site checklist (copy into the project's HANDOFF)

- [ ] Token with the section 1 permissions in `~/.cloudflare_token`; account and zone IDs recorded.
- [ ] Pages project created, production branch `main`.
- [ ] `deploy.sh` and `.cloudflareignore` added; `PROJECT_NAME`, `ACCOUNT_ID`, `GUARD_WORDS` set.
- [ ] Dry run read; first deploy; `pages.dev` checked.
- [ ] Apex and www attached; both `active`; www → apex redirect.
- [ ] `404.html` (root-absolute paths); `_redirects` for any vanity or legacy URLs; extensionless
      canonicals and sitemap.
- [ ] Section 4 checks pass on the custom domain.
- [ ] The project's `HANDOFF.md` records account ID, project, zone ID, domains, token permissions
      and how to deploy.

## Appendix A — `deploy.sh` (tested 2026-09-16)

Tested cases: the dry run publishes only public files; `--preview` and `--dry-run` combine in
either order; an unknown option is refused; a guarded word hidden after a NUL byte inside an
image is caught; an internal file that slipped past the ignore list is caught; and with no token
file it stops before wrangler runs.

```bash
#!/bin/bash
# deploy.sh — publish this folder to Cloudflare Pages by direct upload.
#
#   bash deploy.sh --dry-run            list exactly what would be published; uploads nothing
#   bash deploy.sh "what changed"       deploy to production
#   bash deploy.sh --preview "msg"      deploy to the Preview environment only
#                                       (https://preview.<project>.pages.dev, Preview variables)
#
# wrangler does NOT read .cloudflareignore — it only skips .DS_Store, .git and node_modules.
# So this script copies the folder minus .cloudflareignore into a clean staging folder, refuses
# to continue if anything internal is still in it, and deploys THAT folder.

set -e

# ---- per-site settings --------------------------------------------------------------------
PROJECT_NAME="my-site"                 # the Cloudflare Pages project
ACCOUNT_ID="REPLACE_WITH_ACCOUNT_ID"   # from GET /accounts or `wrangler whoami`
PRODUCTION_BRANCH="main"               # must equal the project's production branch
PREVIEW_BRANCH="preview"
TOKEN_FILE="$HOME/.cloudflare_token"
# Words that must never appear in anything published (a parent brand, client names, internal
# code names). Case-insensitive. Leave the list empty to skip this check.
GUARD_WORDS=()
# -------------------------------------------------------------------------------------------

SITE_DIR="$(cd "$(dirname "$0")" && pwd)"
IGNORE_FILE="$SITE_DIR/.cloudflareignore"

DRY_RUN=0
BRANCH="$PRODUCTION_BRANCH"
while [[ "$1" == --* ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --preview) BRANCH="$PREVIEW_BRANCH" ;;
    *) echo "❌ Unknown option: $1 (use --dry-run and/or --preview)"; exit 1 ;;
  esac
  shift
done
COMMIT_MSG="${1:-Update from local working copy}"
if [[ "$BRANCH" == "$PRODUCTION_BRANCH" ]]; then
  TARGET="production"
else
  TARGET="Preview environment only — https://$BRANCH.$PROJECT_NAME.pages.dev"
fi

if [[ ! -f "$IGNORE_FILE" ]]; then
  echo "❌ $IGNORE_FILE is missing — refusing to deploy (it keeps internal files off the site)."
  exit 1
fi

STAGE_DIR="$(mktemp -d -t pages-deploy)"
trap 'rm -rf "$STAGE_DIR"' EXIT
rsync -a --exclude-from="$IGNORE_FILE" "$SITE_DIR/" "$STAGE_DIR/"

# Guard 1: internal files that slipped past the ignore list
LEAKED_FILES="$(cd "$STAGE_DIR" && find . -type f \( -name '*.md' -o -name 'deploy.sh' -o -name '*.token' -o -name '.cloudflare*' -o -name '.env*' -o -name '.dev.vars' \) | sed 's|^\./||')"

# Guard 2: guarded words in ANY staged file. -a reads every file as text: -I would silently skip
# any file grep thinks is binary — every image (EXIF/XMP metadata) and any page with a NUL byte.
LEAKED_TEXT=""
if (( ${#GUARD_WORDS[@]} )); then
  PATTERNS=()
  for w in "${GUARD_WORDS[@]}"; do PATTERNS+=(-e "$w"); done
  LEAKED_TEXT="$(cd "$STAGE_DIR" && /usr/bin/grep -rail "${PATTERNS[@]}" . 2>/dev/null | sed 's|^\./||' || true)"
fi

if [[ -n "$LEAKED_FILES$LEAKED_TEXT" ]]; then
  echo "❌ Refusing to deploy — this would publish internal material:"
  if [[ -n "$LEAKED_FILES" ]]; then echo "$LEAKED_FILES" | sed 's/^/     internal file: /'; fi
  if [[ -n "$LEAKED_TEXT" ]]; then echo "$LEAKED_TEXT" | sed 's/^/     guarded word in: /'; fi
  echo "   Add files to .cloudflareignore; remove the words from the pages."
  exit 1
fi

FILE_COUNT="$(find "$STAGE_DIR" -type f | wc -l | tr -d ' ')"
if [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry run — $FILE_COUNT files would be published to $TARGET (nothing uploaded):"
  (cd "$STAGE_DIR" && find . -type f | sed 's|^\./||' | sort)
  exit 0
fi

if [[ ! -f "$TOKEN_FILE" ]]; then
  echo "❌ API token file not found at $TOKEN_FILE (see the method, section 1)."
  exit 1
fi
export CLOUDFLARE_API_TOKEN="$(cat "$TOKEN_FILE")"
export CLOUDFLARE_ACCOUNT_ID="$ACCOUNT_ID"

echo "Deploying $FILE_COUNT files → Pages project $PROJECT_NAME, branch $BRANCH ($TARGET)"
echo "Message: $COMMIT_MSG"
# Run from the site folder: wrangler compiles ./functions (Pages Functions) from the folder it
# runs in, and keeps its .wrangler/ cache here — even though the static files come from staging.
cd "$SITE_DIR"
wrangler pages deploy "$STAGE_DIR" \
  --project-name="$PROJECT_NAME" \
  --branch="$BRANCH" \
  --commit-message="$COMMIT_MSG"
echo "✅ Deploy complete: $TARGET — now verify it where it lands (method, section 4)."
```

## Appendix B — `.cloudflareignore`

```gitignore
# Never published. rsync exclude patterns (deploy.sh uses --exclude-from):
# no leading slash = any depth; a leading slash = the site root only.

# secrets and tooling
.cloudflare_token
*.token
.env*
.dev.vars
deploy.sh
.cloudflareignore
.gitignore
.git/
.wrangler/
.claude/
node_modules/

# internal docs (HANDOFF.md, CLAUDE.md, memory.md, drafts…)
*.md

# OS and editor junk
.DS_Store
Thumbs.db
*.swp

# source code that must not be served as files
/functions/
/tools/

# add: source masters, unused heavy files, anything private
```
