#!/usr/bin/env python3
"""Export the FT Cloud / FleetMind platform simulator as one self-contained HTML file.

    python3 tools/export_simulator.py            -> docs/ft-cloud-simulator.html
    python3 tools/export_simulator.py -o out.html

The simulator lives inside content/platform_tutorials.py (markup between the
<!-- simulator --> markers, plus its own <style> and <script>). That module is the
source of truth; this script only repackages it so it can be dropped into another
project or iframed. See docs/ft-cloud-simulator.md.

Standalone means: no stx.css, no portal.js, no build step. The design tokens the
simulator borrows from the portal are resolved to literal values and inlined.
"""
import argparse
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "content" / "platform_tutorials.py"
CSS_FILES = (ROOT / "site/assets/css/stx.css", ROOT / "site/assets/css/portal.css")
DEFAULT_OUT = ROOT / "docs" / "ft-cloud-simulator.html"
FONT_AWESOME = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"


def load_content() -> str:
    spec = importlib.util.spec_from_file_location("platform_tutorials", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.content


def pick_block(html: str, tag: str, must_contain: str) -> str:
    for body in re.findall(rf"<{tag}[^>]*>(.*?)</{tag}>", html, re.S):
        if must_contain in body:
            return body.strip()
    raise SystemExit(f"export_simulator: no <{tag}> containing {must_contain!r}")


def resolve_tokens(names: set[str]) -> tuple[dict[str, str], list[str]]:
    """Read --token: value pairs from the portal's CSS and follow var() aliases.

    Variables the portal does not declare are component-local (e.g. --pct, set inline
    on a bar element); they are returned as the second item and left alone."""
    declared: dict[str, str] = {}
    for path in CSS_FILES:
        for name, value in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;}]+)[;}]", path.read_text()):
            declared.setdefault(name, value.strip())

    def resolve(name: str, depth: int = 0) -> str:
        value = declared.get(name, "")
        if depth > 4 or "var(" not in value:
            return value
        return re.sub(r"var\((--[a-z0-9-]+)\)", lambda m: resolve(m.group(1), depth + 1), value)

    out, local = {}, []
    for name in sorted(names):
        value = resolve(name)
        (out.__setitem__(name, value) if value else local.append(name))
    return out, local


def build(out_path: Path) -> None:
    content = load_content()
    start = content.index("<!-- simulator -->")
    end = content.index("<!-- /simulator -->")
    window = re.search(r'<div class="fm-window">.*?</div>\s*</div>\s*$',
                       content[start:end].rstrip(), re.S)
    if not window:
        raise SystemExit("export_simulator: could not find the .fm-window markup")
    markup = window.group(0)
    css = pick_block(content, "style", ".fm-window")
    js = pick_block(content, "script", "data-top")

    tokens, local_vars = resolve_tokens(set(re.findall(r"var\((--[a-z0-9-]+)", css)))
    token_css = "\n".join(f"      {name}: {value};" for name, value in tokens.items())

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FT Cloud platform - interactive demo</title>
<link rel="stylesheet" href="{FONT_AWESOME}">
<style>
    /* Design tokens the simulator borrows from the portal, resolved to literals.
       Re-theme the component by changing these. */
    :root {{
{token_css}
    }}
    /* The overlays (AI agent, notifications, help, account) are toggled with the
       hidden attribute, and their own display rules would otherwise beat it. */
    [hidden] {{ display: none !important; }}
    html, body {{ margin: 0; background: #fff; }}
    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                   'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', sans-serif;
      padding: 14px;
    }}
    /* The simulator asks for 'DM Sans'/'Inter'. The portal does not load them, so it
       falls back to the stack above. To match the original FleetMind look, add:
       <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Inter:wght@400;500;600&display=swap"> */
{css}
</style>
</head>
<body>
<!-- The script scopes itself to this id - keep it, or change both here and in the script. -->
<div id="platform">
{markup}
</div>
<script>
{js}
</script>
</body>
</html>
"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page, encoding="utf-8")
    views = len(re.findall(r'class="fm-view"|class="fm-view ', markup))
    print(f"export_simulator: wrote {out_path.relative_to(ROOT)} ({len(page) // 1024} KB)")
    print(f"  views: {views} · tokens inlined: {len(tokens)} · css {len(css) // 1024} KB · js {len(js) // 1024} KB")
    if local_vars:
        print(f"  set inline by the markup, left as-is: {', '.join(local_vars)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--out", type=Path, default=DEFAULT_OUT)
    build(ap.parse_args().out)
