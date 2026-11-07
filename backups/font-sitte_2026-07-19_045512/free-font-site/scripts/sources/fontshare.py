"""Fetch Fontshare catalog from the public API."""

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
    variant_label,
)

FONTSHARE_API = "https://api.fontshare.com/v2/fonts"


def fetch_raw() -> dict[str, Any]:
    all_fonts: list[dict[str, Any]] = []
    offset = 0
    limit = 100

    while True:
        resp = requests.get(
            FONTSHARE_API,
            params={"offset": offset, "limit": limit},
            timeout=60,
        )
        resp.raise_for_status()
        chunk = resp.json()
        fonts = chunk.get("fonts", [])
        all_fonts.extend(fonts)
        if not chunk.get("has_more", False) or not fonts:
            break
        offset += 1

    payload = {
        "fetched_at": now_iso(),
        "source": "fontshare",
        "url": "https://www.fontshare.com",
        "family_count": len(all_fonts),
        "fonts": all_fonts,
    }
    save_json(RAW_DIR / "fontshare.json", payload)
    return payload


def _weight_from_style_name(style_name: str) -> int:
    mapping = {
        "thin": 100, "extralight": 200, "light": 300, "regular": 400,
        "medium": 500, "semibold": 600, "bold": 700, "extrabold": 800, "black": 900,
    }
    lower = style_name.lower()
    for key, weight in mapping.items():
        if key in lower:
            return weight
    return 400


def to_catalog_entries(raw: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    if raw is None:
        from utils import load_json

        raw = load_json(RAW_DIR / "fontshare.json")

    entries: list[dict[str, Any]] = []
    for font in raw.get("fonts", []):
        name = font.get("name", "").strip()
        if not name:
            continue

        slug = slugify(name)
        license_raw = font.get("license_type") or "ITF Free Font License"
        license_type = normalize_license(license_raw)
        designers = [d.get("name", "") for d in font.get("designers", []) if d.get("name")]

        font_tags = [t.get("name") for t in font.get("font_tags", []) if t.get("name")]

        variants = []
        for style in font.get("styles", []):
            weight_obj = style.get("weight") or {}
            if isinstance(weight_obj, dict):
                style_name = weight_obj.get("label") or weight_obj.get("name") or "Regular"
                weight = weight_obj.get("number") or weight_obj.get("weight") or 400
            else:
                style_name = str(weight_obj) if weight_obj else "Regular"
                weight = _weight_from_style_name(style_name)

            style_type = "italic" if style.get("is_italic") else "normal"
            files: dict[str, str] = {}
            file_path = style.get("file")
            if file_path:
                files["woff2"] = f"https:{file_path}" if file_path.startswith("//") else file_path

            variants.append({
                "name": style_name,
                "weight": int(weight),
                "style": style_type,
                "files": files,
            })

        if not variants:
            variants.append({"name": "Regular", "weight": 400, "style": "normal", "files": {}})

        entries.append({
            "id": f"fontshare-{slug}",
            "family_name": name,
            "license_type": license_type,
            "license_url": "https://www.fontshare.com/licenses/itf-ffl",
            "commercial_use": is_commercial_ok(license_type, license_raw),
            "source": "fontshare",
            "source_url": f"https://www.fontshare.com/fonts/{slug}",
            "foundry": "Indian Type Foundry",
            "designers": designers,
            "category": normalize_category(font.get("category")),
            "subsets": ["latin"],
            "tags": ["fontshare", "brand-grade"] + font_tags,
            "featured": True,
            "featured_lists": ["fontshare"],
            "variable": bool(font.get("axes")),
            "axes": font.get("axes") or [],
            "popularity": None,
            "date_added": None,
            "last_modified": None,
            "preview_text": font.get("sample_text") or "The quick brown fox jumps over the lazy dog",
            "download_url": f"https://api.fontshare.com/v2/fonts/download/{slug}",
            "github_url": None,
            "variants": variants,
        })

    return entries


if __name__ == "__main__":
    raw_data = fetch_raw()
    entries = to_catalog_entries(raw_data)
    print(f"Fontshare: {len(entries)} families")
