#!/usr/bin/env python3
"""Fetch real preview woff2 URLs from Google/Fontshare CSS APIs (server-side, no CORS)."""

from __future__ import annotations

import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
CATALOG_LITE = ROOT / "web" / "catalog-lite.json"
CACHE_FILE = ROOT / "data" / "preview-cache.json"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
GOOGLE_WOFF2 = re.compile(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)")
FS_WOFF2 = re.compile(r"url\(['\"]?(//cdn\.fontshare\.com/[^)'\"]+\.woff2)")


def load_cache() -> dict[str, str]:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict[str, str]) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def fetch_google_woff2(family: str, weight: int = 400) -> str | None:
    url = (
        "https://fonts.googleapis.com/css2?"
        f"family={requests.utils.quote(family)}:wght@{weight}&display=swap"
    )
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=20)
    resp.raise_for_status()
    match = GOOGLE_WOFF2.search(resp.text)
    return match.group(1) if match else None


def fetch_fontshare_woff2(slug: str, weight: int = 400) -> str | None:
    url = f"https://api.fontshare.com/v2/css?f[]={slug}@{weight}&display=swap"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    match = FS_WOFF2.search(resp.text)
    if not match:
        return None
    path = match.group(1)
    return f"https:{path}" if path.startswith("//") else path


def fetch_fontsource_woff2(slug: str, weight: int = 400) -> str | None:
    url = f"https://cdn.jsdelivr.net/fontsource/fonts/{slug}@latest/latin-{weight}-normal.woff2"
    try:
        resp = requests.head(url, timeout=15, allow_redirects=True)
        if resp.status_code == 200:
            return url
    except requests.RequestException:
        pass
    return None


def resolve_preview(font: dict, cache: dict[str, str]) -> str | None:
    key = font["id"]
    if key in cache and cache[key]:
        return cache[key]
    if key in cache:
        return None

    preview_url: str | None = None
    weight = font.get("variants", [{}])[0].get("weight", 400) if font.get("variants") else 400

    try:
        if font["source"] == "google-fonts":
            preview_url = fetch_google_woff2(font["family_name"], int(weight))
        elif font["source"] == "fontshare":
            slug = font["id"].replace("fontshare-", "", 1)
            preview_url = fetch_fontshare_woff2(slug, int(weight))
        elif font["source"] == "fontsource":
            slug = font["id"].replace("fontsource-", "", 1)
            preview_url = fetch_fontsource_woff2(slug, int(weight))
        elif font["source"] == "omnibus-type":
            preview_url = fetch_google_woff2(font["family_name"], int(weight))
    except requests.RequestException:
        preview_url = None

    cache[key] = preview_url or ""
    return preview_url


def enrich_catalog(fonts: list[dict], max_workers: int = 12) -> tuple[list[dict], int]:
    cache = load_cache()
    need_fetch = [
        f for f in fonts
        if f["source"] in ("google-fonts", "fontshare", "fontsource", "omnibus-type") and f["id"] not in cache
    ]

    print(f"Preview URLs: {len(cache)} cached, {len(need_fetch)} to fetch")

    if need_fetch:
        done = 0
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(resolve_preview, f, cache): f for f in need_fetch}
            for future in as_completed(futures):
                future.result()
                done += 1
                if done % 100 == 0:
                    print(f"  fetched {done}/{len(need_fetch)}…")
                    save_cache(cache)
                time.sleep(0.02)
        save_cache(cache)

    enriched = 0
    for font in fonts:
        url = cache.get(font["id"]) or None
        if url:
            font["preview_woff2"] = url
            enriched += 1
        else:
            font.pop("preview_woff2", None)

    return fonts, enriched


def main() -> None:
    if not CATALOG_LITE.exists():
        raise SystemExit(f"Missing {CATALOG_LITE} — run build_web_catalog.py first")

    data = json.loads(CATALOG_LITE.read_text(encoding="utf-8"))
    fonts, enriched = enrich_catalog(data["fonts"])
    data["fonts"] = fonts
    data["catalog_info"]["preview_enriched"] = enriched
    data["catalog_info"]["preview_enriched_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    CATALOG_LITE.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Enriched {enriched}/{len(fonts)} fonts with preview_woff2")


if __name__ == "__main__":
    main()
