# Active Context

## Current focus (2026-07-19)
Font catalog aggregation pipeline is **complete and working**. Browse UI is **live locally** and confirmed looking good by user.

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

## Next steps (not started)
- [ ] Public deployment (GitHub Pages, Netlify, Vercel)
- [ ] Weekly GitHub Action to refresh catalog
- [ ] Improve Open Foundry ingestion (SPA, only 1 family captured)
- [ ] Optional: DaFont/FontSpace with license parsing
- [ ] Font preview optimization (smaller catalog chunks)

## Active decisions
- Keep `data/raw/` gitignored — regenerate via aggregate.py
- Ship `catalog-lite.json` in web/ for UI (~1.9MB)
- Use Python http.server for dev preview (no build step)
- Port 8080 declared in `.cursor/environment.json`

## Known issues
- Open Foundry scrape only gets 1 family (client-rendered SPA)
- `catalog-lite.json` is ~1.9MB — acceptable but could be split
- Cursor port forwarding may remap 8080 if local port taken
