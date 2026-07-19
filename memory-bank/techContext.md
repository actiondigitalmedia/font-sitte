# Tech Context

## Site stack (font-sitte)
| Layer | Tech |
|-------|------|
| Aggregation | Python 3, requests, BeautifulSoup |
| Data | catalog.json / CSV / JSON Schema |
| UI (current) | Vanilla HTML/CSS/JS |
| Deploy target | GitHub Pages / Netlify (planned) |
| SEO build (planned) | Astro or Eleventy or Python static generator |

## SEO ops stack (planned)
| Layer | Tech |
|-------|------|
| Agent | Cursor (+ optional Cline) |
| Data | DataForSEO PAYG |
| UI/MCP | OpenSEO (Docker/Cloudflare) |
| Truth | Google Search Console API |
| Analytics | Umami or Plausible |
| Scrape | Trafilatura local; Firecrawl free/optional |
| LLM | Claude/GPT API with hard caps |

## Constraints
- No secret `.env` overwrite
- License filter: commercial-safe only
- Do not re-host font binaries
- Cache paid API responses
- MCP modules limited to control spend

## Ports
- 8080 — local catalog UI (existing)
- Avoid 26000–26999
