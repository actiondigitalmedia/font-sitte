# Enable the live site (GitHub Pages)

The repo publishes to **`https://actiondigitalmedia.github.io/font-sitte/`** using the **`gh-pages` branch** (what GitHub Pages is already configured to use).

## What runs automatically

After this work merges to `main`, the workflow **Refresh catalog and deploy site**:

1. Scrapes/fetches all trusted font sources
2. Rebuilds the catalog and static `dist/`
3. Pushes `dist/` → **`gh-pages`** (updates the live site)
4. On schedule (Mon/Thu), commits catalog JSON to `main` when counts change

You do **not** need to switch Pages to “GitHub Actions” unless you want to; the **`gh-pages` branch deploy** is the default path.

## If the site shows “errored” in Settings → Pages

1. Open [Settings → Pages](https://github.com/actiondigitalmedia/font-sitte/settings/pages)
2. **Build and deployment → Source:** Deploy from a branch
3. **Branch:** `gh-pages` / **`/ (root)`**
4. Save  
5. Run **Actions → Refresh catalog and deploy site → Run workflow** once

Within a few minutes the site should serve the new build.

## Optional: GitHub Actions as Pages source

Only if you prefer the official `deploy-pages` action:

1. Settings → Pages → Source: **GitHub Actions**
2. In `.github/workflows/deploy-pages.yml`, set `deploy-official-pages` job `if: true` and remove or keep the `peaceiris` step (not both needed)

## Verify

- Site: https://actiondigitalmedia.github.io/font-sitte/
- Health: https://actiondigitalmedia.github.io/font-sitte/health.html
- Latest workflow: [Actions tab](https://github.com/actiondigitalmedia/font-sitte/actions)
