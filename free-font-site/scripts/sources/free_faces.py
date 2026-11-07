"""Scrape Free Faces gallery for candidate font names (manual-review tier)."""

from __future__ import annotations

import json
import re
from typing import Any

import requests

from utils import RAW_DIR, now_iso, save_json, slugify

FREE_FACES_URL = "https://www.freefaces.gallery/"
FF_FONTS_RE = re.compile(r"window\.FF_FONTS\s*=\s*(\[.*?\]);", re.DOTALL)


def fetch_raw() -> dict[str, Any]:
    resp = requests.get(
        FREE_FACES_URL,
        timeout=60,
        headers={"User-Agent": "Mozilla/5.0 (compatible; font-sitte-discovery/1.1)"},
    )
    resp.raise_for_status()

    fonts: list[dict[str, str]] = []
    seen: set[str] = set()

    match = FF_FONTS_RE.search(resp.text)
    if match:
        try:
            rows = json.loads(match.group(1))
            for row in rows:
                if not row or not isinstance(row, list):
                    continue
                name = (row[0] or row[1] or "").strip()
                slug = (row[2] if len(row) > 2 else slugify(name)) or slugify(name)
                if not name or len(name) > 80:
                    continue
                key = slugify(name)
                if key in seen:
                    continue
                seen.add(key)
                fonts.append({
                    "name": name,
                    "slug": slug,
                    "url": f"{FREE_FACES_URL.rstrip('/')}/fonts/{slug}",
                })
        except json.JSONDecodeError:
            pass

    payload = {
        "fetched_at": now_iso(),
        "source": "free-faces",
        "url": FREE_FACES_URL,
        "family_count": len(fonts),
        "fonts": fonts,
        "note": "Parsed window.FF_FONTS; verify license before approved-candidates.json",
    }
    save_json(RAW_DIR / "free-faces.json", payload)
    return payload


def to_catalog_entries(raw: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Do not auto-merge — discovery only. Returns empty for aggregate."""
    return []


if __name__ == "__main__":
    data = fetch_raw()
    print(f"Free Faces: {data['family_count']} font names scraped")
