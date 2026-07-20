#!/usr/bin/env python3
"""Build SEO-first static site with Jinja2 (fonts, hubs, schema, sitemaps)."""

from __future__ import annotations

import json
import os
import re
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
DIST = ROOT / "dist"
SEO = ROOT / "seo"
TEMPLATES = SEO / "templates"
INTROS_PATH = SEO / "content" / "hub_intros.json"
CATALOG_LITE = WEB / "catalog-lite.json"

SITE_URL = os.environ.get("SITE_URL", "https://actiondigitalmedia.github.io/font-sitte").rstrip("/")
SITE_NAME = os.environ.get("SITE_NAME", "Free Font Catalog")
ADSENSE_PUB = os.environ.get("ADSENSE_PUB_ID", "pub-XXXXXXXXXXXXXXXX")
HUB_LIMIT = int(os.environ.get("SEO_HUB_LIMIT", "400"))
COMMERCIAL_FEATURED_LIMIT = int(os.environ.get("SEO_COMMERCIAL_LIMIT", "120"))

BASE_PATH = urlparse(SITE_URL).path.rstrip("/")  # "" or "/font-sitte"

PAIRING_MAP = {
    "sans-serif": ["serif", "display"],
    "serif": ["sans-serif", "display"],
    "display": ["sans-serif", "serif"],
    "handwriting": ["serif", "sans-serif"],
    "monospace": ["sans-serif"],
    "other": ["sans-serif", "serif"],
}

USE_CASE_RULES = {
    "logos": {"categories": {"display", "sans-serif"}, "prefer_featured": True},
    "websites": {"categories": {"sans-serif", "serif"}, "prefer_variable": True},
    "invitations": {"categories": {"handwriting", "display", "script"}},
    "coding": {"categories": {"monospace"}, "sources": {"nerd-fonts"}},
    "presentations": {"categories": {"sans-serif", "display"}},
}


def asset(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    if path == "/":
        return f"{BASE_PATH}/" if BASE_PATH else "/"
    return f"{BASE_PATH}{path}"


def slugify(value: str) -> str:
    value = (value or "unknown").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "unknown"


def license_slug(license_type: str) -> str:
    return slugify(license_type)


def tag_slug(tag: str) -> str:
    return slugify(tag)


def load_intros() -> dict:
    if INTROS_PATH.exists():
        return json.loads(INTROS_PATH.read_text(encoding="utf-8"))
    return {}


def sort_fonts(fonts: list[dict]) -> list[dict]:
    return sorted(
        fonts,
        key=lambda f: (
            0 if f.get("featured") else 1,
            0 if f.get("commercial_use") else 1,
            (f.get("family_name") or "").lower(),
        ),
    )


def best_for_blurb(font: dict) -> str:
    cat = (font.get("category") or "other").replace("-", " ")
    bits = [f"{font['family_name']} is a free {cat} typeface"]
    if font.get("commercial_use"):
        bits.append(f"released under {font.get('license_type', 'an open license')} for commercial-safe projects")
    else:
        bits.append(f"under {font.get('license_type', 'an open license')} — verify terms before commercial use")
    variants = font.get("variant_count") or len(font.get("variants") or [])
    if variants:
        bits.append(f"with {variants} style{'s' if variants != 1 else ''}")
    if font.get("variable"):
        bits.append("including variable-font axes")
    src = font.get("source") or "the original foundry"
    bits.append(f"Distributed via {src}")
    return ". ".join(bits) + "."


def commercial_faq(font: dict) -> str:
    if font.get("commercial_use"):
        return (
            f"Yes — our catalog marks {font['family_name']} as commercial-use safe under "
            f"{font.get('license_type', 'its libre license')}. Always keep the license file with redistributions."
        )
    return (
        f"Check the {font.get('license_type', 'license')} terms before commercial use. "
        f"When in doubt, open the official license link on this page."
    )


def similar_fonts(font: dict, by_category: dict[str, list[dict]], limit: int = 8) -> list[dict]:
    pool = [f for f in by_category.get(font.get("category") or "other", []) if f["id"] != font["id"]]
    featured = [f for f in pool if f.get("featured")]
    rest = [f for f in pool if not f.get("featured")]
    # Prefer shared tags
    tags = set(font.get("tags") or [])
    if tags:
        rest.sort(key=lambda f: -len(tags.intersection(f.get("tags") or [])))
    return (featured + rest)[:limit]


def pairing_fonts(font: dict, by_category: dict[str, list[dict]], limit: int = 3) -> list[dict]:
    targets = PAIRING_MAP.get(font.get("category") or "other", ["sans-serif"])
    picks: list[dict] = []
    for cat in targets:
        candidates = [f for f in by_category.get(cat, []) if f["id"] != font["id"] and f.get("commercial_use")]
        candidates = sort_fonts(candidates)
        for c in candidates:
            if c["id"] not in {p["id"] for p in picks}:
                picks.append(c)
                break
        if len(picks) >= limit:
            break
    return picks[:limit]


def use_case_fonts(use: str, fonts: list[dict]) -> list[dict]:
    rules = USE_CASE_RULES[use]
    cats = rules.get("categories") or set()
    sources = rules.get("sources") or set()
    matched = []
    for f in fonts:
        if sources and f.get("source") in sources:
            matched.append(f)
            continue
        if f.get("category") in cats:
            matched.append(f)
    if rules.get("prefer_variable"):
        matched.sort(key=lambda f: (0 if f.get("variable") else 1, 0 if f.get("featured") else 1))
    elif rules.get("prefer_featured"):
        matched = sort_fonts(matched)
    else:
        matched = sort_fonts(matched)
    return matched


def font_json_ld(font: dict, canonical: str, description: str) -> dict:
    creators = font.get("designers") or []
    creator_name = ", ".join(creators) if creators else (font.get("foundry") or font.get("source") or "Unknown")
    return {
        "@context": "https://schema.org",
        "@type": ["CreativeWork", "SoftwareApplication"],
        "name": font["family_name"],
        "description": description,
        "url": canonical,
        "applicationCategory": "DesignApplication",
        "operatingSystem": "Windows, macOS, Linux",
        "isAccessibleForFree": True,
        "license": font.get("license_url") or font.get("license_type"),
        "creator": {"@type": "Organization", "name": creator_name},
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "url": font.get("download_url") or font.get("source_url") or canonical,
        },
    }


def breadcrumb_json_ld(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
            for i, (name, url) in enumerate(items)
        ],
    }


def faq_json_ld(font: dict, commercial_answer: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"Can I use {font['family_name']} commercially?",
                "acceptedAnswer": {"@type": "Answer", "text": commercial_answer},
            },
            {
                "@type": "Question",
                "name": f"Is {font['family_name']} free to download?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        f"Yes. This catalog links to the official {font.get('source')} distribution "
                        f"under {font.get('license_type')}."
                    ),
                },
            },
            {
                "@type": "Question",
                "name": f"Where do I get {font['family_name']} files?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Use the official download/use link on this page. We do not re-host font binaries.",
                },
            },
        ],
    }


def website_json_ld() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": f"{SITE_URL}/",
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{SITE_URL}/?q={{search_term_string}}",
            "query-input": "required name=search_term_string",
        },
    }


def make_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.filters["tojson"] = lambda v: Markup(json.dumps(v, ensure_ascii=False))
    env.globals["asset"] = asset
    env.globals["site_name"] = SITE_NAME
    return env


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_sitemaps(fonts: list[dict], hub_urls: list[str]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def urlset(entries: list[tuple[str, str, str]]) -> str:
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ]
        for loc, freq, priority in entries:
            lines.append("  <url>")
            lines.append(f"    <loc>{loc}</loc>")
            lines.append(f"    <lastmod>{now}</lastmod>")
            lines.append(f"    <changefreq>{freq}</changefreq>")
            lines.append(f"    <priority>{priority}</priority>")
            lines.append("  </url>")
        lines.append("</urlset>")
        return "\n".join(lines) + "\n"

    font_entries = [(f"{SITE_URL}/fonts/{f['id']}/", "monthly", "0.6") for f in fonts]
    hub_entries = [(f"{SITE_URL}/", "daily", "1.0")] + [(u, "weekly", "0.8") for u in hub_urls]

    write(DIST / "sitemap-fonts.xml", urlset(font_entries))
    write(DIST / "sitemap-hubs.xml", urlset(hub_entries))
    index = "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            "  <sitemap>",
            f"    <loc>{SITE_URL}/sitemap-hubs.xml</loc>",
            f"    <lastmod>{now}</lastmod>",
            "  </sitemap>",
            "  <sitemap>",
            f"    <loc>{SITE_URL}/sitemap-fonts.xml</loc>",
            f"    <lastmod>{now}</lastmod>",
            "  </sitemap>",
            "</sitemapindex>",
            "",
        ]
    )
    write(DIST / "sitemap.xml", index)
    # Convenience alias matching older builder expectations
    write(DIST / "sitemap-index.xml", index)


def inject_home_seo(index_html: str) -> str:
    """Ensure browse UI index has canonical, site base, and WebSite JSON-LD."""
    html = index_html
    # Always stamp the correct GitHub Pages / custom-domain base path
    html = re.sub(
        r'<script>window\.__SITE_BASE__=.*?</script>',
        f'<script>window.__SITE_BASE__={json.dumps(BASE_PATH)};</script>',
        html,
        count=1,
    )
    if 'rel="canonical"' not in html:
        snippet = f"""  <link rel="canonical" href="{SITE_URL}/" />
  <meta property="og:url" content="{SITE_URL}/" />
  <script type="application/ld+json">{json.dumps(website_json_ld(), ensure_ascii=False)}</script>
"""
        html = html.replace("</head>", snippet + "</head>", 1)
    return html


def main() -> None:
    if not CATALOG_LITE.exists():
        raise SystemExit("Run build_web_catalog.py first (missing web/catalog-lite.json)")
    if not TEMPLATES.exists():
        raise SystemExit(f"Missing templates at {TEMPLATES}")

    catalog = json.loads(CATALOG_LITE.read_text(encoding="utf-8"))
    fonts: list[dict] = catalog["fonts"]
    intros = load_intros()
    env = make_env()

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    for name in ["index.html", "app.js", "styles.css", "ads.js", "specimen.js", "catalog-lite.json"]:
        src = WEB / name
        if src.exists():
            if name == "index.html":
                write(DIST / name, inject_home_seo(src.read_text(encoding="utf-8")))
            else:
                shutil.copy2(src, DIST / name)

    # GSC HTML-file verification tokens (drop google*.html into web/)
    for google_file in sorted(WEB.glob("google*.html")):
        shutil.copy2(google_file, DIST / google_file.name)

    if (ROOT / "health.html").exists():
        shutil.copy2(ROOT / "health.html", DIST / "health.html")

    # Append SEO layout helpers to CSS if not present
    css_path = DIST / "styles.css"
    if css_path.exists():
        extra = (SEO / "seo-extra.css")
        if extra.exists():
            css_path.write_text(css_path.read_text(encoding="utf-8") + "\n" + extra.read_text(encoding="utf-8"), encoding="utf-8")

    by_category: dict[str, list[dict]] = defaultdict(list)
    by_source: dict[str, list[dict]] = defaultdict(list)
    by_license: dict[str, list[dict]] = defaultdict(list)
    by_tag: dict[str, list[dict]] = defaultdict(list)

    for font in fonts:
        by_category[font.get("category") or "other"].append(font)
        by_source[font.get("source") or "unknown"].append(font)
        by_license[license_slug(font.get("license_type") or "unknown")].append(font)
        for tag in font.get("tags") or []:
            by_tag[tag_slug(tag)].append(font)
        if font.get("variable"):
            by_tag["variable"].append(font)
        if font.get("featured"):
            by_tag["featured"].append(font)
        for fl in font.get("featured_lists") or []:
            by_tag[tag_slug(fl)].append(font)

    font_tmpl = env.get_template("font.html")
    hub_tmpl = env.get_template("hub.html")
    hub_index_tmpl = env.get_template("hub_index.html")
    commercial_tmpl = env.get_template("commercial_use.html")
    privacy_tmpl = env.get_template("privacy.html")

    hub_urls: list[str] = [
        f"{SITE_URL}/commercial-use/",
        f"{SITE_URL}/category/",
        f"{SITE_URL}/source/",
        f"{SITE_URL}/licenses/",
        f"{SITE_URL}/tags/",
        f"{SITE_URL}/use/",
        f"{SITE_URL}/privacy.html",
    ]

    # Font entity pages
    for font in fonts:
        path = f"/fonts/{font['id']}/"
        canonical = f"{SITE_URL}{path}"
        cat_label = (font.get("category") or "other").replace("-", " ")
        license_short = font.get("license_type") or "Open"
        variant_count = font.get("variant_count") or len(font.get("variants") or [])
        title = f"{font['family_name']}: Free {cat_label.title()} Font ({license_short})"
        if len(title) > 60:
            title = f"{font['family_name']}: Free {license_short} Font"
        commercial_label = "yes" if font.get("commercial_use") else "check license"
        description = (
            f"Download {font['family_name']} free. {cat_label} typeface with {variant_count} styles. "
            f"{license_short} license — commercial use {commercial_label}. Official {font.get('source')} link."
        )
        if len(description) > 155:
            description = description[:152] + "..."

        faq_answer = commercial_faq(font)
        similar = similar_fonts(font, by_category)
        pairings = pairing_fonts(font, by_category)
        variants = font.get("variants") or []
        variant_names = [v.get("name") or f"{v.get('weight')} {v.get('style')}" for v in variants[:12]]
        tags = [tag_slug(t) for t in (font.get("tags") or [])][:12]
        lic_slug = license_slug(font.get("license_type") or "unknown")

        json_ld = font_json_ld(font, canonical, description)
        crumbs = breadcrumb_json_ld(
            [
                ("Home", f"{SITE_URL}/"),
                (cat_label.title(), f"{SITE_URL}/category/{font.get('category') or 'other'}/"),
                (font["family_name"], canonical),
            ]
        )
        # Combine FAQ into second script via json_ld_extra as @graph companion
        extra = {"@context": "https://schema.org", "@graph": [crumbs, faq_json_ld(font, faq_answer)]}

        html = font_tmpl.render(
            title=title,
            description=description,
            canonical=canonical,
            og_type="article",
            json_ld=json_ld,
            json_ld_extra=extra,
            font=font,
            license_slug=lic_slug,
            variant_count=variant_count,
            variant_names=variant_names,
            tags=tags,
            similar=similar,
            pairings=pairings,
            best_for=best_for_blurb(font),
            commercial_faq=faq_answer,
        )
        write(DIST / "fonts" / font["id"] / "index.html", html)

    def render_hub(
        *,
        out: Path,
        path: str,
        h1: str,
        subtitle: str,
        intro: str,
        fonts_list: list[dict],
        sibling_hubs: list[dict] | None = None,
        breadcrumb_parent: dict | None = None,
    ) -> None:
        canonical = f"{SITE_URL}{path}"
        hub_urls.append(canonical)
        sorted_list = sort_fonts(fonts_list)
        title = h1 if len(h1) <= 60 else h1[:57] + "..."
        description = intro if len(intro) <= 155 else intro[:152] + "..."
        json_ld = breadcrumb_json_ld(
            [
                ("Home", f"{SITE_URL}/"),
                *([(breadcrumb_parent["label"], f"{SITE_URL}{breadcrumb_parent['path']}")] if breadcrumb_parent else []),
                (h1, canonical),
            ]
        )
        html = hub_tmpl.render(
            title=title,
            description=description,
            canonical=canonical,
            json_ld=json_ld,
            h1=h1,
            subtitle=subtitle,
            intro=intro,
            fonts=sorted_list,
            limit=HUB_LIMIT,
            sibling_hubs=sibling_hubs or [],
            breadcrumb_parent=breadcrumb_parent,
        )
        write(out, html)

    # Category hubs
    cat_siblings = [
        {"label": c.replace("-", " ").title(), "path": f"/category/{c}/"} for c in sorted(by_category)
    ]
    for cat, group in by_category.items():
        intro = (intros.get("category") or {}).get(cat) or (
            f"Browse free {cat.replace('-', ' ')} fonts verified for commercial use where licenses allow."
        )
        render_hub(
            out=DIST / "category" / cat / "index.html",
            path=f"/category/{cat}/",
            h1=f"Free {cat.replace('-', ' ').title()} Fonts for Commercial Use",
            subtitle=f"{len(group)} libre families",
            intro=intro,
            fonts_list=group,
            sibling_hubs=[s for s in cat_siblings if s["path"] != f"/category/{cat}/"][:8],
            breadcrumb_parent={"label": "Categories", "path": "/category/"},
        )

    write(
        DIST / "category" / "index.html",
        hub_index_tmpl.render(
            title="Font Categories — Free Commercial-Safe Fonts",
            description="Browse free libre fonts by category: sans-serif, serif, display, handwriting, monospace.",
            canonical=f"{SITE_URL}/category/",
            json_ld=website_json_ld(),
            items=[
                {"label": c.replace("-", " ").title(), "path": f"/category/{c}/", "count": len(g)}
                for c, g in sorted(by_category.items())
            ],
        ),
    )

    # Source hubs
    for source, group in by_source.items():
        render_hub(
            out=DIST / "source" / source / "index.html",
            path=f"/source/{source}/",
            h1=f"Free Fonts from {source.replace('-', ' ').title()}",
            subtitle=f"{len(group)} families via {source}",
            intro=f"Commercial-safe libre fonts aggregated from {source}. Preview here and open the official source for downloads.",
            fonts_list=group,
            breadcrumb_parent={"label": "Sources", "path": "/source/"},
        )
    write(
        DIST / "source" / "index.html",
        hub_index_tmpl.render(
            title="Font Sources — Free Font Catalog",
            description="Browse libre fonts by source: Google Fonts, Fontshare, and more.",
            canonical=f"{SITE_URL}/source/",
            items=[
                {"label": s.replace("-", " ").title(), "path": f"/source/{s}/", "count": len(g)}
                for s, g in sorted(by_source.items())
            ],
        ),
    )

    # License hubs
    for lic, group in by_license.items():
        label = (group[0].get("license_type") if group else lic) or lic
        render_hub(
            out=DIST / "licenses" / lic / "index.html",
            path=f"/licenses/{lic}/",
            h1=f"Free {label} Fonts",
            subtitle=f"{len(group)} families under {label}",
            intro=f"Fonts listed under the {label} license in our commercial-safe libre catalog.",
            fonts_list=group,
            breadcrumb_parent={"label": "Licenses", "path": "/licenses/"},
        )
    write(
        DIST / "licenses" / "index.html",
        hub_index_tmpl.render(
            title="Font Licenses — OFL and Open Source",
            description="Browse free fonts by license type, including OFL and Apache.",
            canonical=f"{SITE_URL}/licenses/",
            items=[
                {
                    "label": (g[0].get("license_type") if g else lic),
                    "path": f"/licenses/{lic}/",
                    "count": len(g),
                }
                for lic, g in sorted(by_license.items())
            ],
        ),
    )

    # Tag hubs (cap to avoid crawl bloat: only tags with >= 5 fonts)
    for tag, group in sorted(by_tag.items()):
        if len(group) < 5:
            continue
        render_hub(
            out=DIST / "tags" / tag / "index.html",
            path=f"/tags/{tag}/",
            h1=f"Free Fonts Tagged “{tag}”",
            subtitle=f"{len(group)} families",
            intro=f"Libre fonts tagged {tag} in the commercial-safe catalog.",
            fonts_list=group,
            breadcrumb_parent={"label": "Tags", "path": "/tags/"},
        )
    write(
        DIST / "tags" / "index.html",
        hub_index_tmpl.render(
            title="Font Tags — Free Font Catalog",
            description="Browse free commercial-safe fonts by tag.",
            canonical=f"{SITE_URL}/tags/",
            items=[
                {"label": t, "path": f"/tags/{t}/", "count": len(g)}
                for t, g in sorted(by_tag.items())
                if len(g) >= 5
            ],
        ),
    )

    # Use-case hubs
    for use in USE_CASE_RULES:
        group = use_case_fonts(use, fonts)
        intro = (intros.get("use") or {}).get(use) or f"Free fonts for {use}."
        render_hub(
            out=DIST / "use" / use / "index.html",
            path=f"/use/{use}/",
            h1=f"Free Fonts for {use.title()}",
            subtitle=f"{len(group)} matching families",
            intro=intro,
            fonts_list=group,
            sibling_hubs=[{"label": u.title(), "path": f"/use/{u}/"} for u in USE_CASE_RULES if u != use],
            breadcrumb_parent={"label": "Use cases", "path": "/use/"},
        )
    write(
        DIST / "use" / "index.html",
        hub_index_tmpl.render(
            title="Fonts by Use Case — Logos, Web, Coding",
            description="Free commercial-safe fonts organized by use case.",
            canonical=f"{SITE_URL}/use/",
            items=[
                {"label": u.title(), "path": f"/use/{u}/", "count": len(use_case_fonts(u, fonts))}
                for u in USE_CASE_RULES
            ],
        ),
    )

    # Commercial-use money page
    commercial = sort_fonts([f for f in fonts if f.get("commercial_use")])
    featured_commercial = [f for f in commercial if f.get("featured")][:COMMERCIAL_FEATURED_LIMIT]
    if len(featured_commercial) < 40:
        featured_commercial = commercial[:COMMERCIAL_FEATURED_LIMIT]
    write(
        DIST / "commercial-use" / "index.html",
        commercial_tmpl.render(
            title="Free Fonts for Commercial Use (OFL & Open Source)",
            description=(
                "Stop risking personal-use fonts. Explore commercial-safe libre fonts — "
                "OFL, Apache, and more — with clear licenses and live previews."
            ),
            canonical=f"{SITE_URL}/commercial-use/",
            json_ld=breadcrumb_json_ld([("Home", f"{SITE_URL}/"), ("Commercial use", f"{SITE_URL}/commercial-use/")]),
            intro=intros.get("commercial-use")
            or "Commercial-safe libre fonts with clear licenses and official download links.",
            fonts=featured_commercial,
            categories=sorted(by_category.keys()),
            use_cases=list(USE_CASE_RULES.keys()),
        ),
    )

    write(
        DIST / "privacy.html",
        privacy_tmpl.render(
            title=f"Privacy Policy — {SITE_NAME}",
            description=f"Privacy policy for {SITE_NAME}.",
            canonical=f"{SITE_URL}/privacy.html",
        ),
    )

    build_sitemaps(fonts, sorted(set(hub_urls)))
    write(
        DIST / "robots.txt",
        f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n",
    )
    write(DIST / "ads.txt", f"google.com, {ADSENSE_PUB}, DIRECT, f08c47fec0942fa0\n")

    # SEO build report for QA
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "site_url": SITE_URL,
        "base_path": BASE_PATH,
        "font_pages": len(fonts),
        "categories": len(by_category),
        "sources": len(by_source),
        "licenses": len(by_license),
        "tags_indexed": sum(1 for g in by_tag.values() if len(g) >= 5),
        "use_cases": len(USE_CASE_RULES),
        "commercial_featured": len(featured_commercial),
        "engine": "python-jinja2",
    }
    write(DIST / "seo-build-report.json", json.dumps(report, indent=2) + "\n")
    print(
        f"Built SEO site → {DIST} | fonts={report['font_pages']} "
        f"categories={report['categories']} sources={report['sources']} "
        f"licenses={report['licenses']} tags={report['tags_indexed']}"
    )


if __name__ == "__main__":
    main()
