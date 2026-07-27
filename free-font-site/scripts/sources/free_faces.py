"""Scrape Free Faces gallery for candidate font names (manual-review tier)."""

from __future__ import annotations

import json
import re
from typing import Any

import requests
from bs4 import BeautifulSoup

from utils import RAW_DIR, now_iso, save_json, slugify

FREE_FACES_URL = "https://www.freefaces.gallery/"


def fetch_raw() -> dict[str, Any]:
    resp = requests.get(
        FREE_FACES_URL,
        timeout=60,
        headers={"User-Agent": "font-sitte-discovery/1.0"},
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    fonts: list[dict[str, str]] = []
    seen: set[str] = set()

    for tag in soup.find_all(["h1", "h2", "h3", "h4", "a", "p", "span"]):
        text = tag.get_text(strip=True)
        if not text or len(text) > 80 or len(text) < 3:
            continue
        if text.lower() in {"free faces", "fonts", "download", "about", "submit"}:
            continue
        # Heuristic: Title Case multi-word or known font-like tokens
        if re.match(r"^[A-Z0-9][A-Za-z0-9 \-]+$", text) and " " in text or len(text) <= 24:
            key = slugify(text)
            if key in seen:
                continue
            seen.add(key)
            href = tag.get("href") if tag.name == "a" else None
            fonts.append({
                "name": text,
                "slug": key,
                "url": href if href and href.startswith("http") else FREE_FACES_URL,
            })

    payload = {
        "fetched_at": now_iso(),
        "source": "free-faces",
        "url": FREE_FACES_URL,
        "family_count": len(fonts),
        "fonts": fonts[:200],
        "note": "Scraped names require manual license verification before approved-candidates.json",
    }
    save_json(RAW_DIR / "free-faces.json", payload)
    return payload


def to_catalog_entries(raw: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Do not auto-merge — discovery only. Returns empty for aggregate."""
    return []
