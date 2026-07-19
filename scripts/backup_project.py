#!/usr/bin/env python3
"""Create a dated snapshot backup of font-sitte project + memory bank."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUPS_DIR = ROOT / "backups"
PROJECT_DIR = ROOT / "free-font-site"
MEMORY_DIR = ROOT / "memory-bank"


def main() -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    dest = BACKUPS_DIR / f"font-sitte_{stamp}"
    dest.mkdir(parents=True, exist_ok=False)

    # Copy project (exclude raw cache and pycache)
    def ignore(dirpath: str, names: list[str]) -> set[str]:
        ignored = set()
        for name in names:
            if name in {"__pycache__", ".pytest_cache"}:
                ignored.add(name)
            if name == "raw" and Path(dirpath).name == "data":
                ignored.add(name)
        return ignored

    shutil.copytree(PROJECT_DIR, dest / "free-font-site", ignore=ignore)
    shutil.copytree(MEMORY_DIR, dest / "memory-bank")

    manifest = {
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "project": "font-sitte",
        "branch": "cursor/free-font-aggregation-43e3",
        "contents": [
            "free-font-site/ (excluding data/raw/)",
            "memory-bank/",
        ],
        "restore_hint": "Copy free-font-site/ and memory-bank/ back to repo root",
    }
    (dest / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Also maintain a 'latest' symlink-like copy name via manifest pointer
    latest_file = BACKUPS_DIR / "LATEST.txt"
    latest_file.write_text(str(dest.name) + "\n", encoding="utf-8")

    print(f"Backup created: {dest}")
    print(f"Latest pointer: {latest_file}")


if __name__ == "__main__":
    main()
