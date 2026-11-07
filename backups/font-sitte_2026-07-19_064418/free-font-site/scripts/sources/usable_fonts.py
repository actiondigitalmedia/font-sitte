"""Parse the usable-fonts curated list for featured tagging."""

from __future__ import annotations

import re
from typing import Any

import requests

from utils import RAW_DIR, now_iso, save_json, slugify

USABLE_FONTS_README = "https://raw.githubusercontent.com/menozero/usable-fonts/main/README.md"

# Typewolf's commonly cited top Google Fonts (open-source, commercial-safe)
TYPEWOLF_TOP = [
    "Inter", "Roboto", "Open Sans", "Lato", "Montserrat", "Source Sans Pro",
    "Source Sans 3", "Raleway", "Poppins", "Nunito", "Merriweather",
    "Playfair Display", "Oswald", "Roboto Slab", "PT Sans", "Noto Sans",
    "Work Sans", "Rubik", "Fira Sans", "IBM Plex Sans", "Libre Baskerville",
    "Crimson Text", "Bitter", "Arvo", "Inconsolata", "Space Mono",
    "DM Sans", "Manrope", "Sora", "Outfit", "Figtree", "Plus Jakarta Sans",
    "Lexend", "Archivo", "Barlow", "Mulish", "Karla", "Josefin Sans",
    "Bebas Neue", "Anton", "Abril Fatface",
]


def fetch_raw() -> dict[str, Any]:
    resp = requests.get(USABLE_FONTS_README, timeout=30)
    resp.raise_for_status()
    text = resp.text

    fonts: list[dict[str, str]] = []
    # README uses bullet lists like "- **Font Name** (OFL)"
    for match in re.finditer(r"^[-*]\s+\*?\*?([A-Za-z0-9][^(*\n]+?)\*?\*?\s*(?:\(([^)]+)\))?", text, re.MULTILINE):
        name = match.group(1).strip().strip("*").strip()
        license_note = (match.group(2) or "").strip()
        if len(name) < 2 or name.lower() in ("font", "license"):
            continue
        if name.startswith("http"):
            continue
        fonts.append({"name": name, "license": license_note, "slug": slugify(name)})

    payload = {
        "fetched_at": now_iso(),
        "source": "usable-fonts",
        "url": "https://github.com/menozero/usable-fonts",
        "fonts": fonts,
        "typewolf_top": [{"name": n, "slug": slugify(n)} for n in TYPEWOLF_TOP],
    }
    save_json(RAW_DIR / "usable-fonts.json", payload)
    return payload


def get_featured_map(raw: dict[str, Any] | None = None) -> dict[str, list[str]]:
    """Return slug -> featured list names."""
    if raw is None:
        from utils import load_json

        raw = load_json(RAW_DIR / "usable-fonts.json")

    featured: dict[str, list[str]] = {}
    for item in raw.get("fonts", []):
        slug = item["slug"]
        featured.setdefault(slug, []).append("usable-fonts")

    for item in raw.get("typewolf_top", []):
        slug = item["slug"]
        featured.setdefault(slug, []).append("typewolf-top")

    return featured


if __name__ == "__main__":
    data = fetch_raw()
    featured = get_featured_map(data)
    print(f"Usable Fonts curated: {len(data.get('fonts', []))} entries, {len(featured)} featured slugs")
