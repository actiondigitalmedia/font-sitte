#!/usr/bin/env python3
"""Full build pipeline: aggregate → catalog-lite → previews → static site."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def run(cmd: list[str]) -> None:
    print(f"\n→ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    fetch = "--no-fetch" not in sys.argv
    args = [] if fetch else ["--no-fetch"]

    run([sys.executable, str(SCRIPTS / "aggregate.py"), *args])
    run([sys.executable, str(SCRIPTS / "build_web_catalog.py")])
    run([sys.executable, str(SCRIPTS / "enrich_preview_urls.py")])
    run([sys.executable, str(SCRIPTS / "build_site.py")])
    if "--discover" in sys.argv:
        run([sys.executable, str(SCRIPTS / "discover_fonts.py")])
    print("\n✓ Build complete → free-font-site/dist/")


if __name__ == "__main__":
    main()
