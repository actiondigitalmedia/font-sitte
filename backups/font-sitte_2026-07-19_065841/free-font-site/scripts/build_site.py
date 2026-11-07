#!/usr/bin/env python3
"""Build static site with SEO specimen pages, category pages, sitemap, ads.txt."""

from __future__ import annotations

import html
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
DIST = ROOT / "dist"
CATALOG_LITE = WEB / "catalog-lite.json"
SITE_URL = os.environ.get("SITE_URL", "https://actiondigitalmedia.github.io/font-sitte").rstrip("/")
ADSENSE_PUB = os.environ.get("ADSENSE_PUB_ID", "pub-XXXXXXXXXXXXXXXX")


def esc(text: str) -> str:
    return html.escape(str(text or ""))


def site_head(title: str, description: str, path: str, og_type: str = "website") -> str:
    url = f"{SITE_URL}{path}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <link rel="canonical" href="{esc(url)}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(description)}" />
  <meta property="og:url" content="{esc(url)}" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:site_name" content="Free Font Catalog" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(description)}" />
  <link rel="stylesheet" href="/styles.css" />
</head>"""


def font_json_ld(font: dict, url: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": font["family_name"],
        "applicationCategory": "DesignApplication",
        "operatingSystem": "Any",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "license": font.get("license_url") or font.get("license_type"),
        "url": url,
    }
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


def specimen_page(font: dict, similar: list[dict]) -> str:
    path = f"/fonts/{font['id']}/"
    url = f"{SITE_URL}{path}"
    title = f"{font['family_name']} — Free {font['license_type']} Font Download"
    desc = (
        f"Download {font['family_name']} free for commercial use. "
        f"{font['category']} · {font['license_type']} · {font.get('variant_count') or len(font.get('variants') or [])} styles."
    )
    links = []
    for label, key in [("Source", "source_url"), ("Download", "download_url"), ("GitHub", "github_url"), ("License", "license_url")]:
        if font.get(key):
            links.append(f'<a href="{esc(font[key])}" rel="noopener">{label}</a>')

    similar_html = "".join(
        f'<a class="chip" href="/fonts/{esc(s["id"])}/">{esc(s["family_name"])}</a>' for s in similar[:6]
    )

    return f"""{site_head(title, desc, path, "article")}
{font_json_ld(font, url)}
<body class="specimen-page">
  <header class="header"><div class="header-inner"><div class="brand"><a href="/" style="color:inherit;text-decoration:none"><h1>{esc(font['family_name'])}</h1></a><p class="subtitle">Free {esc(font['license_type'])} font · {esc(font['category'])}</p></div></div></header>
  <main class="specimen-main">
    <div class="ad-slot ad-leaderboard" data-ad-slot="specimen-top"></div>
    <p class="specimen-preview" id="specimen-preview" data-font-id="{esc(font['id'])}">{esc(font.get('preview_text') or 'The quick brown fox jumps over the lazy dog')}</p>
    <dl class="detail-grid">
      <div><dt>License</dt><dd>{esc(font['license_type'])}</dd></div>
      <div><dt>Source</dt><dd>{esc(font['source'])}</dd></div>
      <div><dt>Category</dt><dd>{esc(font['category'])}</dd></div>
      <div><dt>Styles</dt><dd>{font.get('variant_count') or len(font.get('variants') or [])}</dd></div>
    </dl>
    <div class="links">{''.join(links)} <a href="/">← Browse all fonts</a></div>
    <section><h2>Similar fonts</h2><div class="chips">{similar_html}</div></section>
  </main>
  <footer class="site-footer"><a href="/privacy.html">Privacy</a> · <a href="/">Catalog</a></footer>
  <script src="/specimen.js" defer></script>
  <script src="/ads.js" defer></script>
</body></html>"""


def category_page(category: str, fonts: list[dict]) -> str:
    path = f"/category/{category}/"
    title = f"Free {category.replace('-', ' ').title()} Fonts — Commercial Use"
    desc = f"Browse {len(fonts)} free libre {category} fonts safe for commercial use."
    items = "".join(
        f'<li><a href="/fonts/{esc(f["id"])}/">{esc(f["family_name"])}</a> <span class="meta">{esc(f["license_type"])}</span></li>'
        for f in fonts[:500]
    )
    return f"""{site_head(title, desc, path)}
<body>
  <header class="header"><div class="header-inner"><div class="brand"><h1>{esc(category.replace('-', ' ').title())} Fonts</h1><p class="subtitle">{len(fonts)} free commercial-safe families</p></div></div></header>
  <main class="specimen-main"><ul class="category-list">{items}</ul><p><a href="/">← All fonts</a></p></main>
  <script src="/ads.js" defer></script>
</body></html>"""


def privacy_page() -> str:
    return f"""{site_head("Privacy Policy — Free Font Catalog", "Privacy policy for Free Font Catalog.", "/privacy.html")}
<body>
  <main class="specimen-main">
    <h1>Privacy Policy</h1>
    <p>Free Font Catalog aggregates publicly available libre font metadata. We use cookies for analytics and advertising (Google AdSense) when enabled.</p>
    <h2>Advertising</h2>
    <p>Third-party vendors, including Google, use cookies to serve ads based on prior visits. You may opt out of personalized advertising in your Google account settings.</p>
    <h2>Fonts</h2>
    <p>Font files are served from original sources (Google Fonts, Fontshare, etc.). We do not claim ownership of typefaces. See each font's license page.</p>
    <h2>Contact</h2>
    <p>Repository: <a href="https://github.com/actiondigitalmedia/font-sitte">github.com/actiondigitalmedia/font-sitte</a></p>
    <p><a href="/">← Back to catalog</a></p>
  </main>
</body></html>"""


def build_sitemap(fonts: list[dict], categories: list[str]) -> str:
    urls = [f"  <url><loc>{SITE_URL}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>"]
    for cat in categories:
        urls.append(f"  <url><loc>{SITE_URL}/category/{cat}/</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>")
    for font in fonts:
        urls.append(f"  <url><loc>{SITE_URL}/fonts/{font['id']}/</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>")
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>"


def main() -> None:
    if not CATALOG_LITE.exists():
        raise SystemExit("Run build_web_catalog.py first")

    catalog = json.loads(CATALOG_LITE.read_text(encoding="utf-8"))
    fonts: list[dict] = catalog["fonts"]

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    # Copy main UI assets to dist root
    for name in ["index.html", "app.js", "styles.css", "ads.js", "specimen.js", "catalog-lite.json"]:
        src = WEB / name
        if src.exists():
            shutil.copy2(src, DIST / name)

    shutil.copy2(ROOT / "health.html", DIST / "health.html")

    # Specimen pages
    by_category: dict[str, list] = {}
    font_dir = DIST / "fonts"
    font_dir.mkdir()
    for font in fonts:
        by_category.setdefault(font.get("category", "other"), []).append(font)
        similar = [f for f in fonts if f["id"] != font["id"] and f.get("category") == font.get("category")][:6]
        out = font_dir / font["id"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(specimen_page(font, similar), encoding="utf-8")

    # Category pages
    cat_dir = DIST / "category"
    cat_dir.mkdir()
    categories = sorted(by_category.keys())
    for cat in categories:
        (cat_dir / cat / "index.html").parent.mkdir(parents=True, exist_ok=True)
        (cat_dir / cat / "index.html").write_text(category_page(cat, by_category[cat]), encoding="utf-8")

    (DIST / "privacy.html").write_text(privacy_page(), encoding="utf-8")
    (DIST / "sitemap.xml").write_text(build_sitemap(fonts, categories), encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    (DIST / "ads.txt").write_text(f"google.com, {ADSENSE_PUB}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")

    print(f"Built static site: {len(fonts)} specimen pages, {len(categories)} categories → {DIST}")


if __name__ == "__main__":
    main()
