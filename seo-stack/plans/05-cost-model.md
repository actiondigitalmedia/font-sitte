# Cost Model — Max Impact / Min Spend

## Competitor SaaS (what we're avoiding)

| Tool | Typical entry | Notes |
|------|---------------|-------|
| Ahrefs Lite+ | ~$99–129+/mo | Overkill for one catalog site |
| Semrush Pro | ~$139+/mo | Suite bloat |
| Surfer / Frase | ~$59–99+/mo | Content scoring; replaceable with SERP structure + templates |

Annual risk: **$1,000–$2,500+** for seats you barely use.

## Our stack cost envelope

| Item | Setup | Ongoing |
|------|-------|---------|
| Domain | ~$10–15/yr | — |
| GitHub Pages / Netlify free | $0 | $0 |
| GSC | $0 | $0 |
| Umami self-host / Plausible starter | $0 / ~$9 | low |
| OpenSEO self-host | $0 | $0 |
| DataForSEO | $1 trial; $50 min top-up | PAYG only |
| Firecrawl | Free ~1k credits/mo | $0 until need Hobby |
| LLM API | optional | hard-cap $10/mo |
| Cursor | existing | existing |

### Realistic burn scenarios

| Scenario | What you run | Est. spend |
|----------|--------------|------------|
| **Bootstrap** | Phase 0–1 only (no paid SEO APIs) | **$0** (+ domain) |
| **Research month** | Keyword expand + 500 SERPs + Labs pulls | **~$5–25** |
| **Steady ops** | Weekly rank track 100 KW + monthly SERP sample | **~$3–15/mo** |
| **Aggressive** | Daily tracking, backlinks, on-page audits, LLM copy | **~$30–80/mo** |

Still far below one Ahrefs seat.

## API call hygiene (prevents bill shock)

1. Set DataForSEO dashboard spending limits
2. MCP: enable only needed modules
3. Cache SERP/keyword JSON under `seo-stack/data/cache/` (gitignored)
4. Prefer weekly rank checks over daily
5. Log every billed call with timestamp + workflow id
6. Agents must dry-run with cached fixtures in CI

## What is *not* free (don't kid yourself)

| Need | Reality |
|------|---------|
| Time to build SSG pages | Dev time (Cursor accelerates) |
| Unique hub copy | Edit time or small LLM spend |
| Backlinks | Outreach effort; tools don't buy links ethically |
| Beating DaFont on head terms | Hard; win long-tails + commercial-safe modifiers first |

## ROI framing

One ranking `/fonts/{popular}/` or `/commercial-use/` page that sustains AdSense RPM can repay months of DataForSEO credits. Prioritize **indexable surface area** before paid intel.

## Go / no-go spend gates

| Gate | Spend allowed |
|------|---------------|
| Site not public yet | $0 on SEO APIs |
| Pages live + sitemap submitted | Up to $50 DataForSEO deposit |
| GSC shows impressions | Unlock CTR automation (free) + light tracking |
| Revenue from ads/affiliates | Raise API caps deliberately |
