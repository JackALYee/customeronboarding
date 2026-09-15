#!/usr/bin/env python3
"""Local visual preview of ./site - no Cloudflare, no auth, no real data.

    python3 tools/build_site.py && python3 tools/preview_server.py     -> http://localhost:8790/customer/

Serves site/ the way Cloudflare Pages does for the parts that matter visually
(directory index.html, extensionless *.html) and answers /api/customer/me with a
fixed demo client so the identity chip and Key Contacts render. The real gate,
sign-in and admin API only exist on Cloudflare (functions/) - test those on the
Preview deployment instead (see HANDOFF.md). Never deployed (tools/ isn't published).
"""
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "site"
PORT = int(os.environ.get("PORT", sys.argv[1] if len(sys.argv) > 1 else 8790))

DEMO_ME = {
    "email": "demo@example.com",
    "company": "Demo Fleet (local preview)",
    "audience": "fleet",
    "audience_label": "Fleet Operator",
    "contacts": [
        {"role": "Customer Success", "contact": "csm@streamax.com"},
        {"role": "Technical Support", "contact": "support@streamax.com"},
        {"role": "Hardware RMA", "contact": "rma@streamax.com"},
        {"role": "Billing", "contact": "billing@streamax.com"},
        {"role": "Emergency hotline", "contact": "Available 24/7 via your CSM"},
    ],
}


DEMO_CUSTOMERS = [
    {"email": "ops@northline-freight.example", "company": "Northline Freight", "audience": "fleet",
     "created_at": "2026-09-10T08:12:00Z", "created_by": "staff:demo-admin", "first_login_at": "2026-09-11T02:40:00Z",
     "last_login_at": "2026-09-15T23:05:00Z", "disabled": False},
    {"email": "it@meridian-telematics.example", "company": "Meridian Telematics", "audience": "tsp",
     "created_at": "2026-09-14T06:00:00Z", "created_by": "staff:demo-admin", "first_login_at": None,
     "last_login_at": None, "disabled": False},
    {"email": "safety@harbor-transit.example", "company": "Harbor Transit Authority", "audience": "fleet",
     "created_at": "2026-08-28T09:30:00Z", "created_by": "staff:demo-admin", "first_login_at": "2026-08-29T01:10:00Z",
     "last_login_at": "2026-09-02T04:22:00Z", "disabled": True},
]
DEMO_EVENTS = [
    {"email": "ops@northline-freight.example", "role": "customer", "method": "password", "at": "2026-09-15T23:05:00Z"},
    {"email": "demo-admin", "role": "staff", "method": "password", "at": "2026-09-15T22:58:00Z"},
    {"email": "ops@northline-freight.example", "role": "customer", "method": "password", "at": "2026-09-13T07:41:00Z"},
]


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        if path == "/api/customer/me":
            return self._json(DEMO_ME)
        if path == "/api/admin/me":
            return self._json({"username": "demo-admin"})
        if path == "/api/admin/customers":
            return self._json({"customers": DEMO_CUSTOMERS})
        if path.startswith("/api/admin/customers/"):
            email = path.rsplit("/", 1)[1].replace("%40", "@")
            c = next((x for x in DEMO_CUSTOMERS if x["email"] == email), DEMO_CUSTOMERS[0])
            return self._json({"customer": {**c, "audience_label": "TSP / Channel Partner" if c["audience"] == "tsp" else "Fleet Operator",
                                            "contacts": DEMO_ME["contacts"], "contacts_are_default": True}})
        if path == "/api/admin/events":
            return self._json({"events": DEMO_EVENTS, "total": len(DEMO_EVENTS), "total_capped": False})
        # extensionless -> .html, like Pages
        target = ROOT / path.lstrip("/")
        if not target.exists() and target.with_suffix(".html").exists():
            self.path = path + ".html"
        return super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/customer/logout"):
            return self._json({"ok": True})
        return self._json({"error": "Local preview has no backend - sign-in only works on Cloudflare."}, 501)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    print(f"LOCAL PREVIEW (no auth, demo data) -> http://localhost:{PORT}/customer/")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
