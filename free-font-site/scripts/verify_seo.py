#!/usr/bin/env python3
"""Verify generated dist/ meets SEO acceptance checks."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "dist"
REQUIRED_IN_FONT = [
    'rel="canonical"',
    'name="description"',
    "application/ld+json",
    "BreadcrumbList",
    "FAQPage",
    "Commercial use",
    "Similar free fonts",
]


def main() -> int:
    report_path = DIST / "seo-build-report.json"
    if not report_path.exists():
        print("FAIL: missing seo-build-report.json — run build_site.py")
        return 1
    report = json.loads(report_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    if report.get("font_pages", 0) < 1000:
        errors.append(f"expected >=1000 font pages, got {report.get('font_pages')}")

    for rel in [
        "fonts/roboto/index.html",
        "commercial-use/index.html",
        "category/sans-serif/index.html",
        "licenses/ofl/index.html",
        "use/logos/index.html",
        "sitemap.xml",
        "sitemap-fonts.xml",
        "sitemap-hubs.xml",
        "robots.txt",
    ]:
        if not (DIST / rel).exists():
            errors.append(f"missing {rel}")

    sample = DIST / "fonts" / "roboto" / "index.html"
    if sample.exists():
        html = sample.read_text(encoding="utf-8")
        for needle in REQUIRED_IN_FONT:
            if needle not in html:
                errors.append(f"roboto page missing: {needle}")
        if not re.search(r"<title>[^<]+</title>", html):
            errors.append("roboto page missing title")
        # inbound-ish modules
        if html.count('href="') < 8:
            errors.append("roboto page looks under-linked")

    robots = (DIST / "robots.txt").read_text(encoding="utf-8") if (DIST / "robots.txt").exists() else ""
    if "Sitemap:" not in robots:
        errors.append("robots.txt missing Sitemap")

    if errors:
        print("SEO VERIFY FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("SEO VERIFY OK")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
