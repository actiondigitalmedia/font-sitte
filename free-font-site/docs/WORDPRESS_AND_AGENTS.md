# WordPress MCP vs this catalog (Agents window)

This project ships as **static files** on GitHub Pages — fast, cheap, and ideal for **Cloud Agents** that run `scheduled_refresh.py` on a schedule.

## What to use where

| Goal | Tool |
|------|------|
| Public font browse + live previews | This repo → Pages (`gh-pages`) |
| Scheduled font fetch + deploy | GitHub Actions `deploy-pages.yml` |
| Research new fonts + approve licenses | Cursor **Automations** + `cloud-agent-catalog-runbook.md` |
| Marketing / coupon / blog site | WordPress MCP in the **IDE** (separate repo) |

## Agents window (Cursor)

Create an automation:

1. Repo: `actiondigitalmedia/font-sitte`
2. Schedule: weekly (between Mon/Thu CI runs)
3. Prompt file: `free-font-site/docs/cloud-agent-catalog-runbook.md`
4. Tasks: run discovery → verify Free Faces candidates → update `approved-candidates.json` → commit → push `main`

CI will rebuild and update the live list with **in-card font previews** after each push.

## Making the list look like FontSpace / 1001 Fonts

The browse UI (`web/`) now uses:

- **Light preview pane** on each card with the **family name, alphabet, and pangram in the actual face**
- **Eager batch loading** (`PREVIEW_CONCURRENCY`) so the first screenful shows real fonts quickly
- **Header search** + **category pills** like major directories

No WordPress required for that experience.
