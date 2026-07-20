# Active Context

## Current focus (2026-07-20)
**Deploy + GSC** — workflow ready; Pages must be enabled once in GitHub UI (API 403 for agent token).

## Done
- Python/Jinja2 SEO builder (2136 pages, verify OK)
- Fixed GH project Pages base path (`window.__SITE_BASE__`, `sitePath()` in app.js)
- Deploy workflow triggers on SEO branch; CI builds without live scrape + verify_seo
- GSC runbook: `free-font-site/seo/DEPLOY.md`
- CTR repair script: `scripts/gsc_ctr_report.py` (+ sample CSV)

## Blocked on user (exact UI)
Settings → Pages → **Source: Deploy from a branch** → Branch **`gh-pages`** → Folder **`/ (root)`** → **Save**

Do NOT need “GitHub Actions” as source. `gh-pages` branch is already pushed with the full site.

## Next after Pages live
- Smoke URLs in DEPLOY.md
- Export GSC Pages CSV → ctr-repair when impressions exist
