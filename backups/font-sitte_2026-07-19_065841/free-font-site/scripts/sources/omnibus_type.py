"""Import Omnibus Type libre fonts from GitHub."""

from __future__ import annotations

from typing import Any

import requests

from utils import RAW_DIR, now_iso, save_json, slugify

OMNIBUS_API = "https://api.github.com/users/omnibus-type/repos"


def fetch_raw() -> dict[str, Any]:
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        resp = requests.get(
            OMNIBUS_API,
            params={"per_page": 100, "page": page, "type": "public"},
            headers={"Accept": "application/vnd.github+json"},
            timeout=60,
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    payload = {
        "fetched_at": now_iso(),
        "source": "omnibus-type",
        "url": "https://www.omnibus-type.com",
        "family_count": len(repos),
        "repos": repos,
    }
    save_json(RAW_DIR / "omnibus-type.json", payload)
    return payload


def to_catalog_entries(raw: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    if raw is None:
        from utils import load_json

        raw = load_json(RAW_DIR / "omnibus-type.json")

    entries: list[dict[str, Any]] = []
    for repo in raw.get("repos", []):
        repo_name = repo.get("name", "")
        if repo_name.lower() in ("website", "docs", ".github"):
            continue

        family_name = repo_name.replace("_", " ").replace("-", " ")
        slug = slugify(repo_name)

        entries.append({
            "id": f"omnibus-{slug}",
            "family_name": family_name,
            "license_type": "OFL",
            "license_url": "https://openfontlicense.org",
            "commercial_use": True,
            "source": "omnibus-type",
            "source_url": repo.get("html_url"),
            "foundry": "Omnibus Type",
            "designers": [],
            "category": "sans-serif",
            "subsets": ["latin", "latin-ext"],
            "tags": ["omnibus-type", "libre", "brand-grade"],
            "featured": True,
            "featured_lists": ["omnibus-type"],
            "variable": "variable" in (repo.get("description") or "").lower(),
            "axes": [],
            "popularity": repo.get("stargazers_count"),
            "date_added": None,
            "last_modified": repo.get("updated_at"),
            "preview_text": repo.get("description") or "Open-source font from Omnibus Type",
            "download_url": repo.get("clone_url"),
            "github_url": repo.get("html_url"),
            "variants": [{"name": "Regular", "weight": 400, "style": "normal", "files": {}}],
        })

    return entries


if __name__ == "__main__":
    raw_data = fetch_raw()
    entries = to_catalog_entries(raw_data)
    print(f"Omnibus Type: {len(entries)} families")
