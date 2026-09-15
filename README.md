# Streamax Customer Onboarding Portal

A guided onboarding site for new Streamax fleet customers and TSP / channel partners, with a
staff admin for managing client accounts.

- **Customer portal:** https://www.streamax-trucking.com/customer
- **Staff admin:** https://www.streamax-trucking.com/admin

Static pages on Cloudflare Pages; sign-in and data run on Pages Functions + Workers KV. There is
no server to run or keep alive.

## What's in it

Eight pages behind a customer sign-in:

1. **Welcome**: scroll-driven brand intro, your first 30 days, a map of the portal, Day-1 checks and your Streamax team
2. **My Products**: the product catalogue by family (dashcams, gateways, MDVRs and more) with downloads
3. **Installation**: step-by-step installation guides per product
4. **Platform Tutorials**: a live platform demo and guided how-tos (CAN Bus License and eSIM activation are placeholders)
5. **AI Features**: SafeGPT, Evidence Cards, ADAS and DMS detections
6. **Training Academy**: role-based learning paths and sample lessons
7. **Playbooks**: first-90-days plan, driver coaching, driver buy-in, accident workflow, industry playbooks
8. **Support**: how to get help, FAQ, downloads, what's new

Across the site: search (Ctrl K / ⌘ K), a language menu, and shareable links to any heading.

## Accounts

There is no self sign-up. Staff create each client in `/admin` (email, company, fleet or TSP,
password) and hand the credentials over. From the admin they can also reset a password (which signs
the client out everywhere), turn access off, edit the key contacts shown on Welcome, or delete
the account.

Admin logins are created by the owner:

```bash
python3 tools/set_admin.py
```

## Working on it

```bash
python3 tools/build_site.py
python3 tools/preview_server.py
bash deploy.sh --dry-run
bash deploy.sh --preview "what changed"
bash deploy.sh "what changed"
```

In order: regenerate the customer pages from `content/*.py`; preview locally at
http://localhost:8790/customer/ (demo data, no sign-in); list exactly what would be published;
deploy to the preview environment; deploy to production.

## Files

| Path | Purpose |
|---|---|
| `content/` | The eight sections; each module exports one section's HTML |
| `tools/build_site.py` | Wraps the sections in the shared page shell; writes `site/customer/` and the search index |
| `site/` | Everything that gets published: sign-in pages, admin, CSS/JS, images, the brand morph |
| `functions/` | Sign-in, sessions, page gating and the admin API (Cloudflare Pages Functions) |
| `tools/set_admin.py` | Create, reset or remove admin logins |
| `tools/preview_server.py` | Local preview server |
| `deploy.sh` | Build, stage, guard and deploy |
| `HANDOFF.md` | Deployment facts: domains, IDs, security model, known limits |
| `CLAUDE.md` | Developer guide: architecture, design system, content rules, pitfalls |
