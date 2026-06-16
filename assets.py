"""Static assets, inlined as base64 data URIs.

The Streamax mascot is loaded from a local PNG and embedded as a data URI
rather than hot-linked from Google Drive — Drive blocks <img> hotlinking
(rate limits / cookie checks), and a data URI also works inside the
sandboxed components.html iframe where a relative path wouldn't resolve.
"""
import base64
from pathlib import Path

_ASSETS_DIR = Path(__file__).parent / "assets"


def _data_uri(filename: str, mime: str) -> str:
    try:
        raw = (_ASSETS_DIR / filename).read_bytes()
        return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"
    except Exception:
        return ""  # img onerror handlers hide a broken/empty src gracefully


MASCOT_DATA_URI = _data_uri("mascot.png", "image/png")
