# Backups and reusing discovery on other sites (e.g. coupon site)

## Local backup (any time)

```bash
python3 scripts/backup_project.py
```

Creates under `backups/`:

| Output | Purpose |
|--------|---------|
| `font-sitte_YYYY-MM-DD_HHMMSS/` | Full tree copy (no raw cache) |
| `font-sitte_YYYY-MM-DD_HHMMSS.tar.gz` | Portable archive for off-site storage |
| `catalog-snapshot.json` | Point-in-time catalog for diff/restore |
| `manifest.json` | Family count, branch, reuse notes |
| `LATEST.txt` | Pointer to newest backup |

## CI backup

Workflow **`backup-snapshot.yml`** runs **weekly (Sunday 07:30 UTC)** and on demand. Artifacts retained **90 days** in GitHub Actions.

## Restore

```bash
tar -xzf backups/font-sitte_<stamp>.tar.gz -C /tmp
# Copy /tmp/font-sitte_<stamp>/free-font-site and memory-bank into your repo
cd free-font-site && pip install -r requirements.txt && python3 scripts/scheduled_refresh.py
```

## Reuse for coupon / WordPress / other agents

This repo is **static GitHub Pages**, not WordPress. Your WordPress MCP workflows stay in the IDE for other projects. **Reuse these pieces** on any property:

| Component | Reuse |
|-----------|--------|
| `scripts/discover_fonts.py` | Weekly “what’s new” diff vs catalog |
| `discovery/sources-registry.json` | Legal tiers + source list |
| `discovery/approved-candidates.json` | Human-verified adds |
| `docs/cloud-agent-catalog-runbook.md` | Scheduled Cloud Agent prompt |
| `scripts/scheduled_refresh.py` | One command full rebuild |

For a **coupon site agent**: point the same automation at this repo (fonts) or fork `discovery/` into the coupon repo and add offer-specific `sources-registry.json` entries.

## WordPress note

To mirror this **UI** on WordPress later: export specimen HTML pattern from `web/app.js` + `styles.css`, or embed the static catalog via iframe to `https://actiondigitalmedia.github.io/font-sitte/`. The live preview pattern is `FontFace` + `preview_woff2` from `catalog-lite.json`.
