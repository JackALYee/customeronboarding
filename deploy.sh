#!/bin/bash
# deploy.sh — publish the onboarding portal to Cloudflare Pages by direct upload.
# Adapted from cloudflare_deploy_method.md, Appendix A.
#
#   bash deploy.sh --dry-run            build + list exactly what would be published; uploads nothing
#   bash deploy.sh "what changed"       deploy to production (www.streamax-trucking.com)
#   bash deploy.sh --preview "msg"      deploy to the Preview environment only
#                                       (https://preview.streamax-onboarding.pages.dev, Preview KV)
#
# Differences from the method's template:
#   - runs tools/build_site.py first (customer pages are generated from content/*.py)
#   - publishes ONLY ./site (the repo root holds source, tools and docs)
#   - Pages Functions come from ./functions (wrangler compiles them from the folder it runs in)
# wrangler does NOT read .cloudflareignore, so the staging copy below enforces it.

set -e

# ---- per-site settings --------------------------------------------------------------------
PROJECT_NAME="streamax-onboarding"
ACCOUNT_ID="b377955e9eb4b1916473ebafa6ec2859"
PRODUCTION_BRANCH="main"
PREVIEW_BRANCH="preview"
TOKEN_FILE="$HOME/.cloudflare_token"
# Never publishable (content boundaries: internal vendor names, the FleetMind dev host).
# Case-insensitive. Never put a secret itself in this list - it would be committed.
GUARD_WORDS=("webbing" "inventure" "cango" "fleetmind-dev")
# -------------------------------------------------------------------------------------------

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
PUBLIC_DIR="$REPO_DIR/site"
IGNORE_FILE="$REPO_DIR/.cloudflareignore"

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

echo "Building customer pages from content/ ..."
python3 "$REPO_DIR/tools/build_site.py"

STAGE_DIR="$(mktemp -d -t pages-deploy)"
trap 'rm -rf "$STAGE_DIR"' EXIT
rsync -a --exclude-from="$IGNORE_FILE" "$PUBLIC_DIR/" "$STAGE_DIR/"

# Guard 1: internal files that slipped past the ignore list
LEAKED_FILES="$(cd "$STAGE_DIR" && find . -type f \( -name '*.md' -o -name '*.py' -o -name 'deploy.sh' -o -name '*.token' -o -name '.cloudflare*' -o -name '.env*' -o -name '.dev.vars' -o -name 'cloudflare.json' \) | sed 's|^\./||')"

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
  echo "Pages Functions (compiled from ./functions, never served as files):"
  (cd "$REPO_DIR" && find functions -type f -name '*.js' ! -path '*/_lib/*' | sed 's|^functions||;s|\.js$||;s|/index$||;s|/_middleware$| (middleware)|' | sort | sed 's/^/     /')
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
# Run from the repo root: wrangler compiles ./functions from the folder it runs in and keeps
# its .wrangler/ cache here — even though the static files come from staging.
cd "$REPO_DIR"
wrangler pages deploy "$STAGE_DIR" \
  --project-name="$PROJECT_NAME" \
  --branch="$BRANCH" \
  --commit-message="$COMMIT_MSG" \
  --commit-dirty=true
echo "✅ Deploy complete: $TARGET — now verify it where it lands (method, section 4)."
