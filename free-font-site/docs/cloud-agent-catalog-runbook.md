# Cloud Agent runbook — font catalog refresh

Use this as the **system prompt** (or attachment) for a **scheduled Cursor Cloud Agent** on `actiondigitalmedia/font-sitte`. GitHub Actions already rebuilds and deploys 2× weekly; this agent adds **license verification** and **approved-candidates** merges.

## Mission

Keep the public catalog growing with **legal, commercial-safe** fonts users care about (Old English, Y2K, pixel, web-modern, display, script, mono)—without bypassing the human gate for untrusted sources.

## Preconditions

- Branch: `main` or `cursor/free-font-aggregation-43e3` (match your deploy branch until merged)
- Python 3.12+, network for source fetches
- Never create or overwrite `.env` files

## Steps (execute in order)

### 1. Load context

Read:

- `free-font-site/docs/font-discovery-operation.md`
- `free-font-site/docs/continuous-updates.md`
- `memory-bank/activeContext.md` and `memory-bank/progress.md`

### 2. Discovery diff

```bash
cd free-font-site
pip install -r requirements.txt
python3 scripts/discover_fonts.py
```

Open the newest file in `discovery/reports/*-discovery.json`.

### 3. Triage `source_diffs`

For each entry with `not_in_catalog > 0`:

| `legal_tier` / `auto_merge` | Action |
|-----------------------------|--------|
| `verified-*`, `auto_merge: true` | If names are missing from live catalog, **fix the source adapter** or dedupe slug in code—do not only add to approved-candidates |
| `manual-review` | Open official specimen/license page; if OFL/Apache/ITF-FFL/commercial OK → add to `discovery/approved-candidates.json` |
| Already in Google/Fontshare under different spelling | Document dedupe; no duplicate approved entry |

### 4. Approved candidates

Edit `free-font-site/discovery/approved-candidates.json`:

- Required: `family_name`, `license_type`, `license_url`, `commercial_use: true`, `source_url`, `verified_at`, `verified_by`
- Optional: `style_tags`, `download_url`, `category`, `notes`

### 5. Full refresh

```bash
python3 scripts/scheduled_refresh.py
```

Confirm `discovery/reports/latest-refresh-summary.json`:

- `total_families` increased or stable (no unexpected drop)
- `discovery_highlights` reviewed

### 6. Ship

```bash
git add free-font-site/ memory-bank/
git commit -m "feat(catalog): discovery refresh — <short summary>"
git push
```

Open or update PR if not on `main`. GitHub Actions will deploy on code push (catalog-only bot commits on schedule skip redeploy via `paths-ignore`).

### 7. Document

Append to `memory-bank/progress.md`: date, fonts added, sources researched, open backlog.

## Out of scope (do not do)

- Host font binaries on our origin unless license explicitly allows
- Merge FontSpace / unknown licenses without reading license text
- Disable `commercial_use` filter in aggregate

## Escalation

- Repeated Fontshare “missing” names with `auto_merge: true` → fix `scripts/sources/fontshare.py` + `discover_fonts.py` name normalization
- Free Faces scraper noise → tighten `scripts/sources/free_faces.py` heuristics

## Success

- New verified families in catalog
- PR merged / deploy green
- Discovery report artifact shows shrinking manual-review backlog over time
