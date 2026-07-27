# Continuous catalog updates

The font site is designed to **stay fresh without manual builds**: upstream sources are re-fetched, the catalog is merged, style tags applied, previews enriched, and GitHub Pages is redeployed on a fixed schedule. A optional **Cursor Cloud Agent** layer handles human-review fonts (Free Faces, approved candidates).

## What runs automatically (GitHub Actions)

| Trigger | Workflow | What happens |
|---------|----------|----------------|
| **Mon + Thu 06:00 UTC** | [`deploy-pages.yml`](../.github/workflows/deploy-pages.yml) | Full fetch → `scheduled_refresh.py` → deploy Pages → commit catalog to `main` if changed |
| **Push to `main`** (code/docs, not catalog-only) | Same | Rebuild + deploy |
| **Manual** | Actions → *Refresh catalog and deploy site* → *Run workflow* | Optional `--no-fetch` / skip discovery |

Entry script (CI + agents):

```bash
cd free-font-site
python3 scripts/scheduled_refresh.py          # full refresh + discovery report
python3 scripts/scheduled_refresh.py --no-fetch   # rebuild from cached raw
```

Summary JSON for logs: `discovery/reports/latest-refresh-summary.json` (local/CI; reports dir is gitignored except via artifacts).

### Enable GitHub Pages (one-time)

1. Repo **Settings → Pages → Build and deployment → GitHub Actions**
2. Ensure environment `github-pages` exists (created on first deploy)

Live URL (default): `https://actiondigitalmedia.github.io/font-sitte/`

### Catalog commits vs deploys

Bot commits (`chore(catalog): automated refresh …`) only touch catalog JSON/CSV/lite/cache. They are **`paths-ignore`d** so they do **not** start a second deploy—the scheduled job already deployed in the same run.

## Cursor Cloud Agent (scheduled “smart” layer)

GitHub Actions covers **trusted sources** (Google, Fontshare, Fontsource, etc.). For **manual-review** finds (Free Faces gallery, one-off OFL releases, UNCUT backlog), use a **recurring Cloud Agent** to research licenses and append `discovery/approved-candidates.json`.

### Recommended schedule

| Layer | Cadence | Responsibility |
|-------|---------|----------------|
| GitHub Actions | 2× / week | Fetch, merge, deploy, commit catalog |
| Cloud Agent | 1× / week (e.g. Wed) | Read discovery report, verify candidates, PR approved fonts |

### Create the automation in Cursor

1. Open **Cursor → Automations** (or Cloud Agents schedule UI for your team).
2. **Repository:** `actiondigitalmedia/font-sitte`
3. **Base branch:** `main` (or your integration branch)
4. **Schedule:** e.g. `0 14 * * 3` (Wed 14:00 UTC)—between GitHub refresh days.
5. **Instructions:** paste the runbook below or point the agent at [`cloud-agent-catalog-runbook.md`](cloud-agent-catalog-runbook.md).

### Agent runbook (short)

Copy into the automation prompt:

```text
You maintain the Free Font Catalog discovery operation.

1. Read free-font-site/docs/font-discovery-operation.md and docs/continuous-updates.md.
2. Run: cd free-font-site && pip install -r requirements.txt && python3 scripts/discover_fonts.py
3. Open the latest discovery/reports/*-discovery.json. For each source with not_in_catalog > 0:
   - Skip if auto_merge is true and the gap is likely a slug/dedupe bug (investigate adapter first).
   - For manual-review sources (Free Faces): verify OFL/commercial license on the official page.
4. Add verified fonts to discovery/approved-candidates.json (never merge unverified).
5. Run python3 scripts/scheduled_refresh.py and verify family count / style_tag_counts in latest-refresh-summary.json.
6. Commit, push, open/update PR. Do not create or overwrite .env files.
7. Update memory-bank/progress.md with what was added or researched.
```

Full checklist: [`cloud-agent-catalog-runbook.md`](cloud-agent-catalog-runbook.md).

## Monitoring

- **Actions tab:** *Refresh catalog and deploy site* — green = live site updated
- **Artifacts:** `font-discovery-<run_id>` — JSON diffs per run
- **Catalog trend:** `total_families` in commit messages / `stats.json`

## Changing cadence

Edit `schedule.cron` in `.github/workflows/deploy-pages.yml`:

```yaml
schedule:
  - cron: "0 6 * * 1,4"   # Mon & Thu
  # - cron: "0 6 * * *"    # daily (heavier on upstream APIs)
```

## Related docs

- [`font-discovery-operation.md`](font-discovery-operation.md) — legal bar, style taxonomy, weekly human procedure
- [`cloud-agent-catalog-runbook.md`](cloud-agent-catalog-runbook.md) — detailed agent checklist
