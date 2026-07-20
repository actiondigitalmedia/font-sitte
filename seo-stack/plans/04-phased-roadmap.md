# Phased Roadmap — SEO Execution

No calendar-day estimates. Phases are dependency-ordered work packages.

## Phase 0 — Preconditions (before SEO spend)

**Exit criteria:** public HTTPS domain, GSC verified, baseline crawl works.

- [ ] Merge/ship font catalog site to GitHub Pages or Netlify
- [ ] Custom domain + SSL
- [ ] `robots.txt` allowing crawl
- [ ] Privacy page (needed before AdSense later)
- [ ] GSC property verified (DNS or HTML file)
- [ ] Umami or Plausible installed

**Cost:** $0–domain

## Phase 1 — Technical + entity foundation (highest ROI)

**Exit criteria:** ≥2,000 indexable font URLs in sitemap; schema validates; internal links present.

- [x] Choose generator: **Python + Jinja2** (locked — meets/exceeds SEO standards without Astro/Eleventy)
- [x] Emit `/fonts/{slug}/index.html` from catalog (`scripts/build_site.py`)
- [x] Title + meta templates (`seo/templates/`)
- [x] JSON-LD CreativeWork/SoftwareApplication + Breadcrumbs + FAQPage
- [x] OG/Twitter cards on entity + hub pages
- [x] Category + source + license + tags + use hubs + `/commercial-use/`
- [x] `sitemap.xml` index (hubs + fonts) + robots.txt
- [ ] Fix CWV: lazy-load previews, shrink `catalog-lite` strategy for browse
- [ ] Deploy + ping GSC

**Cost:** $0 API

**Verify:** `python3 free-font-site/scripts/build_site.py && python3 free-font-site/scripts/verify_seo.py`

## Phase 2 — Keyword intelligence (cheap data)

**Exit criteria:** prioritized keyword → page map for top 100 opportunities.

- [ ] DataForSEO account ($1 trial → $50 deposit when ready)
- [ ] OpenSEO Docker or hosted + MCP in Cursor
- [ ] Seed list research (see `workflows/01-keyword-cluster.md`)
- [ ] Cluster → assign primary page (font vs hub vs use-case)
- [ ] Rank-track 50–100 keywords weekly (not daily)

**Cost:** typically low single-digit to tens of dollars for initial research

## Phase 3 — Intent hubs + selective copy

**Exit criteria:** commercial-use + top use-case hubs live with unique intros.

- [ ] `/commercial-use/` money page
- [ ] Top 10 `/use/*` hubs from keyword data
- [ ] LLM draft → human edit → commit markdown overlays
- [ ] Internal link injection from hubs → best fonts

**Cost:** <$10 LLM if capped

## Phase 4 — GSC feedback loop (automation)

**Exit criteria:** weekly PR or report of CTR losers with proposed titles.

- [ ] GSC API credentials (OAuth service account / OAuth client)
- [ ] Script: impressions≥1000 & CTR<2% → CSV + title proposals
- [ ] Apply winners; remeasure 14–28 days later

See `workflows/03-gsc-ctr-repair.md`.

**Cost:** $0

## Phase 5 — Competitor structure + link graph polish

- [ ] Scrape 10–20 competitor entity pages (structure only)
- [ ] Diff H2 inventory vs our template
- [ ] Automate similar-font + pairing edges
- [ ] Orphan audit (pages with <3 inbound)

See `workflows/02-competitor-structure-scrape.md` and `04-internal-linking.md`.

## Phase 6 — Expansion & AI visibility

- [ ] `/alternatives/{classic}/` pages (Futura, Helvetica, Garamond free alts)
- [ ] Light editorial (best-of lists) only when data-backed
- [ ] OpenSEO AI visibility / citations monitoring
- [ ] Backlink prospecting (directories, type blogs) — manual + agent assist

## Monetization sync (parallel, not before Phase 1)

From existing roadmap: AdSense slots **after** indexable pages exist and trust pages (privacy, about) are live. Never on download obstruction.

## Phase dependency graph

```
Phase0 deploy ──► Phase1 entity pages ──► Phase2 keywords
                         │                      │
                         ▼                      ▼
                   Phase4 GSC ◄──────── Phase3 hubs
                         │
                         ▼
                   Phase5 links/competitors ──► Phase6 expansion
```

## Definition of done (first meaningful SEO ship)

1. Domain live
2. All fonts have static URLs
3. Hubs for categories + commercial-use
4. Sitemap in GSC
5. OpenSEO/GSC connected for ongoing ops
