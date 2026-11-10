#!/usr/bin/env python3
"""Dated snapshot + tarball for font-sitte (reuse discovery pipeline on coupon sites)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUPS_DIR = ROOT / "backups"
PROJECT_DIR = ROOT / "free-font-site"
MEMORY_DIR = ROOT / "memory-bank"
CATALOG = PROJECT_DIR / "data" / "output" / "catalog.json"


def git_branch() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return os.environ.get("GITHUB_REF_NAME", "unknown")


def ignore(dirpath: str, names: list[str]) -> set[str]:
    ignored = set()
    for name in names:
        if name in {"__pycache__", ".pytest_cache", "dist", "node_modules"}:
            ignored.add(name)
        if name == "raw" and Path(dirpath).name == "data":
            ignored.add(name)
    return ignored


def main() -> None:
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    dest = BACKUPS_DIR / f"font-sitte_{stamp}"
    dest.mkdir(parents=True, exist_ok=False)

    shutil.copytree(PROJECT_DIR, dest / "free-font-site", ignore=ignore)
    shutil.copytree(MEMORY_DIR, dest / "memory-bank")
    shutil.copytree(PROJECT_DIR / "discovery", dest / "discovery-snapshot", ignore=shutil.ignore_patterns("reports"))

    family_count = None
    if CATALOG.exists():
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
        family_count = data.get("catalog_info", {}).get("total_families")
        shutil.copy2(CATALOG, dest / "catalog-snapshot.json")
        lite = PROJECT_DIR / "web" / "catalog-lite.json"
        if lite.exists():
            shutil.copy2(lite, dest / "catalog-lite-snapshot.json")

    manifest = {
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "project": "font-sitte",
        "branch": git_branch(),
        "total_families": family_count,
        "contents": [
            "free-font-site/ (no data/raw/, no dist/)",
            "memory-bank/",
            "discovery-snapshot/",
            "catalog-snapshot.json",
        ],
        "reuse": {
            "coupon_site": "Copy scripts/discover_fonts.py, discovery/sources-registry.json, scheduled_refresh pattern",
            "agents": "Use docs/cloud-agent-catalog-runbook.md as automation prompt template",
        },
        "restore_hint": "Unpack tarball; copy free-font-site/ and memory-bank/ to repo root; pip install -r requirements.txt; python3 scripts/scheduled_refresh.py",
    }
    (dest / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    tarball = BACKUPS_DIR / f"font-sitte_{stamp}.tar.gz"
    with tarfile.open(tarball, "w:gz") as tar:
        tar.add(dest, arcname=dest.name)

    latest_file = BACKUPS_DIR / "LATEST.txt"
    latest_file.write_text(f"{dest.name}\n{tarball.name}\n", encoding="utf-8")

    print(f"Backup folder: {dest}")
    print(f"Backup tarball: {tarball} ({tarball.stat().st_size:,} bytes)")
    print(f"Latest pointer: {latest_file}")
    if family_count:
        print(f"Catalog families snapshotted: {family_count}")


if __name__ == "__main__":
    main()
