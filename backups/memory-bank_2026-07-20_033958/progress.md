# Progress

## What works
- [x] Font catalog pipeline + browse UI (~2136 families on this branch)
- [x] SEO strategy plans in `seo-stack/`
- [x] **Python/Jinja2 SEO builder** (`scripts/build_site.py` + `seo/templates/`)
- [x] Entity pages, hubs, commercial-use, schema, sitemap index
- [x] `verify_seo.py` acceptance checks — PASS

## What's left
- [ ] Deploy via GitHub Pages / custom domain
- [ ] GSC property + CTR repair workflow
- [ ] Real AdSense pub id
- [ ] DataForSEO/OpenSEO when public

## Last verify
2026-07-20 — `python3 scripts/build_site.py && python3 scripts/verify_seo.py` → OK (2136 fonts)
