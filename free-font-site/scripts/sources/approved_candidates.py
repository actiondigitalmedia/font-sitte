"""Merge human-approved font candidates from discovery/approved-candidates.json."""

from __future__ import annotations

import json
from typing import Any

from utils import RAW_DIR, ROOT, now_iso, save_json, slugify

APPROVED = ROOT / "discovery" / "approved-candidates.json"


def fetch_raw() -> dict[str, Any]:
    data = json.loads(APPROVED.read_text(encoding="utf-8"))
    payload = {
        "fetched_at": now_iso(),
        "source": "approved-candidates",
        "url": str(APPROVED),
        "family_count": len(data.get("candidates", [])),
        "candidates": data.get("candidates", []),
    }
    save_json(RAW_DIR / "approved-candidates.json", payload)
    return payload


def to_catalog_entries(raw: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    if raw is None:
        from utils import load_json

        raw = load_json(RAW_DIR / "approved-candidates.json")

    entries: list[dict[str, Any]] = []
    for c in raw.get("candidates", []):
        name = (c.get("family_name") or "").strip()
        if not name:
            continue
        if not c.get("commercial_use", True):
            continue

        slug = slugify(name)
        entries.append({
            "id": f"approved-{slug}",
            "family_name": name,
            "license_type": c.get("license_type", "OFL"),
            "license_url": c.get("license_url"),
            "commercial_use": True,
            "source": "approved-candidates",
            "source_url": c.get("source_url"),
            "foundry": c.get("foundry") or "Approved candidate",
            "designers": c.get("designers") or [],
            "category": c.get("category", "display"),
            "subsets": c.get("subsets") or ["latin"],
            "tags": ["approved", "discovery-op"] + (c.get("style_tags") or []),
            "style_tags": c.get("style_tags") or [],
            "featured": c.get("featured", False),
            "featured_lists": c.get("featured_lists") or ["discovery-approved"],
            "variable": c.get("variable", False),
            "axes": [],
            "popularity": None,
            "date_added": c.get("verified_at"),
            "last_modified": c.get("verified_at"),
            "preview_text": c.get("preview_text") or "The quick brown fox jumps over the lazy dog",
            "download_url": c.get("download_url"),
            "github_url": c.get("github_url"),
            "variants": c.get("variants") or [{"name": "Regular", "weight": 400, "style": "normal", "files": {}}],
        })

    return entries
