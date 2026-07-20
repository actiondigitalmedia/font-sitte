# Super-Tool Stack Architecture

## Design principle

**Compose, don't subscribe.** Each tool does one job. Cursor is the orchestrator. Pay only for data you consume.

```
┌─────────────────────────────────────────────────────────────┐
│  CURSOR / CLOUD AGENTS                                      │
│  Write scripts • run workflows • review diffs • ship PRs    │
└───────────────┬─────────────────────────────┬───────────────┘
                │ MCP                         │ scripts
                ▼                             ▼
┌───────────────────────────┐   ┌─────────────────────────────┐
│ OpenSEO (OSS UI + MCP)    │   │ font-sitte pipelines        │
│ keywords • ranks • audits │   │ aggregate → build pages     │
└─────────────┬─────────────┘   │ sitemap • schema • links    │
              │                 └──────────────▲──────────────┘
              ▼                                │
┌───────────────────────────┐                  │
│ DataForSEO APIs           │                  │
│ SERP • Labs • Keywords    │                  │
│ OnPage • Backlinks        │                  │
└───────────────────────────┘                  │
                                               │
┌───────────────────────────┐   ┌──────────────┴──────────────┐
│ Google Search Console API │   │ Site (static HTML)          │
│ clicks • CTR • queries    │──▶│ /fonts/* /category/* /use/* │
└───────────────────────────┘   └─────────────────────────────┘
                                               ▲
┌───────────────────────────┐                  │
│ Scraper (optional)        │──────────────────┘
│ Firecrawl / Trafilatura   │  competitor structure → markdown
│ BeautifulSoup (existing)  │
└───────────────────────────┘
```

## Layer A — Coding environment (already have)

| Piece | Role |
|-------|------|
| Cursor Desktop / Cloud Agents | Implement pages, pipelines, audits |
| This repo `seo-stack/` | Plans, workflow specs, MCP templates |
| `free-font-site/` (other branch) | Catalog data + UI |

**Agent rules of engagement**

- Prefer scripts in-repo over chat copy-paste
- Never commit API keys (use CI secrets / local env; **no new `.env` files that overwrite existing**)
- Cap DataForSEO modules; log every paid call to `seo-stack/logs/` (gitignored)

## Layer B — Data engine

### Primary: DataForSEO (pay-as-you-go)

| Module | Use for font-sitte | Priority |
|--------|--------------------|----------|
| Keywords Data / Labs | Seed expansion: "free commercial fonts", "OFL fonts", "[name] font download" | P0 |
| SERP API | SERP feature + competitor URL patterns | P0 |
| On-Page API | Technical audit once live | P1 |
| Backlinks API | Referring domain gaps vs FontSpace/DaFont (realistic expectations) | P2 |
| Domain Analytics | Competitor traffic estimates | P2 |

**Cost shape:** ~$0.0006+/SERP; $50 min deposit once past $1 trial. No monthly SaaS seat.

### UI + agent bridge: OpenSEO ([every-app/open-seo](https://github.com/every-app/open-seo))

- Self-host: Docker (local) or Cloudflare Workers (team)
- Native MCP → Cursor can call keyword/SERP/GSC tools in chat
- Hosted option at openseo.so if you don't want to host

**Recommended start:** Docker OpenSEO locally + DataForSEO key when research phase begins.

## Layer C — Site truth (free)

| Tool | Why |
|------|-----|
| **Google Search Console API** | Only accurate clicks/impressions/queries for *your* domain |
| **Google Analytics alternative** | Umami (self-host) or Plausible (cheap) — privacy-friendly, light |
| **PageSpeed Insights / CrUX** | CWV before scaling pSEO |

GSC automation target (from your brief, adapted):

> Flag URLs with **impressions ≥ 1,000** and **CTR < 2.0%** → propose title + meta rewrites → PR.

## Layer D — Scraper

| Option | When | Cost |
|--------|------|------|
| Existing BeautifulSoup/requests | Source aggregation (already in pipeline) | $0 |
| [Trafilatura](https://github.com/adbar/trafilatura) | Cheap local markdown extraction | $0 |
| Firecrawl free (~1k credits/mo) | JS-heavy competitor pages, clean MD for agents | $0–$16 Hobby |
| Firecrawl self-host | High volume, you operate Docker | $0 infra only |

**Policy:** Scrape for **structure/intent patterns**, never republish competitor copy.

## Layer E — LLM (selective)

Use Claude/GPT APIs only for:

1. Unique intros for category hubs (human-edited)
2. CTR title/meta variants from GSC losers
3. Pairing blurb generation from catalog attributes

Do **not** generate 2,000 generic "This is a beautiful font…" bodies. Catalog fields already provide uniqueness.

## Recommended "super config" (minimal monthly)

| Component | Setup | Est. monthly |
|-----------|-------|--------------|
| Cursor | Existing | (already paying) |
| Static hosting | GitHub Pages | $0 |
| GSC + Umami | Free / self-host | $0 |
| OpenSEO | Docker self-host | $0 |
| DataForSEO | PAYG, hard spend cap $20–50 | $5–50 usage |
| Firecrawl | Free tier | $0 |
| LLM API | Cap $10 | $0–10 |
| **Total** | | **~$5–60** |

Vs Ahrefs Lite / Semrush Pro: often $99–$229+/seat for overlapping data you won't use.

## MCP wiring (conceptual)

See [`../config/mcp.openseo.example.json`](../config/mcp.openseo.example.json) and [`../config/mcp.dataforseo.example.json`](../config/mcp.dataforseo.example.json).

Enable only:

```
KEYWORDS, SERP, LABS, SEARCH_CONSOLE
```

Disable Backlinks/OnPage until needed — prevents agent spend explosions.

## Multi-site note

You said "web sites" (plural). This stack is **site-agnostic**:

1. One OpenSEO org with multiple projects
2. One DataForSEO account, per-site spend tags
3. Per-repo `seo-stack/` or a shared `actiondigitalmedia/seo-ops` later

For now, **font-sitte** is Site Zero and the pSEO proving ground.
