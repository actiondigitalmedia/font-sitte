"""Import Nerd Fonts (icon-patched libre fonts) from FontGet-Sources."""

from __future__ import annotations

from typing import Any

import requests

from utils import RAW_DIR, now_iso, save_json, slugify

FONTGET_NERD_URL = (
    "https://raw.githubusercontent.com/Graphixa/FontGet-Sources/main/sources/nerd-fonts.json"
)


def fetch_raw() -> dict[str, Any]:
    resp = requests.get(FONTGET_NERD_URL, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    data["_fetched_at"] = now_iso()
    save_json(RAW_DIR / "nerd-fonts.json", data)
    return data


def to_catalog_entries(raw: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    if raw is None:
        from utils import load_json

        raw = load_json(RAW_DIR / "nerd-fonts.json")

    entries: list[dict[str, Any]] = []
    fonts = raw.get("fonts", {})

    for font_id, font in fonts.items():
        name = font.get("family") or font.get("name") or font_id
        variants = []
        for v in font.get("variants", []):
            files = {k: url for k, url in (v.get("files") or {}).items() if url}
            variants.append({
                "name": v.get("name", "Regular"),
                "weight": v.get("weight", 400),
                "style": v.get("style", "normal"),
                "files": files,
            })

        entries.append({
            "id": f"nerd-fonts-{slugify(font_id)}",
            "family_name": name,
            "license_type": font.get("license", "Mixed"),
            "license_url": font.get("license_url"),
            "commercial_use": True,
            "source": "nerd-fonts",
            "source_url": font.get("source_url") or f"https://www.nerdfonts.com/font-downloads",
            "foundry": font.get("foundry") or "Nerd Fonts",
            "designers": [font.get("designer")] if font.get("designer") else [],
            "category": "monospace",
            "subsets": ["latin"],
            "tags": ["nerd-font", "icons", "developer"],
            "featured": False,
            "featured_lists": [],
            "variable": False,
            "axes": [],
            "popularity": font.get("popularity"),
            "date_added": None,
            "last_modified": font.get("last_modified"),
            "preview_text": "λ ∑ ∞ → dev icons included",
            "download_url": font.get("metadata_url"),
            "github_url": "https://github.com/ryanoasis/nerd-fonts",
            "variants": variants or [{"name": "Regular", "weight": 400, "style": "normal", "files": {}}],
        })

    return entries


if __name__ == "__main__":
    raw_data = fetch_raw()
    entries = to_catalog_entries(raw_data)
    print(f"Nerd Fonts: {len(entries)} families")
