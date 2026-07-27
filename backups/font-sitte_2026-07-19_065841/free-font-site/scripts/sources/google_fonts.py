"""Fetch Google Fonts metadata from the public fonts.google.com endpoint."""

from __future__ import annotations

import json
from typing import Any

import requests

from utils import (
    RAW_DIR,
    as_tag_list,
    is_commercial_ok,
    normalize_category,
    normalize_license,
    now_iso,
    parse_google_variant_key,
    save_json,
    slugify,
    variant_label,
)

GOOGLE_METADATA_URL = "https://fonts.google.com/metadata/fonts"
LICENSE_DIRS = {"ofl": "OFL", "apache": "Apache-2.0", "ufl": "UFL"}


def _parse_metadata_response(text: str) -> dict[str, Any]:
    # Google prefixes JSON with )]}' to prevent XSSI
    if text.startswith(")]}'"):
        text = text.split("\n", 1)[-1]
    return json.loads(text)


def _infer_license(family: dict[str, Any]) -> str:
    name = family.get("family", "")
    slug = slugify(name)
    for directory, license_name in LICENSE_DIRS.items():
        url = f"https://github.com/google/fonts/tree/main/{directory}/{slug}"
        # METADATA doesn't always include license; infer from repo structure convention
        if family.get("isNoto"):
            return "OFL"
    # Default for Google Fonts catalog — all are open source
    return "OFL"


def fetch_raw() -> dict[str, Any]:
    resp = requests.get(GOOGLE_METADATA_URL, timeout=120)
    resp.raise_for_status()
    data = _parse_metadata_response(resp.text)
    payload = {
        "fetched_at": now_iso(),
        "source": "google-fonts",
        "url": "https://fonts.google.com",
        "family_count": len(data.get("familyMetadataList", [])),
        "families": data.get("familyMetadataList", []),
    }
    save_json(RAW_DIR / "google-fonts.json", payload)
    return payload


def to_catalog_entries(raw: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    if raw is None:
        from utils import load_json

        raw = load_json(RAW_DIR / "google-fonts.json")

    entries: list[dict[str, Any]] = []
    for family in raw.get("families", []):
        name = family.get("family", "").strip()
        if not name:
            continue

        slug = slugify(name)
        license_type = _infer_license(family)
        fonts_meta = family.get("fonts", {}) or {}
        variants = []
        for key in sorted(fonts_meta.keys(), key=lambda k: (parse_google_variant_key(k)[0], parse_google_variant_key(k)[1])):
            weight, style = parse_google_variant_key(key)
            variants.append({
                "name": variant_label(weight, style),
                "weight": weight,
                "style": style,
                "files": {},
            })

        axes = family.get("axes") or []
        designers = [d.get("name", d) if isinstance(d, dict) else str(d) for d in family.get("designers", [])]

        entries.append({
            "id": slug,
            "family_name": name,
            "license_type": license_type,
            "license_url": "https://openfontlicense.org",
            "commercial_use": is_commercial_ok(license_type),
            "source": "google-fonts",
            "source_url": f"https://fonts.google.com/specimen/{name.replace(' ', '+')}",
            "foundry": "Google Fonts",
            "designers": designers,
            "category": normalize_category(family.get("category")),
            "subsets": [s for s in family.get("subsets", []) if s != "menu"],
            "tags": as_tag_list(family.get("stroke")),
            "featured": False,
            "featured_lists": [],
            "variable": bool(axes),
            "axes": [
                {
                    "tag": a.get("tag"),
                    "min": a.get("min"),
                    "max": a.get("max"),
                    "default": a.get("defaultValue"),
                }
                for a in axes
            ],
            "popularity": family.get("popularity"),
            "date_added": family.get("dateAdded"),
            "last_modified": family.get("lastModified"),
            "preview_text": "The quick brown fox jumps over the lazy dog",
            "download_url": f"https://github.com/google/fonts/tree/main/ofl/{slug}",
            "github_url": f"https://github.com/google/fonts/tree/main/ofl/{slug}",
            "variants": variants,
        })

    return entries


if __name__ == "__main__":
    raw_data = fetch_raw()
    entries = to_catalog_entries(raw_data)
    print(f"Google Fonts: {len(entries)} families")
