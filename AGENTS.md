# AGENTS.md

Guidance for coding agents (Codex and others) working in this repository.

**[CLAUDE.md](CLAUDE.md) is the single source of truth**: architecture, commands, design system,
content rules and pitfalls. Deployment facts live in [HANDOFF.md](HANDOFF.md). This file only
repeats the rules that must never be missed. If anything here disagrees with CLAUDE.md, CLAUDE.md wins.

- Static site on Cloudflare Pages + Pages Functions + Workers KV. **No Streamlit** (removed 2026-09-16).
- Edit `content/*.py` and rebuild (`python3 tools/build_site.py`). Never hand-edit the generated
  `site/customer/*/index.html` or `site/customer/search-index.json`.
- Publish only through `bash deploy.sh` (`--dry-run`, then `--preview`); deploy to production only
  when the owner says so.
- Never read, print or write the Cloudflare token or any password. Admin logins are created by
  the owner with `tools/set_admin.py`.
- Customer-facing content: no pricing, no internal vendor or supplier names, no pre-release
  products, partner-positive tone. Company figures must match the `streamax-knowledge` skill exactly.
