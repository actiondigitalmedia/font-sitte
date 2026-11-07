# Font Discovery Operation

Ongoing process to find **new libre fonts** we can **legally offer** on the site, classify them (Old English, pixel, web-modern, etc.), and merge them into the catalog.

**Full playbook:** [`docs/font-discovery-operation.md`](../docs/font-discovery-operation.md)

## Quick commands

```bash
cd free-font-site

# Weekly discovery run (diff sources vs catalog, write report)
python3 scripts/discover_fonts.py

# Apply style tags (old-english, pixel-retro, y2k-web, …) to catalog
python3 scripts/apply_style_tags.py

# Full rebuild after approving new candidates
python3 scripts/build_all.py
```

## Key files

| File | Purpose |
|------|---------|
| `discovery/sources-registry.json` | Trusted sources + legal policy per source |
| `discovery/style-taxonomy.json` | Auto-tag rules (Old English, Y2K, pixel, etc.) |
| `discovery/approved-candidates.json` | Human-verified fonts ready to merge |
| `discovery/reports/` | Generated discovery reports (gitignored) |

## Adding a verified font manually

1. Confirm license allows **commercial use** (OFL, Apache, MIT, ITF FFL, etc.).
2. Add an entry to `discovery/approved-candidates.json`.
3. Run `python3 scripts/build_all.py`.

Never add fonts with “personal use only” or unclear licenses.
