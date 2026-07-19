# Active Context

## Current focus (2026-07-19)
**SEO strategy planning** on branch `cursor/seo-strategy-plans-d92e`.

User brought AI SEO stack ideas (Cursor + DataForSEO + Firecrawl + OpenSEO + GSC). We mapped them onto font-sitte reality and produced a full plan pack under `seo-stack/`.

## Answers delivered
- **CMS:** custom static site (vanilla + Python), not WP/Webflow
- **Primary SEO goal:** publishing/discovery for free commercial-safe fonts (pSEO)

## Recent changes
- Created `seo-stack/` with plans, workflows, templates, MCP examples, seeds
- Initialized memory-bank for this repo state

## Next steps (awaiting approval to execute)
1. Ship/deploy catalog site (Phase 0) — depends on PR #1 merge/deploy
2. Implement static `/fonts/{slug}/` builder (Phase 1)
3. Wire GSC + optional OpenSEO/DataForSEO when public

## Active decisions
- Compose cheap APIs; avoid Ahrefs/Semrush
- Catalog-driven uniqueness > bulk LLM pages
- No new project `.env` files that overwrite existing secrets
- Commercial-safe license boundary stays

## Open questions for user
- Confirm domain for launch
- Any other sites besides font-sitte to include in multi-site OpenSEO?
- Prefer Astro vs Eleventy vs pure Python static builder?
