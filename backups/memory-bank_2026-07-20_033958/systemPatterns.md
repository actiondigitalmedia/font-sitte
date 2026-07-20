# System Patterns

## Architecture patterns
- **Catalog as source of truth** → generate pages/sitemaps/links at build time
- **Compose SEO tooling** → Cursor orchestrates; DataForSEO supplies data; GSC supplies truth; OpenSEO is optional UI/MCP
- **Entity-first IA** → `/fonts/{slug}/` primary; hubs secondary
- **Pay-as-you-go** → never idle SaaS seats

## SEO patterns
- Programmatic pages from structured data
- Keyword cluster → single owner URL
- CTR repair loop on high-impression losers
- Internal link graph from catalog fields
- Structure scraping of competitors (not content cloning)

## Repo patterns
- Plans in `seo-stack/plans/`
- Executable workflow specs in `seo-stack/workflows/`
- Example MCP configs only (no secrets)
- Memory bank updated every major step
- Separate feature branches: `cursor/<name>-d92e`
