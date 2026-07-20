# Active Context

## Current focus (2026-07-20)
**Python + Jinja2 SEO static site builder implemented** on `cursor/seo-strategy-plans-d92e`.

User confirmed: skip Astro/Eleventy; Python/Jinja2 is fine if it meets top SEO standards.

## Done this session
- Brought `free-font-site/` from catalog branch onto SEO branch
- Rewrote `scripts/build_site.py` to Jinja2 templates under `seo/templates/`
- Full IA: fonts, category/source/license/tags/use hubs, commercial-use, privacy
- JSON-LD: CreativeWork+SoftwareApplication, BreadcrumbList, FAQPage
- Sitemap index + robots.txt + verify_seo.py
- Build verified: **2136 font pages**, SEO VERIFY OK

## Next steps
1. Merge/deploy with Pages workflow (SITE_URL)
2. Custom domain + GSC
3. Optional: unique hub intros polish, CTR loop

## Active decisions
- **SSG = Python + Jinja2** (locked)
- Compose cheap APIs later; no Ahrefs/Semrush
- Catalog-driven uniqueness > bulk LLM pages
- `dist/` gitignored; generated in CI via `build_all.py` / `build_site.py`
