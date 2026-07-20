# Deploy + Google Search Console

## 1) Enable GitHub Pages (required — one-time, in the GitHub UI)

This agent token cannot enable Pages (API 403). Do this once as repo admin:

1. Open **Settings → Pages**
2. **Build and deployment → Source:** GitHub Actions
3. Save

Site URL (project Pages):  
`https://actiondigitalmedia.github.io/font-sitte/`

Optional custom domain later: Settings → Pages → Custom domain (then set `SITE_URL` in the workflow).

## 2) Deploy

Workflow: [`.github/workflows/deploy-pages.yml`](../.github/workflows/deploy-pages.yml)

Triggers on push to:
- `main`
- `cursor/seo-strategy-plans-d92e`
- `cursor/free-font-aggregation-43e3`
- or **Actions → Build and Deploy Pages → Run workflow**

CI builds from committed catalog (no live scrape) + runs `verify_seo.py`.

## 3) Google Search Console

1. Go to [Google Search Console](https://search.google.com/search-console)
2. Add property: **URL prefix** → `https://actiondigitalmedia.github.io/font-sitte/`
3. Verify with **HTML file** (easiest):
   - Download `googleXXXXXXXX.html` from GSC
   - Drop it in `free-font-site/web/` (and it will be copied into `dist/` on next build)
   - Or put the file contents path into `free-font-site/seo/content/gsc-verification.html` and we can wire copy — for now copy into `web/`
4. After verify → **Sitemaps** → submit: `sitemap.xml`
5. Also submit if needed: `sitemap-hubs.xml`, `sitemap-fonts.xml` (index already references them)

### HTML-tag verification alternative

If GSC gives a meta tag, paste it into `free-font-site/web/index.html` `<head>` and rebuild.

## 4) CTR repair loop (after impressions exist)

Export Pages CSV from GSC Performance, then:

```bash
python3 free-font-site/scripts/gsc_ctr_report.py ~/Downloads/Pages.csv \
  --min-impressions 100 --max-ctr 0.02
# → seo-stack/data/ctr-repair.csv
```

Early traffic: use `--min-impressions 50`. Later: raise to `1000` as in the original brief.

## 5) Post-deploy smoke checklist

- [ ] `https://actiondigitalmedia.github.io/font-sitte/`
- [ ] `.../fonts/roboto/`
- [ ] `.../commercial-use/`
- [ ] `.../sitemap.xml`
- [ ] `.../robots.txt`
- [ ] View-source: canonical + JSON-LD present
- [ ] GSC property verified + sitemap submitted
