# Spend & safety guardrails for SEO agents

## Hard rules
1. Never commit API keys or filled secret files.
2. Default modules: KEYWORDS, SERP, LABS, SEARCH_CONSOLE only.
3. Cache API responses; do not re-fetch identical SERPs within 7 days.
4. Rank tracking: weekly max unless debugging.
5. Firecrawl: free tier first; structure-only scrapes.
6. LLM: no bulk body generation for all fonts.
7. Catalog license boundary stays: commercial-safe only.

## Before any paid API call
- [ ] Site public OR research explicitly approved
- [ ] Cap set in DataForSEO dashboard
- [ ] Workflow name logged
- [ ] Dry-run path exists for CI

## Incident response
If spend spikes: disable MCP servers in Cursor, rotate keys, inspect `seo-stack/data/cache/` call patterns.
