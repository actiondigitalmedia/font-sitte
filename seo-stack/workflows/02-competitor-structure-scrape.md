# Workflow 02 — Competitor Structure Scrape

## Goal

Extract **heading structure + page sections** from top-ranking font pages to improve our templates. Not for copying prose.

## Inputs

- Top URLs from SERP for 10 seeds
- Firecrawl (free tier) **or** Trafilatura local

## Steps

1. From keyword research, pick top 3 organic URLs per seed (skip ads).
2. Scrape to Markdown (title, H1–H3, lists, CTA labels only).
3. Normalize into a section checklist:
   - Specimen present?
   - License placement
   - Download CTA wording
   - Similar fonts module
   - Categories/tags
   - Author/foundry entity
   - Comments/social proof
4. Diff vs our `templates/font-page.md`
5. Open PR updating templates only — no scraped sentences committed as content.

## Cursor prompt

```
Scrape these URLs to markdown (structure only). Summarize recurring H2 sections.
Propose template changes to seo-stack/templates/font-page.md.
Do not paste competitor paragraphs into the site.
Prefer Trafilatura locally; use Firecrawl only if JS rendering required.
```

## Outputs

- `seo-stack/data/competitor-structure.json`
- Template PR

## Ethics / legal

- Respect robots.txt where applicable
- Rate-limit
- No binary/font file scraping
- No republishing personal-use fonts into our commercial-safe catalog
