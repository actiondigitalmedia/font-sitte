# SEO Stack — Maximum Impact, Minimal Cost

Autonomous SEO planning + tooling config for **font-sitte** (free/libre font catalog) and reusable across future Action Digital Media sites.

## Quick answers

| Question | Answer (this repo) |
|----------|--------------------|
| **CMS / platform** | Custom static site — vanilla HTML/CSS/JS + Python catalog pipeline. No WordPress/Webflow. Deploy target: GitHub Pages / Netlify. |
| **Primary SEO goal** | **Publishing / discovery traffic** for commercial-safe free fonts → AdSense + affiliate later. Not local lead-gen, not classic e-com checkout. |
| **Best strategy** | **Programmatic SEO (pSEO)** at catalog scale (~2k+ font pages + category/intent clusters), powered by cheap APIs + Cursor agents. |

## What's in this folder

| Path | Purpose |
|------|---------|
| [`plans/00-executive-brief.md`](plans/00-executive-brief.md) | Verdict, cost ceiling, what to build first |
| [`plans/01-stack-architecture.md`](plans/01-stack-architecture.md) | Super-tool config: Cursor + OpenSEO + DataForSEO + GSC + scrapers |
| [`plans/02-competitor-teardown.md`](plans/02-competitor-teardown.md) | What Google Fonts / DaFont / FontSpace / 1001Fonts / Fontshare do |
| [`plans/03-page-taxonomy.md`](plans/03-page-taxonomy.md) | URL map, templates, schema, internal linking graph |
| [`plans/04-phased-roadmap.md`](plans/04-phased-roadmap.md) | Phased build plan (foundation → pSEO → automation → scale) |
| [`plans/05-cost-model.md`](plans/05-cost-model.md) | Pay-as-you-go budget vs Semrush/Ahrefs |
| [`workflows/`](workflows/) | Cursor-agent workflow specs (keyword → pages → GSC loop) |
| [`config/`](config/) | MCP / env templates (no secrets committed) |
| [`templates/`](templates/) | Title/meta/JSON-LD templates for static generators |

## Non-goals (for this planning pass)

- Paying for Ahrefs/Semrush/Surfer subscriptions
- Shipping 1,000 LLM-spam pages without unique catalog data
- Hosting font binaries (catalog + link-out model stays)

## Next action after plan approval

Implement Phase 0–1 from [`plans/04-phased-roadmap.md`](plans/04-phased-roadmap.md): static per-font pages, sitemap, JSON-LD, then wire OpenSEO MCP + GSC.
