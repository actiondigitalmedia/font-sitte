#!/usr/bin/env python3
"""
Canonical entry point for CI and Cursor Cloud Agents.

Runs the full catalog + site pipeline, writes a short JSON summary for logs/agents,
and exits non-zero only on build failure (not when zero new fonts).
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SUMMARY_PATH = ROOT / "discovery" / "reports" / "latest-refresh-summary.json"


def main() -> None:
    discover = "--no-discover" not in sys.argv
    skip_fetch = "--no-fetch" in sys.argv

    cmd = [sys.executable, str(SCRIPTS / "build_all.py")]
    if skip_fetch:
        cmd.append("--no-fetch")
    if discover:
        cmd.append("--discover")

    print("→ scheduled_refresh:", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)

    catalog_path = ROOT / "data" / "output" / "catalog.json"
    stats_path = ROOT / "data" / "output" / "stats.json"
    summary: dict = {
        "finished_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "discover_ran": discover,
        "fetch_ran": not skip_fetch,
    }

    if catalog_path.exists():
        cat = json.loads(catalog_path.read_text(encoding="utf-8"))
        info = cat.get("catalog_info", {})
        summary["total_families"] = info.get("total_families")
        summary["total_variants"] = info.get("total_variants")
        summary["style_tag_counts"] = info.get("style_tag_counts", {})
        summary["generated_at"] = info.get("generated_at")

    if stats_path.exists():
        summary["stats"] = json.loads(stats_path.read_text(encoding="utf-8"))

    reports = sorted((ROOT / "discovery" / "reports").glob("*-discovery.json"))
    if reports:
        latest = json.loads(reports[-1].read_text(encoding="utf-8"))
        summary["discovery_report"] = str(reports[-1].relative_to(ROOT))
        summary["discovery_highlights"] = [
            {
                "source_id": d["source_id"],
                "not_in_catalog": d.get("not_in_catalog"),
                "sample_missing": (d.get("sample_missing") or [])[:5],
            }
            for d in latest.get("source_diffs", [])
            if d.get("not_in_catalog")
        ]

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nSummary: {SUMMARY_PATH}")
    print(json.dumps({k: summary[k] for k in summary if k != "stats"}, indent=2))


if __name__ == "__main__":
    main()
