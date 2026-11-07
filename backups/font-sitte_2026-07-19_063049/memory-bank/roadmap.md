# Roadmap: font-sitte

## Immediate (now)
- [x] Fix font previews — use Google Fonts CSS API + Fontshare CSS API (fake gstatic URLs removed)
- [ ] User verify previews look distinct after hard refresh

## Phase 1 — More verified libre fonts
Expand catalog with additional **commercial-safe, verifiable** sources:

| Source | License | Method | Priority |
|--------|---------|--------|----------|
| Fontsource metadata | OFL/Apache | GitHub JSON | High |
| Omnibus Type | OFL | GitHub/scrape | High |
| Collletttivo | OFL | GitHub org API | Medium |
| UNCUT.wtf | Mixed libre | API/scrape if available | Medium |
| Free Faces | OFL | Curated list scrape | Medium |
| Google Fonts GitHub | OFL/Apache | METADATA.json per family (for download URLs) | Low (already have metadata) |

**Rule:** Every new font must have `license_type`, `license_url`, and `commercial_use: true` before inclusion.

## Phase 2 — SEO foundation
- [ ] Per-font specimen pages (`/fonts/roboto/`) with unique title/meta description
- [ ] Sitemap.xml generation from catalog
- [ ] Structured data (JSON-LD) for CreativeWork / SoftwareApplication
- [ ] Category landing pages (e.g. `/category/sans-serif/`)
- [ ] Open Graph + Twitter cards for sharing
- [ ] Static site generator or lightweight router (Eleventy, Astro, or vanilla hash routes)

**Target keywords:** "free commercial fonts", "open source fonts", "OFL fonts download", "[font name] free font"

## Phase 3 — Monetization (non-intrusive)
- [ ] Google AdSense slot — header leaderboard (728×90 or responsive)
- [ ] In-feed native ad units between font card rows (every N cards)
- [ ] Sidebar sticky ad on desktop
- [ ] Footer ad unit
- [ ] **No ads on license/download pages** — keep trust
- [ ] Privacy policy + cookie consent (GDPR/CCPA if AdSense)
- [ ] ads.txt for AdSense verification

**Principle:** Ads supplement, never block font discovery or downloads.

## Phase 4 — Deployment
- [ ] GitHub Pages or Netlify static deploy
- [ ] Custom domain + SSL
- [ ] Weekly GitHub Action: aggregate → build → deploy
- [ ] CDN for catalog-lite.json

## Phase 5 — Growth features
- [ ] Font pairing suggestions
- [ ] "Similar fonts" recommendations
- [ ] User favorites (localStorage → optional accounts later)
- [ ] Newsletter / new fonts feed
- [ ] Submit-a-font form (manual review queue)

## Legal guardrails
- Only aggregate fonts with clear libre/commercial licenses
- Display license + attribution on every specimen page
- Link to original source; do not re-host binaries unless license permits
- Keep DMCA/contact page ready before public launch
