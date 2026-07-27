# Product Context

## Why this exists
Designers and developers need one place to discover **legitimately free, commercial-safe fonts** without wading through mixed-license portals like DaFont.

## Problems it solves
- Scattered libre font sources (Google Fonts, Fontshare, foundries, etc.)
- No single searchable catalog with consistent metadata
- Hard to know which "free" fonts are actually OK for commercial use

## How it should work
1. **Aggregate** — Python pipeline pulls metadata from trusted libre sources
2. **Normalize** — Unified schema: family, license, category, variants, download URLs
3. **Browse** — Static web UI: search, filter, preview, detail modal with links
4. **Refresh** — Re-run aggregation periodically to stay current

## User experience goals
- Feel "huge" — 2,000+ families visible immediately
- Fast discovery — search by name, category, source, featured tags
- Live previews — lazy-loaded woff2 / Google Fonts CSS
- Trust — license type and commercial_use flag on every entry
- One-click to source page, GitHub, or download

## Target categories
Serif, Sans-serif, Display, Handwriting, Monospace, Slab, Script, Featured, Variable, Brand-grade, Experimental

## Current catalog stats (2026-07-19)
- **2,013** merged families (deduplicated, commercial-safe)
- **7,875** variants
- **105** featured families
