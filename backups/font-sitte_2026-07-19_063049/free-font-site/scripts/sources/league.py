"""Fetch The League of Moveable Type fonts from their GitHub org."""

from __future__ import annotations

from typing import Any

import requests

from utils import RAW_DIR, now_iso, save_json, slugify

LEAGUE_API = "https://api.github.com/orgs/theleagueof/repos"


def fetch_raw() -> dict[str, Any]:
    resp = requests.get(
        LEAGUE_API,
        params={"per_page": 100, "type": "public"},
        headers={"Accept": "application/vnd.github+json"},
        timeout=60,
    )
    resp.raise_for_status()
    repos = resp.json()

    payload = {
        "fetched_at": now_iso(),
        "source": "league-of-moveable-type",
        "url": "https://www.theleagueofmoveabletype.com",
        "family_count": len(repos),
        "repos": repos,
    }
    save_json(RAW_DIR / "league.json", payload)
    return payload


def to_catalog_entries(raw: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    if raw is None:
        from utils import load_json

        raw = load_json(RAW_DIR / "league.json")

    entries: list[dict[str, Any]] = []
    for repo in raw.get("repos", []):
        repo_name = repo.get("name", "")
        # League repos are often named like "league-gothic" or "chunk"
        family_name = repo_name.replace("-", " ").replace("league ", "League ").title()
        slug = slugify(repo_name)

        entries.append({
            "id": f"league-{slug}",
            "family_name": family_name,
            "license_type": "OFL",
            "license_url": "https://openfontlicense.org",
            "commercial_use": True,
            "source": "league-of-moveable-type",
            "source_url": f"https://www.theleagueofmoveabletype.com/{repo_name}",
            "foundry": "The League of Moveable Type",
            "designers": [],
            "category": "display",
            "subsets": ["latin"],
            "tags": ["classic", "open-source", "league"],
            "featured": True,
            "featured_lists": ["league"],
            "variable": False,
            "axes": [],
            "popularity": repo.get("stargazers_count"),
            "date_added": None,
            "last_modified": repo.get("updated_at"),
            "preview_text": repo.get("description") or "Open-source font from The League",
            "download_url": repo.get("clone_url"),
            "github_url": repo.get("html_url"),
            "variants": [{"name": "Regular", "weight": 400, "style": "normal", "files": {}}],
        })

    return entries


if __name__ == "__main__":
    raw_data = fetch_raw()
    entries = to_catalog_entries(raw_data)
    print(f"League: {len(entries)} families")
