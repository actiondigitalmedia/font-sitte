"""Scrape Open Foundry curated open-source typefaces."""

from __future__ import annotations

import json
import re
from typing import Any

import requests
from bs4 import BeautifulSoup

from utils import RAW_DIR, now_iso, save_json, slugify

OPEN_FOUNDRY_URL = "https://open-foundry.com/fonts"
# Open Foundry also exposes font data in page scripts
OPEN_FOUNDRY_API = "https://open-foundry.com/api/fonts"


def fetch_raw() -> dict[str, Any]:
    fonts: list[dict[str, Any]] = []

    # Try API-style endpoint first
    try:
        resp = requests.get(OPEN_FOUNDRY_API, timeout=60)
        if resp.status_code == 200 and resp.headers.get("content-type", "").startswith("application/json"):
            data = resp.json()
            if isinstance(data, list):
                fonts = data
            elif isinstance(data, dict):
                fonts = data.get("fonts", data.get("data", []))
    except (requests.RequestException, json.JSONDecodeError):
        pass

    if not fonts:
        fonts = _scrape_listing_page()

    payload = {
        "fetched_at": now_iso(),
        "source": "open-foundry",
        "url": "https://open-foundry.com",
        "family_count": len(fonts),
        "fonts": fonts,
    }
    save_json(RAW_DIR / "open-foundry.json", payload)
    return payload


def _scrape_listing_page() -> list[dict[str, Any]]:
    resp = requests.get(OPEN_FOUNDRY_URL, timeout=60, headers={"User-Agent": "free-font-site-aggregator/1.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    fonts: list[dict[str, Any]] = []

    # Look for embedded JSON in script tags
    for script in soup.find_all("script"):
        text = script.string or ""
        if "fonts" in text and ("family" in text or "name" in text):
            for match in re.finditer(r"\{[^{}]*\"name\"\s*:\s*\"([^\"]+)\"[^{}]*\}", text):
                fonts.append({"name": match.group(1)})

    # Fallback: parse font cards/links
    if not fonts:
        seen: set[str] = set()
        for link in soup.select("a[href*='/fonts/']"):
            href = link.get("href", "")
            if href in ("/fonts", "/fonts/"):
                continue
            name = link.get_text(strip=True) or href.rstrip("/").split("/")[-1]
            if not name or name in seen:
                continue
            seen.add(name)
            fonts.append({
                "name": name,
                "url": href if href.startswith("http") else f"https://open-foundry.com{href}",
            })

    return fonts


def to_catalog_entries(raw: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    if raw is None:
        from utils import load_json

        raw = load_json(RAW_DIR / "open-foundry.json")

    entries: list[dict[str, Any]] = []
    for font in raw.get("fonts", []):
        name = (font.get("name") or font.get("family") or font.get("title") or "").strip()
        if not name:
            continue

        slug = slugify(name)
        source_url = font.get("url") or font.get("source_url") or f"https://open-foundry.com/fonts/{slug}"

        entries.append({
            "id": f"open-foundry-{slug}",
            "family_name": name,
            "license_type": font.get("license") or "OFL",
            "license_url": font.get("license_url") or "https://openfontlicense.org",
            "commercial_use": True,
            "source": "open-foundry",
            "source_url": source_url,
            "foundry": font.get("foundry") or font.get("designer") or "Open Foundry",
            "designers": [font.get("designer")] if font.get("designer") else [],
            "category": (font.get("category") or "display").lower().replace(" ", "-"),
            "subsets": font.get("subsets") or ["latin"],
            "tags": ["open-foundry", "curated", "libre"],
            "featured": True,
            "featured_lists": ["open-foundry"],
            "variable": bool(font.get("variable")),
            "axes": font.get("axes") or [],
            "popularity": None,
            "date_added": None,
            "last_modified": None,
            "preview_text": font.get("description") or "Open-source typeface from Open Foundry",
            "download_url": font.get("download_url") or source_url,
            "github_url": font.get("github_url"),
            "variants": [{"name": "Regular", "weight": 400, "style": "normal", "files": {}}],
        })

    return entries


if __name__ == "__main__":
    raw_data = fetch_raw()
    entries = to_catalog_entries(raw_data)
    print(f"Open Foundry: {len(entries)} families")
