#!/usr/bin/env python3
"""Build web/catalog-lite.json from data/output/catalog.json for the browse UI."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "output" / "catalog.json"
OUT = ROOT / "web" / "catalog-lite.json"
CACHE = ROOT / "data" / "preview-cache.json"


def load_preview_cache() -> dict[str, str]:
    if not CACHE.exists():
        return {}
    raw = json.loads(CACHE.read_text(encoding="utf-8"))
    return {k: v for k, v in raw.items() if v}


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    previews = load_preview_cache()
    lite_fonts = []
    enriched = 0
    for f in data["fonts"]:
        item = {
            "id": f["id"],
            "family_name": f["family_name"],
            "license_type": f["license_type"],
            "license_url": f.get("license_url"),
            "commercial_use": f.get("commercial_use"),
            "source": f["source"],
            "source_url": f.get("source_url"),
            "category": f.get("category"),
            "featured": f.get("featured"),
            "featured_lists": f.get("featured_lists", []),
            "variable": f.get("variable"),
            "designers": f.get("designers", []),
            "tags": f.get("tags", []),
            "preview_text": f.get("preview_text"),
            "download_url": f.get("download_url"),
            "github_url": f.get("github_url"),
            "variants": [
                {
                    "name": v.get("name"),
                    "weight": v.get("weight"),
                    "style": v.get("style"),
                    "files": v.get("files", {}),
                }
                for v in (f.get("variants") or [])[:8]
            ],
            "variant_count": len(f.get("variants") or []),
        }
        # Prefer existing catalog field, then preview-cache (survives lite rebuilds)
        woff2 = f.get("preview_woff2") or previews.get(f["id"])
        if woff2:
            item["preview_woff2"] = woff2
            enriched += 1
        lite_fonts.append(item)

    info = dict(data["catalog_info"])
    info["preview_enriched"] = enriched
    OUT.write_text(
        json.dumps({"catalog_info": info, "fonts": lite_fonts}, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes, {len(lite_fonts)} families, {enriched} previews)")


if __name__ == "__main__":
    main()
