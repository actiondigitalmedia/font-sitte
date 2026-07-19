# Active Context

## Current focus (2026-07-19)
1. **Fixed font previews** — was using fake gstatic woff2 URLs; now loads via Google Fonts CSS API + Fontshare CSS API
2. User wants more verified OSS fonts + monetization (AdSense, native ads) + SEO as near-future steps

See `memory-bank/roadmap.md` for full plan.

## Recent changes
1. Built aggregation pipeline from 7 sources
2. Created unified catalog (JSON, CSV, per-source slices, stats)
3. Built static browse UI at `free-font-site/web/`
4. Fixed Cursor browser preview issues:
   - Server bind `0.0.0.0:8080`
   - Same-origin `catalog-lite.json`
   - Fixed broken `app.js` syntax error (googleCssUrl)
   - Added `health.html` for port-forward verification
5. User confirmed UI "looking nice" via localhost

## How to run right now
```bash
cd free-font-site
python3 -m http.server 8080 --bind 0.0.0.0
# http://localhost:8080/health.html  — verify port forward
# http://localhost:8080/web/           — browse UI
```

Refresh catalog data:
```bash
pip install -r requirements.txt
python3 scripts/aggregate.py
python3 scripts/build_web_catalog.py
```

## Next steps (prioritized)
- [ ] User verify font previews look distinct (hard refresh /web/)
- [ ] Add more verified libre sources (Fontsource, Omnibus, Collletttivo)
- [ ] SEO: per-font pages, sitemap, structured data
- [ ] Monetization: AdSense + native ad slots
- [ ] Public deployment (GitHub Pages / Netlify)

## Active decisions
- Keep `data/raw/` gitignored — regenerate via aggregate.py
- Ship `catalog-lite.json` in web/ for UI (~1.9MB)
- Use Python http.server for dev preview (no build step)
- Port 8080 declared in `.cursor/environment.json`

## Known issues
- Open Foundry scrape only gets 1 family (client-rendered SPA)
- `catalog-lite.json` is ~1.9MB — acceptable but could be split
- Cursor port forwarding may remap 8080 if local port taken
