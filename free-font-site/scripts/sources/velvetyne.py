"""Fetch Velvetyne Type Foundry libre fonts from GitHub."""

from __future__ import annotations

from typing import Any

import requests

from utils import RAW_DIR, now_iso, save_json, slugify

VTF_API = "https://api.github.com/orgs/velvetyne/repos"
PER_PAGE = 100


def fetch_raw() -> dict[str, Any]:
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        resp = requests.get(
            VTF_API,
            params={"per_page": PER_PAGE, "page": page, "type": "public"},
            headers={"Accept": "application/vnd.github+json"},
            timeout=60,
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < PER_PAGE:
            break
        page += 1

    payload = {
        "fetched_at": now_iso(),
        "source": "velvetyne",
        "url": "https://velvetyne.fr",
        "family_count": len(repos),
        "repos": repos,
    }
    save_json(RAW_DIR / "velvetyne.json", payload)
    return payload


def to_catalog_entries(raw: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    if raw is None:
        from utils import load_json

        raw = load_json(RAW_DIR / "velvetyne.json")

    entries: list[dict[str, Any]] = []
    for repo in raw.get("repos", []):
        name = repo.get("name", "").replace("-", " ").title()
        slug = slugify(repo.get("name", ""))
        if not slug:
            continue

        entries.append({
            "id": f"velvetyne-{slug}",
            "family_name": name,
            "license_type": "OFL",
            "license_url": "https://openfontlicense.org",
            "commercial_use": True,
            "source": "velvetyne",
            "source_url": repo.get("html_url"),
            "foundry": "Velvetyne Type Foundry",
            "designers": [],
            "category": "display",
            "subsets": ["latin"],
            "tags": ["experimental", "contemporary", "libre"],
            "featured": True,
            "featured_lists": ["velvetyne"],
            "variable": False,
            "axes": [],
            "popularity": repo.get("stargazers_count"),
            "date_added": None,
            "last_modified": repo.get("updated_at"),
            "preview_text": repo.get("description") or "Libre typeface from Velvetyne",
            "download_url": repo.get("clone_url"),
            "github_url": repo.get("html_url"),
            "variants": [{"name": "Regular", "weight": 400, "style": "normal", "files": {}}],
        })

    return entries


if __name__ == "__main__":
    raw_data = fetch_raw()
    entries = to_catalog_entries(raw_data)
    print(f"Velvetyne: {len(entries)} families")
