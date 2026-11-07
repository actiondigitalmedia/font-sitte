# Roadmap: font-sitte (updated 2026-07-19)

## Phase 1 — More verified libre fonts ✅ (partial)
- [x] Fontsource non-Google fonts (+120)
- [x] Omnibus Type GitHub (+29)
- [ ] Collletttivo (org not found on GitHub)
- [ ] UNCUT.wtf
- [ ] Free Faces curated scrape

**Catalog now: 2,136 families** (was 2,013)

## Phase 2 — SEO foundation ✅
- [x] Per-font specimen pages `/fonts/{id}/`
- [x] Category landing pages `/category/{category}/`
- [x] sitemap.xml + robots.txt
- [x] JSON-LD structured data on specimen pages
- [x] Open Graph + Twitter meta tags
- [x] Static site builder `scripts/build_site.py`

## Phase 3 — Monetization ✅ (scaffold)
- [x] Ad slot placeholders (header, sidebar, in-feed, footer, specimen)
- [x] ads.js config (set `enabled: true` + publisher ID when approved)
- [x] ads.txt template
- [x] privacy.html + cookie consent banner
- [ ] Live AdSense (needs publisher approval + slot IDs)

## Phase 4 — Deployment ✅ (scaffold)
- [x] GitHub Actions workflow `.github/workflows/deploy-pages.yml`
- [x] Weekly scheduled rebuild (Mondays 06:00 UTC)
- [x] `scripts/build_all.py` one-command pipeline
- [ ] Enable GitHub Pages in repo settings
- [ ] Custom domain

## Phase 5 — Growth features ✅ (partial)
- [x] Favorites (localStorage)
- [x] Similar fonts (same category)
- [x] Font pairing suggestions (category heuristics)
- [ ] Newsletter
- [ ] Submit-a-font form

## Build command
```bash
cd free-font-site
python3 scripts/build_all.py
python3 scripts/serve.py 8080
# http://localhost:8080/
```
