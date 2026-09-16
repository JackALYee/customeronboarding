# FT Cloud platform simulator — reusable component

An interactive, clickable clone of the FT Cloud fleet platform (the markup brands it
**FleetMind**, the white-label name). It looks like the real product in a browser window, but it
is pure HTML/CSS/JS with sample data: **no backend, no network calls, no storage**. Built for the
customer portal's Platform Tutorials page; this doc is about reusing it anywhere else.

| | |
|---|---|
| Standalone file | [`ft-cloud-simulator.html`](ft-cloud-simulator.html) — 87 KB, one file, iframe-ready |
| Source of truth | `content/platform_tutorials.py` (Python builds the markup) |
| Regenerate | `python3 tools/export_simulator.py` |
| Contents | 3 contexts · 22 views · 4 overlay panels · 94 hover tooltips |
| External dependency | Font Awesome 6.4.0 from cdnjs — **the only** outbound request |
| Minimum comfortable width | ~920 px (one breakpoint below that) |
| Height | 662 px on most views, 738 px on the tallest (Compliance), measured at 1280 px wide |

## What's inside

- **Vision** (12 views) — Dashboard, Safety (map, risk, events), Fuel (real-time, usage),
  Compliance, Reports, Driver Coaching, Basic Data (vehicle, driver, fleet)
- **Subscription** (6) — Invoices, Details, Features, Contacts, Delivery, Organisations
- **Settings** (4) — General, Users, Privacy, Notifications
- **Overlays** — AI Agent (FleetAdvisor) slide-over, Notifications, Help, Account
- Hovering almost any control shows a pop-up explaining what that function does — the point of
  the component: it teaches the platform without giving anyone a real login.

## Use it in another project

### As an iframe (easiest, fully isolated)

Copy `ft-cloud-simulator.html` into that project and point an iframe at it:

```html
<iframe src="/path/to/ft-cloud-simulator.html"
        title="FT Cloud platform demo"
        style="width:100%; min-width:320px; height:790px; border:0;"
        loading="lazy"></iframe>
```

Height is fixed — the page does not tell the parent how tall it is. 790 px clears the tallest
view (Compliance, 738 px) plus the 14 px padding. If you want it to auto-size, add a `postMessage` of `scrollHeight` on load and a
listener in the parent; nothing in the component does that today.

### Inline, inside an existing page

Open the standalone file and copy three pieces out of it: the `<style>`, the `<div id="platform">…</div>`
markup, and the `<script>`. Then make sure the host page has all five of these:

1. **Font Awesome 6.x** loaded — every icon in the UI is a `<i class="fa-solid …">`.
2. **`[hidden] { display: none !important; }`** — see Gotchas; without it all four overlays are
   permanently visible.
3. **The eight design tokens** in the `:root` block (`--blue --gold --green --ink-3 --ink-4 --line
   --line-2 --shadow-3`). They are resolved to literal values in the standalone file.
4. **`id="platform"` on the wrapper** — the script starts with
   `document.getElementById('platform')` and does nothing if it is missing.
5. A **light background**. The component is light-themed and scoped under `.fm-sim`, so it won't
   leak styles outward, but a dark page around it will look odd.

## Re-brand and re-theme

| Change | Where |
|---|---|
| Product name (6 occurrences) | `FleetMind` in the topbar, account menu and footer |
| Address-bar URL | `app.fleetmind.com` in `.fm-url` |
| Demo user | `admin@fleetmind.io`, initials `AD` |
| Accent colour (36 occurrences) | `#7c5cff` — the platform's own purple, deliberately **not** Streamax blue |
| Surrounding chrome | the 8 tokens in `:root` |
| Typeface | the CSS asks for `DM Sans`/`Inter`; neither is loaded, so it falls back to the host stack. The standalone file has a commented-out Google Fonts link to restore the original look |

## Change the content

Edit `content/platform_tutorials.py`, not the exported HTML — the export overwrites it. The
module is built from small helpers (`_kpi`, `_table`, `_pagehead`, `_pill`, `_btn`, `_badge`,
`_nav`), one `_v_<name>()` function per view, three sidebar builders, and `_TOPBAR` / `_OVERLAYS` /
`_VIEWS` at the bottom. To add a view: write `_v_thing()`, add it to `_VIEWS`, add a `_nav(...)`
entry to the right sidebar, then:

```bash
python3 tools/build_site.py && python3 tools/export_simulator.py
```

## How the JS works

122 lines, no dependencies, scoped to `#platform`:

- `data-top` on the top-bar tabs swaps the active `.fm-rail` sidebar and jumps to that context's first view
- `data-view` on sidebar items shows the matching `.fm-view` and updates the fake address bar (`#fm-crumb`)
- `data-panel` on the top-right icons toggles a `.fm-overlay` via the `hidden` attribute; `[data-close]` closes it
- `data-tip="Title|Body"` drives the hover tooltip, positioned with `window.innerWidth/innerHeight`
- `.fm-group-head` runs the sidebar accordions, `.fm-subtab` the in-page tab strips
- It sets `data-fm-init` on the root so a double include can't bind everything twice

## Gotchas

- **The `hidden` attribute loses to a component's own `display` rule.** `.fm-overlay { display:flex }`
  beats `hidden`, so without the `[hidden] { display:none !important }` rule the AI-agent panel,
  notifications, help and account menus all render at once, stacked over the UI. This has bitten
  this codebase twice — once here, once on the portal's sign-in error box.
- **The root id is load-bearing.** Change `id="platform"` and the script silently does nothing.
- **Exclude it from site search.** In the portal it sits between `<!-- simulator -->` markers so
  the search-index builder skips it; otherwise 94 tooltips and every table cell become search hits.
- **Below 920 px** the single media query collapses the layout; it is designed for desktop.
- **It is a demo, not the product.** Sample vehicles, drivers and invoices only. Don't present it
  as live data, and don't wire it to a real API without revisiting every screen.

## Regenerating

```bash
python3 tools/export_simulator.py
python3 tools/export_simulator.py -o /somewhere/else.html
```

The exporter pulls the markup, CSS and JS straight out of the Python module, resolves the design
tokens from `site/assets/css/*.css`, and writes one self-contained file. It fails loudly if the
markers or the style/script blocks move.
