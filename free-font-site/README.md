# Free Font Site — Aggregated Catalog

A reproducible pipeline that aggregates **2,000+ commercial-safe libre fonts** from major open-source libraries into a unified JSON/CSV catalog ready for a font discovery website.

## What's included

| Source | Families | License policy |
|--------|----------|----------------|
| [Google Fonts](https://fonts.google.com) | 1,940 | OFL / Apache / UFL |
| [Fontshare](https://www.fontshare.com) | 100 | ITF Free Font License |
| [Font Squirrel](https://www.fontsquirrel.com) | 608 (608 merged, deduped) | Verified commercial-free |
| [Velvetyne](https://velvetyne.fr) | 22 | OFL |
| [The League of Moveable Type](https://www.theleagueofmoveabletype.com) | 20 | OFL |
| [Nerd Fonts](https://www.nerdfonts.com) | 67 | Mixed (base fonts are libre) |
| [Open Foundry](https://open-foundry.com) | 1* | OFL |

**Merged catalog (deduplicated, commercial-safe): 2,013 families · 7,875 variants**

\* Open Foundry is a client-rendered SPA; their catalog is partially captured. Re-run when they expose an API.

## Assumptions (your stated preferences)

- **License boundary:** Libre / open-source fonts safe for commercial use (OFL, Apache, UFL, ITF FFL, etc.)
- **Hosting model:** Catalog + download/source links (font binaries stay at origin; Google Fonts families link to `github.com/google/fonts`)
- **Featured tags:** Cross-referenced with [usable-fonts](https://github.com/menozero/usable-fonts) and Typewolf top picks

## Quick start

### Browse the catalog (UI)

```bash
cd free-font-site
python3 -m http.server 8080
# open http://localhost:8080/web/
```

The UI loads `data/output/catalog.json`, supports search/filter/sort, lazy-loads font previews, and opens a detail modal with download links.

### Refresh the catalog data

```bash
cd free-font-site
pip install -r requirements.txt
python3 scripts/aggregate.py
```

Outputs land in `data/output/`:

- `catalog.json` — full unified catalog (schema in `schema/font.schema.json`)
- `catalog.csv` — flat summary for spreadsheets / DB import
- `by-source/*.json` — per-source slices

### Options

```bash
python3 scripts/aggregate.py --no-fetch          # rebuild from cached raw data
python3 scripts/aggregate.py --include-all-licenses  # keep personal-use-only fonts
```

## Catalog schema (per family)

```json
{
  "id": "roboto",
  "family_name": "Roboto",
  "license_type": "OFL",
  "commercial_use": true,
  "source": "google-fonts",
  "source_url": "https://fonts.google.com/specimen/Roboto",
  "category": "sans-serif",
  "subsets": ["latin", "latin-ext", "cyrillic"],
  "featured": true,
  "featured_lists": ["usable-fonts", "typewolf-top"],
  "variable": true,
  "axes": [{"tag": "wght", "min": 100, "max": 900, "default": 400}],
  "variants": [
    {"name": "Regular", "weight": 400, "style": "normal", "files": {"woff2": "..."}}
  ],
  "download_url": "https://github.com/google/fonts/tree/main/ofl/roboto",
  "github_url": "https://github.com/google/fonts/tree/main/ofl/roboto"
}
```

## Site categories (suggested)

The catalog supports filtering by:

- **Category:** serif, sans-serif, slab-serif, monospace, display, handwriting, script
- **Featured:** usable-fonts, typewolf-top, fontshare, velvetyne, league
- **Variable fonts:** `variable: true`
- **Tags:** brand-grade, experimental, nerd-font, developer, etc.

## Legal notes

- Google Fonts, Velvetyne, League, and most Font Squirrel entries are explicitly libre.
- Fontshare fonts are free for personal **and** commercial use under ITF FFL.
- Nerd Fonts patch libre base fonts; license inherits from the underlying family.
- Always display license + attribution per family on your site. This repo provides `license_type` and `license_url` fields for that.

## Project layout

```
free-font-site/
├── schema/font.schema.json    # JSON Schema for catalog
├── scripts/
│   ├── aggregate.py           # Main orchestrator
│   ├── utils.py               # Normalization helpers
│   └── sources/               # Per-source fetch adapters
├── data/
│   ├── raw/                   # Cached API responses (gitignored)
│   └── output/                # catalog.json, catalog.csv, by-source/
└── requirements.txt
```

## Next steps for the website

1. Import `data/output/catalog.json` into your DB or load statically
2. Use `variants[].files.woff2` for live previews (Google Fonts / Fontshare CDN URLs)
3. Add a `/download` flow that links to `download_url` or bundles from Google Fonts GitHub
4. Schedule `aggregate.py` weekly (GitHub Action) to refresh the catalog
