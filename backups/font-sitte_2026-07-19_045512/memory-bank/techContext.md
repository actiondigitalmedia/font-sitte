# Tech Context

## Stack
| Layer | Technology |
|-------|------------|
| Aggregation | Python 3.12, requests, beautifulsoup4 |
| Data format | JSON (catalog), CSV (flat export), JSON Schema |
| Web UI | Vanilla HTML/CSS/JS (no build step) |
| Dev server | `python3 -m http.server 8080 --bind 0.0.0.0` |
| Version control | Git, branch `cursor/free-font-aggregation-43e3` |

## Dependencies
```
requests>=2.31.0
beautifulsoup4>=4.12.0
```

## External APIs / endpoints
| Source | Endpoint |
|--------|----------|
| Google Fonts | `https://fonts.google.com/metadata/fonts` |
| Fontshare | `https://api.fontshare.com/v2/fonts?offset=N&limit=100` |
| Font Squirrel | FontGet-Sources mirror on GitHub raw |
| Nerd Fonts | FontGet-Sources mirror on GitHub raw |
| Velvetyne | `https://api.github.com/orgs/velvetyne/repos` |
| League | `https://api.github.com/orgs/theleagueof/repos` |
| Usable Fonts | `https://raw.githubusercontent.com/menozero/usable-fonts/main/README.md` |
| Open Foundry | Scrape `https://open-foundry.com/fonts` (limited) |

## Key commands
```bash
# Full refresh
cd free-font-site
pip install -r requirements.txt
python3 scripts/aggregate.py

# Rebuild web-lite catalog after aggregate
python3 scripts/build_web_catalog.py

# Serve UI
python3 -m http.server 8080 --bind 0.0.0.0 --directory free-font-site
```

## Constraints
- No `.env` file created (user rule)
- Raw fetch cache gitignored to keep repo size manageable
- Full `catalog.json` ~3.8MB committed; `catalog-lite.json` ~1.9MB in web/
- Cursor browser requires HTTP server (not file://)

## Ports
- **8080** — font catalog UI (declared in environment.json)
- Avoid 26000–26999 (Cursor internal range)
