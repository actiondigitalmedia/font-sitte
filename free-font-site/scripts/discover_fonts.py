#!/usr/bin/env python3
"""Discovery run: compare sources to catalog, write report, list new candidates."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

ROOT = SCRIPTS.parent
DISCOVERY = ROOT / "discovery"
REPORTS = DISCOVERY / "reports"
REGISTRY = DISCOVERY / "sources-registry.json"
CATALOG = ROOT / "data" / "output" / "catalog.json"


def load_catalog_slugs() -> set[str]:
    if not CATALOG.exists():
        return set()
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    from utils import slugify

    return {slugify(f["family_name"]) for f in data.get("fonts", [])}


def fetch_source_names(source_id: str) -> list[str]:
    """Return family names from raw cache if present."""
    raw_map = {
        "google-fonts": "google-fonts.json",
        "fontshare": "fontshare.json",
        "fontsource": "fontsource.json",
        "omnibus-type": "omnibus-type.json",
        "free-faces": "free-faces.json",
    }
    fname = raw_map.get(source_id)
    if not fname:
        return []
    path = ROOT / "data" / "raw" / fname
    if not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))
    if source_id == "google-fonts":
        return [f.get("family", "") for f in data.get("families", [])]
    if source_id == "fontshare":
        return [f.get("name", "") for f in data.get("fonts", [])]
    if source_id == "fontsource":
        return [f.get("family", "") for f in data.get("fonts", [])]
    if source_id == "omnibus-type":
        return [r.get("name", "").replace("-", " ") for r in data.get("repos", [])]
    if source_id == "free-faces":
        return [f.get("name", "") for f in data.get("fonts", [])]
    return []


def style_coverage() -> dict[str, int]:
    if not CATALOG.exists():
        return {}
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    counts: dict[str, int] = {}
    for f in data.get("fonts", []):
        for tag in f.get("style_tags") or []:
            counts[tag] = counts.get(tag, 0) + 1
    return counts


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)

    # Refresh free-faces scrape for discovery (no catalog merge)
    try:
        from sources import free_faces

        print("Scraping Free Faces gallery (candidates only)…")
        free_faces.fetch_raw()
    except Exception as exc:
        print(f"Free Faces scrape skipped: {exc}")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    catalog_slugs = load_catalog_slugs()
    from utils import slugify

    report = {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "catalog_family_count": len(catalog_slugs),
        "source_diffs": [],
        "style_coverage": style_coverage(),
        "policy": registry.get("policy"),
        "backlog_sources": registry.get("backlog_sources"),
    }

    for src in registry.get("sources", []):
        sid = src["id"]
        if not src.get("discovery", {}).get("enabled"):
            continue
        names = fetch_source_names(sid)
        missing = [n for n in names if n and slugify(n) not in catalog_slugs]
        report["source_diffs"].append({
            "source_id": sid,
            "source_name": src.get("name"),
            "legal_tier": src.get("legal_tier"),
            "auto_merge": src.get("auto_merge"),
            "raw_count": len(names),
            "not_in_catalog": len(missing),
            "sample_missing": missing[:15],
        })
        print(f"{sid}: {len(names)} raw, {len(missing)} not in catalog")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = REPORTS / f"{stamp}-discovery.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nReport written: {out}")


if __name__ == "__main__":
    main()
