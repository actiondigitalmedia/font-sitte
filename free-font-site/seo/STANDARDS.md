# Python + Jinja2 SEO standards — can we match Astro/Eleventy?

**Yes.** Search engines rank HTML, schema, links, and CWV — not the generator brand.

## What we ship (meets / exceeds typical “top SEO” checklists)

| Standard | Implementation |
|----------|----------------|
| Indexable entity URLs | `/fonts/{slug}/` static HTML (2,000+) |
| Unique title + meta | Jinja templates, ≤60 / ≤155 patterns |
| Canonical | Absolute `SITE_URL` + `BASE_PATH` aware assets |
| Open Graph / Twitter | All entity + hub pages |
| JSON-LD entity | `CreativeWork` + `SoftwareApplication` + `Offer` price 0 |
| Breadcrumbs | Visible nav + `BreadcrumbList` |
| FAQ rich result fodder | FAQ section + `FAQPage` schema |
| Hub IA | category, source, license, tags, use-case |
| Money page | `/commercial-use/` |
| Sitemap index | `sitemap.xml` → hubs + fonts |
| robots.txt | Allow + sitemap pointer |
| Internal links | category/source/license/tags + similar + pairings |
| Orphan resistance | Every font linked from ≥1 category + source + similar module |
| Crawl budget | Tags only if ≥5 fonts; hub lists capped |
| Privacy | `/privacy.html` |
| ads.txt | Placeholder for AdSense |
| GH Pages base path | `/font-sitte/...` asset prefix from `SITE_URL` |

## Commands

```bash
cd free-font-site
pip install -r requirements.txt
# catalog-lite.json already present, or:
# python3 scripts/build_web_catalog.py
python3 scripts/build_site.py
python3 scripts/verify_seo.py
python3 scripts/serve.py 8080   # serves dist/
```

Env:

- `SITE_URL` (default `https://actiondigitalmedia.github.io/font-sitte`)
- `SITE_NAME`
- `ADSENSE_PUB_ID`
- `SEO_HUB_LIMIT` / `SEO_COMMERCIAL_LIMIT`

## Still later (not generator-limited)

- GSC CTR repair loop
- Real AdSense pub id
- Custom domain
- CWV tuning on browse UI JS bundle size
- Unique hub intros beyond `seo/content/hub_intros.json`
