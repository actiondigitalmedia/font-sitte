# Project Brief: font-sitte (Free Font Site)

## Project name
**font-sitte** — Free/libre font catalog aggregation + browse website

## Repository
- GitHub: `github.com/actiondigitalmedia/font-sitte`
- Active branch: `cursor/free-font-aggregation-43e3`
- PR: #1 — libre font aggregation pipeline + browse UI

## Core goal
Aggregate a large catalog of **commercial-safe libre/open-source fonts** from major sources and provide a browsable website for discovery, preview, and download linking.

## Scope decisions (locked in)
| Decision | Choice |
|----------|--------|
| License boundary | Libre / commercial-safe only (OFL, Apache, UFL, ITF FFL) |
| Hosting model | **Catalog + link out** — no font binary hosting in-repo |
| Initial sources | Google Fonts, Fontshare, Font Squirrel, Velvetyne, League, Nerd Fonts, Open Foundry |

## Success criteria
1. Reproducible aggregation pipeline (`scripts/aggregate.py`)
2. Unified JSON/CSV catalog with schema
3. Working browse UI with search, filters, live previews
4. Featured/curation tags (usable-fonts, Typewolf top picks)
5. Safe legal posture — license fields on every family

## Out of scope (for now)
- DaFont / FontSpace (mixed licenses, per-font parsing needed)
- Hosting font binaries in-repo
- User accounts, uploads, or font subsetting tools
- Public deployment (local/Cursor preview only so far)

## Project folder
All work lives in `/workspace/free-font-site/` — separate from other projects.
