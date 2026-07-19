# Executive Brief — SEO for font-sitte

## Verdict

You already have the hard part: **2,013 commercial-safe font entities** with licenses, categories, sources, and download links. That is a pSEO dataset. Do **not** buy an all-in-one SEO suite. Build a **data-first stack**:

1. **Site layer (free)** — crawlable per-font + category pages, sitemaps, schema, Core Web Vitals
2. **Truth layer (free)** — Google Search Console + lightweight analytics (Umami/Plausible)
3. **Intel layer (cheap)** — DataForSEO pay-as-you-go behind OpenSEO (self-host or hosted)
4. **Agent layer (Cursor)** — scripts that cluster keywords, draft unique copy from catalog fields, fix CTR losers, map internal links
5. **Scrape layer (optional/cheap)** — Firecrawl free tier or self-host for competitor SERP/page structure (not for bulk content theft)

## Why this beats $99–$399/mo tools

| Capability | Semrush/Ahrefs | Our stack |
|------------|----------------|-----------|
| Rank + keyword data | Subscription seat | DataForSEO cents/call |
| Dashboard | SaaS UI | OpenSEO (OSS) + MCP for Cursor |
| Content at scale | Manual / expensive AI add-ons | Catalog-driven templates + selective LLM polish |
| Site truth | Imported | Direct GSC API (source of truth) |
| Monthly floor | High | ~$0–$50 until you scale |

## Impact ranking (do first → later)

| Rank | Lever | Why | Cost |
|------|-------|-----|------|
| 1 | Indexable `/fonts/{slug}/` pages | Competitors win on entity pages; SPA modals don't rank | $0 |
| 2 | Category + intent hubs | "free commercial sans serif fonts", "OFL fonts" | $0 |
| 3 | JSON-LD + OG + sitemap | Richer SERP understanding, faster discovery | $0 |
| 4 | GSC CTR repair loop | Titles/metas for high-impression losers | $0 API |
| 5 | Keyword clustering via DataForSEO | Prioritize which hubs/pages to expand | ~$5–20 |
| 6 | Internal link graph from catalog | Avoid orphan pages; push equity to money pages | $0 |
| 7 | Selective unique copy (LLM) | Only where template uniqueness is weak | API cents |
| 8 | Backlink / AI-visibility monitoring | After you have indexable surface area | DataForSEO |

## Differentiation vs DaFont / FontSpace

They win on volume + habit. You win on **trust + commercial-safe clarity**:

- Every page screams **OFL / commercial-use verified**
- Link to authoritative sources (Google Fonts, Fontshare, etc.)
- No "personal use only" traps
- Cleaner UX, faster pages, entity schema

Positioning angle: **"Free fonts you can actually use commercially."**

## Risk flags

- Thin template pages with zero unique fields → soft Google filter. Mitigate: unique license/source/variant/pairing/tag content per family.
- LLM spam at 1k pages before technical SEO → waste. Mitigate: ship templates first, LLM only for top clusters.
- Agent runaway API spend → set DataForSEO spend caps + `ENABLED_MODULES` on MCP.

## Approve to execute

Default execution order after you say go:

1. Static site generator path (Astro or Eleventy) from `catalog.json`
2. GSC property + Umami
3. OpenSEO Docker + DataForSEO $50 deposit when ready for research
4. Cursor workflows in `seo-stack/workflows/`
