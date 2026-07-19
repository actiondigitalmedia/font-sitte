#!/usr/bin/env python3
"""Static file server with same-origin font proxy for Cursor/embedded browsers."""

from __future__ import annotations

import sys
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from functools import partial

try:
    from http.server import SimpleHTTPRequestHandler
except ImportError:
    from http.server import SimpleHTTPRequestHandler  # type: ignore

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_PREFIXES = (
    "https://fonts.gstatic.com/",
    "https://cdn.fontshare.com/",
)


class FontSiteHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str | None = None, **kwargs):
        super().__init__(*args, directory=directory or str(ROOT), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/proxy-font":
            self._proxy_font(parse_qs(parsed.query).get("url", [""])[0])
            return
        if parsed.path == "/":
            self.send_response(302)
            self.send_header("Location", "/web/")
            self.end_headers()
            return
        super().do_GET()

    def _proxy_font(self, raw_url: str) -> None:
        url = unquote(raw_url)
        if not url.startswith(ALLOWED_PREFIXES):
            self.send_error(403, "URL not allowed")
            return
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "font-sitte-proxy/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                ctype = resp.headers.get("Content-Type", "font/woff2")
        except urllib.error.HTTPError as exc:
            self.send_error(exc.code, exc.reason)
            return
        except urllib.error.URLError:
            self.send_error(502, "Upstream font fetch failed")
            return

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "public, max-age=604800")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args) -> None:
        if str(args[0]).startswith("GET /proxy-font"):
            return
        super().log_message(format, *args)


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    handler = partial(FontSiteHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("0.0.0.0", port), handler)
    print(f"Serving {ROOT} on http://0.0.0.0:{port}")
    print(f"UI: http://localhost:{port}/web/")
    print(f"Health: http://localhost:{port}/health.html")
    server.serve_forever()


if __name__ == "__main__":
    main()
