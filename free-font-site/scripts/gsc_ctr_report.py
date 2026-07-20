#!/usr/bin/env python3
"""
GSC CTR repair from a Search Console export CSV (no API keys required).

Export path (GSC UI):
  Performance → Search results → Pages (or Queries) → Export → CSV
  Or: Download → Pages.csv from the performance report.

Usage:
  python3 scripts/gsc_ctr_report.py path/to/Pages.csv
  python3 scripts/gsc_ctr_report.py path/to/Pages.csv --min-impressions 100 --max-ctr 0.02

Outputs:
  seo-stack/data/ctr-repair.csv (proposals)
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "seo-stack" / "data" / "ctr-repair.csv"


def parse_pct(value: str) -> float:
    raw = (value or "").strip().replace(",", "")
    if not raw:
        return 0.0
    had_pct = "%" in raw
    num = float(raw.replace("%", "").strip())
    # GSC UI export uses "0.80%" ; API-style dumps may use 0.008
    if had_pct or num > 1.0:
        return num / 100.0
    return num


def parse_num(value: str) -> float:
    return float((value or "0").strip().replace(",", "") or 0)


def slug_from_url(url: str) -> str | None:
    path = urlparse(url).path.rstrip("/")
    m = re.search(r"/fonts/([^/]+)$", path)
    return m.group(1) if m else None


def propose_title(url: str, top_hint: str = "") -> str:
    path = urlparse(url).path.rstrip("/")
    slug = slug_from_url(url)
    if path.endswith("/commercial-use") or path.endswith("commercial-use"):
        return "Free Fonts for Commercial Use (OFL & Open Source)"
    name = (slug or "Font").replace("-", " ").title()
    if "commercial" in (top_hint or "").lower():
        return f"{name}: Free Font for Commercial Use (OFL)"
    if "download" in (top_hint or "").lower():
        return f"Download {name} Font Free — OFL License"
    return f"{name}: Free Font Download (Commercial-Safe)"


def propose_meta(url: str) -> str:
    slug = slug_from_url(url)
    name = (slug or "This font").replace("-", " ").title()
    return (
        f"Download {name} free. Libre/open-source typeface with clear commercial-use licensing. "
        f"Preview styles and open the official source."
    )[:155]


def find_columns(fieldnames: list[str]) -> dict[str, str]:
    lower = {f.lower(): f for f in fieldnames}

    def pick(*names: str) -> str:
        for n in names:
            if n in lower:
                return lower[n]
        raise KeyError(names[0])

    return {
        "url": pick("top pages", "page", "landing page", "url", "pages"),
        "clicks": pick("clicks"),
        "impr": pick("impressions", "impr"),
        "ctr": pick("ctr"),
        "pos": pick("position", "avg. position", "average position"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Propose title/meta fixes for low-CTR GSC pages")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--min-impressions", type=float, default=100.0)
    parser.add_argument("--max-ctr", type=float, default=0.02)
    parser.add_argument("--min-position", type=float, default=3.0)
    parser.add_argument("--max-position", type=float, default=20.0)
    args = parser.parse_args()

    if not args.csv_path.exists():
        print(f"Missing CSV: {args.csv_path}", file=sys.stderr)
        return 1

    with args.csv_path.open(encoding="utf-8-sig", newline="") as fh:
        # Skip comment lines so hand-authored samples stay readable
        filtered = (line for line in fh if line.strip() and not line.lstrip().startswith("#"))
        reader = csv.DictReader(filtered)
        if not reader.fieldnames:
            print("Empty CSV", file=sys.stderr)
            return 1
        cols = find_columns(list(reader.fieldnames))
        rows_out = []
        for row in reader:
            url = (row.get(cols["url"]) or "").strip()
            if not url:
                continue
            impressions = parse_num(row.get(cols["impr"], "0"))
            ctr = parse_pct(row.get(cols["ctr"], "0"))
            position = parse_num(row.get(cols["pos"], "0"))
            clicks = parse_num(row.get(cols["clicks"], "0"))
            if impressions < args.min_impressions:
                continue
            if ctr >= args.max_ctr:
                continue
            if position and (position < args.min_position or position > args.max_position):
                continue
            rows_out.append(
                {
                    "url": url,
                    "clicks": int(clicks),
                    "impressions": int(impressions),
                    "ctr": round(ctr, 4),
                    "position": round(position, 2),
                    "title_proposed": propose_title(url),
                    "meta_proposed": propose_meta(url),
                }
            )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "url",
                "clicks",
                "impressions",
                "ctr",
                "position",
                "title_proposed",
                "meta_proposed",
            ],
        )
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Wrote {len(rows_out)} CTR repair candidates → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
