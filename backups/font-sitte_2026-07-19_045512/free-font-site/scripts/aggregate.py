#!/usr/bin/env python3
"""Aggregate free/libre fonts from multiple sources into a unified catalog."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

# Allow running from repo root or scripts/
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from sources import (  # noqa: E402
    font_squirrel,
    fontshare,
    google_fonts,
    league,
    nerd_fonts,
    open_foundry,
    usable_fonts,
    velvetyne,
)
from utils import OUTPUT_DIR, RAW_DIR, as_tag_list, ensure_dirs, load_json, now_iso, save_json, slugify, write_csv_rows  # noqa: E402


SOURCE_ORDER = [
    "google-fonts",
    "fontshare",
    "velvetyne",
    "league-of-moveable-type",
    "open-foundry",
    "font-squirrel",
    "nerd-fonts",
]


def merge_catalogs(all_entries: list[dict], featured_map: dict[str, list[str]]) -> list[dict]:
    """Deduplicate by family name, preferring earlier sources in SOURCE_ORDER."""
    by_name: dict[str, dict] = {}
    source_rank = {s: i for i, s in enumerate(SOURCE_ORDER)}

    for entry in all_entries:
        key = slugify(entry["family_name"])
        lists = featured_map.get(key, [])
        if lists:
            entry["featured"] = True
            entry["featured_lists"] = sorted(set(entry.get("featured_lists", []) + lists))

        existing = by_name.get(key)
        if existing is None:
            by_name[key] = entry
            continue

        # Keep higher-priority source, merge metadata
        existing_rank = source_rank.get(existing["source"], 99)
        new_rank = source_rank.get(entry["source"], 99)
        if new_rank < existing_rank:
            merged = {**existing, **entry}
            merged["featured_lists"] = sorted(set(existing.get("featured_lists", []) + entry.get("featured_lists", [])))
            merged["featured"] = merged["featured"] or existing.get("featured") or entry.get("featured")
            merged["tags"] = sorted(set(as_tag_list(existing.get("tags")) + as_tag_list(entry.get("tags"))))
            by_name[key] = merged
        else:
            existing["featured_lists"] = sorted(set(existing.get("featured_lists", []) + entry.get("featured_lists", [])))
            existing["featured"] = existing.get("featured") or entry.get("featured")
            existing["tags"] = sorted(set(as_tag_list(existing.get("tags")) + as_tag_list(entry.get("tags"))))
            if not existing.get("download_url") and entry.get("download_url"):
                existing["download_url"] = entry["download_url"]

    return sorted(by_name.values(), key=lambda e: (not e.get("featured"), e.get("family_name", "").lower()))


def build_csv_rows(fonts: list[dict]) -> list[dict]:
    rows = []
    for f in fonts:
        rows.append({
            "id": f["id"],
            "family_name": f["family_name"],
            "source": f["source"],
            "license_type": f["license_type"],
            "commercial_use": f.get("commercial_use"),
            "category": f.get("category"),
            "featured": f.get("featured"),
            "featured_lists": "|".join(f.get("featured_lists") or []),
            "variable": f.get("variable"),
            "variant_count": len(f.get("variants") or []),
            "subsets": "|".join(f.get("subsets") or []),
            "tags": "|".join(f.get("tags") or []),
            "designers": "|".join(f.get("designers") or []),
            "source_url": f.get("source_url"),
            "download_url": f.get("download_url"),
            "github_url": f.get("github_url"),
        })
    return rows


def run(fetch: bool = True, libre_only: bool = True) -> dict:
    ensure_dirs()

    source_stats = []

    if fetch:
        print("Fetching Google Fonts...")
        google_raw = google_fonts.fetch_raw()
        print("Fetching Fontshare...")
        fontshare_raw = fontshare.fetch_raw()
        print("Fetching Usable Fonts curated list...")
        usable_raw = usable_fonts.fetch_raw()
        print("Fetching Velvetyne...")
        velvetyne_raw = velvetyne.fetch_raw()
        print("Fetching League of Moveable Type...")
        league_raw = league.fetch_raw()
        print("Fetching Open Foundry...")
        open_foundry_raw = open_foundry.fetch_raw()
        print("Fetching Font Squirrel (FontGet mirror)...")
        squirrel_raw = font_squirrel.fetch_raw()
        print("Fetching Nerd Fonts...")
        nerd_raw = nerd_fonts.fetch_raw()
    else:
        google_raw = load_json(RAW_DIR / "google-fonts.json")
        fontshare_raw = load_json(RAW_DIR / "fontshare.json")
        usable_raw = load_json(RAW_DIR / "usable-fonts.json")
        velvetyne_raw = load_json(RAW_DIR / "velvetyne.json")
        league_raw = load_json(RAW_DIR / "league.json")
        open_foundry_raw = load_json(RAW_DIR / "open-foundry.json")
        squirrel_raw = load_json(RAW_DIR / "font-squirrel.json")
        nerd_raw = load_json(RAW_DIR / "nerd-fonts.json")

    featured_map = usable_fonts.get_featured_map(usable_raw)

    all_entries: list[dict] = []
    source_entries = [
        ("google-fonts", google_fonts.to_catalog_entries(google_raw), google_raw),
        ("fontshare", fontshare.to_catalog_entries(fontshare_raw), fontshare_raw),
        ("velvetyne", velvetyne.to_catalog_entries(velvetyne_raw), velvetyne_raw),
        ("league-of-moveable-type", league.to_catalog_entries(league_raw), league_raw),
        ("open-foundry", open_foundry.to_catalog_entries(open_foundry_raw), open_foundry_raw),
        ("font-squirrel", font_squirrel.to_catalog_entries(squirrel_raw), squirrel_raw),
        ("nerd-fonts", nerd_fonts.to_catalog_entries(nerd_raw), nerd_raw),
    ]

    for source_id, entries, raw in source_entries:
        count = len(entries)
        source_stats.append({
            "id": source_id,
            "name": source_id.replace("-", " ").title(),
            "url": raw.get("url", ""),
            "family_count": count,
            "fetched_at": raw.get("fetched_at") or raw.get("_fetched_at") or now_iso(),
        })
        all_entries.extend(entries)
        print(f"  {source_id}: {count} families")

    merged = merge_catalogs(all_entries, featured_map)

    if libre_only:
        before = len(merged)
        merged = [f for f in merged if f.get("commercial_use")]
        print(f"Filtered to commercial-safe libre fonts: {len(merged)} (removed {before - len(merged)})")

    total_variants = sum(len(f.get("variants") or []) for f in merged)

    catalog = {
        "catalog_info": {
            "version": "1.0.0",
            "generated_at": now_iso(),
            "total_families": len(merged),
            "total_variants": total_variants,
            "license_policy": "libre-commercial-safe",
            "sources": source_stats,
        },
        "fonts": merged,
    }

    save_json(OUTPUT_DIR / "catalog.json", catalog)
    write_csv_rows(
        OUTPUT_DIR / "catalog.csv",
        build_csv_rows(merged),
        fieldnames=[
            "id", "family_name", "source", "license_type", "commercial_use",
            "category", "featured", "featured_lists", "variable", "variant_count",
            "subsets", "tags", "designers", "source_url", "download_url", "github_url",
        ],
    )

    # Per-source snapshots for the site
    by_source: dict[str, list] = {}
    for f in merged:
        by_source.setdefault(f["source"], []).append(f)
    for src, fonts in by_source.items():
        save_json(OUTPUT_DIR / f"by-source/{src}.json", {"source": src, "count": len(fonts), "fonts": fonts})

    categories: dict[str, int] = {}
    licenses: dict[str, int] = {}
    for f in merged:
        categories[f.get("category", "other")] = categories.get(f.get("category", "other"), 0) + 1
        licenses[f.get("license_type", "Unknown")] = licenses.get(f.get("license_type", "Unknown"), 0) + 1

    save_json(OUTPUT_DIR / "stats.json", {
        "generated_at": catalog["catalog_info"]["generated_at"],
        "total_families": len(merged),
        "total_variants": total_variants,
        "featured_count": sum(1 for f in merged if f.get("featured")),
        "license_policy": catalog["catalog_info"]["license_policy"],
        "categories": dict(sorted(categories.items(), key=lambda x: -x[1])),
        "top_licenses": dict(sorted(licenses.items(), key=lambda x: -x[1])[:15]),
        "sources": [{"id": s["id"], "families": s["family_count"]} for s in source_stats],
    })

    print(f"\nCatalog written: {len(merged)} families, {total_variants} variants")
    print(f"  JSON: {OUTPUT_DIR / 'catalog.json'}")
    print(f"  CSV:  {OUTPUT_DIR / 'catalog.csv'}")

    return catalog


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate free/libre font catalogs")
    parser.add_argument("--no-fetch", action="store_true", help="Use cached raw data only")
    parser.add_argument("--include-all-licenses", action="store_true", help="Include non-commercial fonts")
    args = parser.parse_args()

    run(fetch=not args.no_fetch, libre_only=not args.include_all_licenses)


if __name__ == "__main__":
    main()
