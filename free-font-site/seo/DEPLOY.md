# Deploy (branch method — matches what you see in Settings → Pages)

GitHub’s Pages UI usually shows **Source: Deploy from a branch**, not a separate “GitHub Actions” button. That’s fine. We now publish from the **`gh-pages`** branch.

## What you should see / do

1. Open: https://github.com/actiondigitalmedia/font-sitte/settings/pages  
   (must be logged in as **actiondigitalmedia** — admin on the repo)

2. Under **Build and deployment**:
   - **Source:** leave / set to **Deploy from a branch**
   - **Branch:** **`gh-pages`**
   - **Folder:** **`/ (root)`**
   - Click **Save**

3. Wait 1–2 minutes. Refresh the Pages settings page — a green box should show the site URL:

   **https://actiondigitalmedia.github.io/font-sitte/**

### If you still don’t see those controls

- Confirm you’re on **Settings → Pages** (left sidebar under “Code and automation”), not Environments / Actions.
- Confirm you’re the repo owner (`actiondigitalmedia`). Collaborators without admin won’t get the Branch dropdown.
- On mobile/narrow UI, look for a **Source** dropdown that currently says `Deploy from a branch` — open it; options are usually only that + `GitHub Actions`.

You do **not** need “GitHub Actions” as the source for this setup.

## Smoke-test after Save

- https://actiondigitalmedia.github.io/font-sitte/
- https://actiondigitalmedia.github.io/font-sitte/fonts/roboto/
- https://actiondigitalmedia.github.io/font-sitte/commercial-use/
- https://actiondigitalmedia.github.io/font-sitte/sitemap.xml
- https://actiondigitalmedia.github.io/font-sitte/robots.txt

## Google Search Console (after the site URL works)

1. https://search.google.com/search-console → Add property → **URL prefix**  
   `https://actiondigitalmedia.github.io/font-sitte/`
2. Verify (HTML file → drop `google*.html` into `free-font-site/web/` → rebuild/redeploy)
3. Sitemaps → submit `sitemap.xml`

CTR repair later:

```bash
python3 free-font-site/scripts/gsc_ctr_report.py ~/Downloads/Pages.csv
```

## How updates work

The `gh-pages` branch already has the full built site (2,136 font pages + hubs).  
CI on the SEO branch can rebuild and force-push `gh-pages` on each push (see workflow).
