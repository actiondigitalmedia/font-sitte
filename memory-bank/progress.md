# Progress

## Working
- 2,136 commercial-safe font families aggregated (9 sources + approved-candidates hook)
- 2,061 live previews (woff2 enrichment + localhost proxy)
- Static site: specimen pages, categories, sitemap, ads scaffold, GitHub Pages workflow
- Browse UI: search, filters (category, source, **style**), favorites, pairings, similar
- **Font discovery operation** documented and scripted (discover → approve → aggregate → style tags → build)

## Style tag coverage (auto, 2026-07-27)
| Tag | Families |
|-----|----------|
| brand-display | 544 |
| handwritten-script | 385 |
| slab-workhorse | 365 |
| monospace-dev | 145 |
| web-modern | 46 |
| pixel-retro | 30 |
| experimental | 24 |
| y2k-web | 7 |
| old-english | 7 |

## Discovery backlog (from 2026-07-27 report)
- Fontshare: 64 names not in merged catalog (dedupe investigation)
- Free Faces: 47 candidate names for human license review
- Extend raw adapters for velvetyne/league in `discover_fonts.py` for fuller diffs

## Known issues
- Open Foundry SPA still ~1 family
- MedievalSharp example in approved-candidates dedupes against Google Fonts (format demo only)
