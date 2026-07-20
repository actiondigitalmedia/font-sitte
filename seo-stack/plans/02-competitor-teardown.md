# Competitor Teardown — Free Font Discovery Sites

Benchmark: what ranking sites do, what to copy, what to skip.

## Competitor map

| Site | Model | Strength | Weakness (your opening) |
|------|-------|----------|-------------------------|
| **Google Fonts** | Official catalog + webfont CDN | Authority, completeness, performance docs | Not "download desktop font" intent; no commercial-use education as primary UX |
| **DaFont** | UGC mega-catalog | Brand habit, rankings for "[name] font", theme taxonomy | License chaos (personal-use traps); ugly tech SEO; trust risk |
| **FontSpace** | UGC + designer pages | Category URLs, designer entities, download velocity | Mixed licenses; noisy UX |
| **1001 Fonts** | Catalog aggregator | Breadth, category coverage | Thin pages, trust/license clarity |
| **Fontshare** | Curated quality free | Brand, quality, commercial clarity | Small catalog |
| **Font Squirrel** | Curated + "almost free" | License filters, quality | Slower growth, older IA |
| **MyFonts / Adobe** | Paid | Commercial intent capture | Paywall — not your competitor for free |

## URL & IA patterns that win

### Google Fonts
- Entity = family: `/specimen/{Family+Name}`
- Strong filters: category, language, properties (variable, etc.)
- Educational content hubs (readability, material design) — **topic authority**
- Live specimen as primary content (not blog spam)

**Steal:** Specimen-first pages, filters as crawlable hubs where possible, educational cluster content.

### DaFont
- Entity: `/{slug}.font`
- Themes: `theme.php?cat=N` (parameterized — weaker than path-based)
- Top / new / lists for discovery + freshness signals
- Download counts as social proof

**Steal:** Per-font entity URL, popularity/new lists. **Skip:** Query-string categories; unclear licenses.

### FontSpace
- Categories: `/category/{style}` and multi-tag paths
- Designer/foundry entity pages
- Commercial-use filter (important — users search this)

**Steal:** `/category/{slug}`, designer/source pages, commercial-use as first-class filter **and** landing page.

## SERP intent clusters (font niche)

| Intent | Example queries | Page type you need |
|--------|-----------------|--------------------|
| Brand/entity | `roboto font`, `inter font download` | `/fonts/roboto/` |
| Modifier + free | `free commercial fonts`, `ofl fonts` | Hub: `/commercial-use/`, `/licenses/ofl/` |
| Style | `free sans serif fonts`, `free script fonts` | `/category/sans-serif/` |
| Use-case | `free fonts for logos`, `wedding invitation fonts free` | `/use/logos/`, `/use/wedding/` |
| Comparison | `roboto vs open sans`, `best google fonts 2026` | Editorial (Phase 3) |
| Alternative | `futura free alternative` | `/alternatives/futura/` (high value, later) |

## Content quality bar vs spam

Winners combine:

1. **Live specimen** (must render the typeface)
2. **License clarity above the fold**
3. **Download / webfont CTA**
4. **Related fonts + category links**
5. **Minimal unique prose** that still answers intent ("what it's for", "weights", "pairings")

Losers: walls of AI text, no specimen, unclear license, orphan URLs.

## Technical patterns to match/beat

| Signal | Competitors | Our target |
|--------|-------------|------------|
| Indexable HTML | Mixed (some JS-heavy) | Pre-rendered static HTML for all money pages |
| CWV | Often mediocre on UGC sites | Fast static + lazy font samples |
| Schema | Rare / inconsistent | `CreativeWork` / `SoftwareApplication` + `Offer` (price 0) + BreadcrumbList |
| Sitemap | Usually yes | Auto-generated from catalog |
| Internal links | Category ↔ font ↔ designer | Catalog graph: category, source, tags, similar, pairings |
| Canonical | Spotty on facets | Strict canonicals; noindex junk facets |

## Positioning wedge (copy this into brand messaging)

> **Commercial-safe libre fonts only.** Every family verified OFL/Apache/UFL/etc. Preview instantly. Download from the source.

That wedge is weak on DaFont/FontSpace SERPs and strong against "got burned by personal-use font" stories.

## Competitive research workflow (cheap)

1. DataForSEO SERP for 20 seed keywords → extract ranking URL patterns
2. Firecrawl/Trafilatura 10 competitor pages → H1/H2/structure checklist
3. Diff against our template → update `templates/`
4. Rank-track weekly top 50 seeds via OpenSEO (not daily — save $)

See [`../workflows/02-competitor-structure-scrape.md`](../workflows/02-competitor-structure-scrape.md).
