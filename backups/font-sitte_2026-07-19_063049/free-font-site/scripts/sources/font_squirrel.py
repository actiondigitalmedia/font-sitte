"""Import Font Squirrel free commercial fonts via FontGet-Sources mirror."""

from __future__ import annotations

from typing import Any

import requests

from utils import (
    RAW_DIR,
    is_commercial_ok,
    normalize_category,
    normalize_license,
    now_iso,
    save_json,
    slugify,
)

FONTGET_SQUIRREL_URL = (
    "https://raw.githubusercontent.com/Graphixa/FontGet-Sources/main/sources/font-squirrel.json"
)


def fetch_raw() -> dict[str, Any]:
    resp = requests.get(FONTGET_SQUIRREL_URL, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    data["_fetched_at"] = now_iso()
    save_json(RAW_DIR / "font-squirrel.json", data)
    return data


def to_catalog_entries(raw: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    if raw is None:
        from utils import load_json

        raw = load_json(RAW_DIR / "font-squirrel.json")

    entries: list[dict[str, Any]] = []
    fonts = raw.get("fonts", {})

    for font_id, font in fonts.items():
        name = font.get("family") or font.get("name") or font_id
        license_raw = font.get("license", "")
        license_type = normalize_license(license_raw)

        variants = []
        for v in font.get("variants", []):
            files = {k: url for k, url in (v.get("files") or {}).items() if url}
            variants.append({
                "name": v.get("name", "Regular"),
                "weight": v.get("weight", 400),
                "style": v.get("style", "normal"),
                "files": files,
            })

        if not variants:
            variants = [{"name": "Regular", "weight": 400, "style": "normal", "files": {}}]

        categories = font.get("categories") or []
        category = normalize_category(categories[0] if categories else "display")

        entries.append({
            "id": f"font-squirrel-{slugify(font_id)}",
            "family_name": name,
            "license_type": license_type,
            "license_url": font.get("license_url"),
            "commercial_use": is_commercial_ok(license_type, license_raw),
            "source": "font-squirrel",
            "source_url": font.get("source_url") or f"https://www.fontsquirrel.com/fonts/{font_id}",
            "foundry": font.get("foundry"),
            "designers": [font.get("designer")] if font.get("designer") else [],
            "category": category,
            "subsets": [],
            "tags": font.get("tags") or ["font-squirrel"],
            "featured": False,
            "featured_lists": [],
            "variable": False,
            "axes": [],
            "popularity": font.get("popularity"),
            "date_added": None,
            "last_modified": font.get("last_modified"),
            "preview_text": font.get("sample_text") or "The quick brown fox jumps over the lazy dog",
            "download_url": font.get("source_url"),
            "github_url": None,
            "variants": variants,
        })

    return entries


if __name__ == "__main__":
    raw_data = fetch_raw()
    entries = to_catalog_entries(raw_data)
    commercial = sum(1 for e in entries if e["commercial_use"])
    print(f"Font Squirrel: {len(entries)} families ({commercial} commercial-OK)")
