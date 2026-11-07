"""Import non-Google fonts from Fontsource API (verified OFL/Apache)."""

from __future__ import annotations

from typing import Any

import requests

from utils import RAW_DIR, normalize_category, normalize_license, now_iso, save_json, slugify

FONTSOURCE_API = "https://api.fontsource.org/v1/fonts"


def fetch_raw() -> dict[str, Any]:
    resp = requests.get(FONTSOURCE_API, timeout=120)
    resp.raise_for_status()
    all_fonts = resp.json()

    # Fontsource includes Google mirrors — only keep non-google for new families
    fonts = [f for f in all_fonts if f.get("type") != "google"]

    payload = {
        "fetched_at": now_iso(),
        "source": "fontsource",
        "url": "https://fontsource.org",
        "family_count": len(fonts),
        "fonts": fonts,
    }
    save_json(RAW_DIR / "fontsource.json", payload)
    return payload


def to_catalog_entries(raw: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    if raw is None:
        from utils import load_json

        raw = load_json(RAW_DIR / "fontsource.json")

    entries: list[dict[str, Any]] = []
    for font in raw.get("fonts", []):
        name = font.get("family", "").strip()
        if not name:
            continue

        slug = font.get("id") or slugify(name)
        license_raw = font.get("license", "OFL-1.1")
        license_type = normalize_license(license_raw)

        variants = []
        for weight in font.get("weights", [400]):
            for style in font.get("styles", ["normal"]):
                style_name = "Regular" if weight == 400 and style == "normal" else f"{weight} {style}"
                variants.append({
                    "name": style_name.strip(),
                    "weight": int(weight),
                    "style": style if style in ("normal", "italic") else "normal",
                    "files": {},
                })

        if not variants:
            variants = [{"name": "Regular", "weight": 400, "style": "normal", "files": {}}]

        entries.append({
            "id": f"fontsource-{slug}",
            "family_name": name,
            "license_type": license_type,
            "license_url": "https://openfontlicense.org",
            "commercial_use": True,
            "source": "fontsource",
            "source_url": f"https://fontsource.org/fonts/{slug}",
            "foundry": "Fontsource",
            "designers": [],
            "category": normalize_category(font.get("category")),
            "subsets": font.get("subsets", ["latin"]),
            "tags": ["fontsource", font.get("type", "libre")],
            "featured": False,
            "featured_lists": [],
            "variable": bool(font.get("variable")),
            "axes": [],
            "popularity": None,
            "date_added": font.get("lastModified"),
            "last_modified": font.get("lastModified"),
            "preview_text": "The quick brown fox jumps over the lazy dog",
            "download_url": f"https://fontsource.org/fonts/{slug}",
            "github_url": f"https://github.com/fontsource/font-files/tree/main/fonts/google/{slug}" if font.get("type") == "google" else None,
            "variants": variants,
        })

    return entries


if __name__ == "__main__":
    raw_data = fetch_raw()
    entries = to_catalog_entries(raw_data)
    print(f"Fontsource (non-Google): {len(entries)} families")
