#!/usr/bin/env python3
"""Apply style_tags from discovery/style-taxonomy.json to catalog fonts."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY = ROOT / "discovery" / "style-taxonomy.json"
CATALOG = ROOT / "data" / "output" / "catalog.json"


def _matches(font: dict, rule: dict) -> bool:
    name = font.get("family_name", "").lower()
    blob = " ".join([
        name,
        font.get("category", ""),
        font.get("source", ""),
        " ".join(font.get("tags") or []),
        " ".join(font.get("designers") or []),
    ]).lower()

    for kw in rule.get("keywords", []):
        if kw.lower() in blob:
            return True

    for pat in rule.get("family_name_patterns", []):
        if pat.lower() in name:
            return True

    if font.get("category") in rule.get("categories", []):
        return True

    if font.get("source") in rule.get("sources", []):
        return True

    return False


def apply_to_fonts(fonts: list[dict]) -> tuple[list[dict], dict[str, int]]:
    taxonomy = json.loads(TAXONOMY.read_text(encoding="utf-8"))
    counts: dict[str, int] = {}

    for font in fonts:
        existing = set(font.get("style_tags") or [])
        for tag_id, rule in taxonomy.get("style_tags", {}).items():
            if _matches(font, rule):
                existing.add(tag_id)
                counts[tag_id] = counts.get(tag_id, 0) + 1
        font["style_tags"] = sorted(existing)

    return fonts, counts


def main() -> None:
    if not CATALOG.exists():
        raise SystemExit("Run aggregate.py first")

    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    fonts, counts = apply_to_fonts(data["fonts"])
    data["fonts"] = fonts
    data["catalog_info"]["style_tag_counts"] = dict(sorted(counts.items(), key=lambda x: -x[1]))
    data["catalog_info"]["style_tags_applied_at"] = __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc
    ).replace(microsecond=0).isoformat()

    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Style tags applied:")
    for tag, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {tag}: {n}")


if __name__ == "__main__":
    main()
