# Active Context

## Current focus (2026-07-27)
**Continuing Font Discovery Operation** — documented pipeline to find legal free fonts (Old English, Y2K, pixel, web-modern, etc.) and grow the catalog.

## Recent changes
1. **`docs/font-discovery-operation.md`** — weekly playbook, legal bar, architecture
2. **`discovery/`** — `sources-registry.json`, `style-taxonomy.json`, `approved-candidates.json`, reports (gitignored)
3. **`scripts/discover_fonts.py`** — diff raw sources vs catalog; Free Faces scrape for candidates
4. **`scripts/apply_style_tags.py`** — auto tags on aggregate (9 style buckets)
5. **UI** — Style filter + badges on cards/detail; specimen pages show style tags
6. **`approved-candidates`** adapter — human-verified fonts merge into aggregate
7. **`.github/workflows/discover-fonts.yml`** — Monday discovery artifact
8. Fixed **`aggregate.py`** (broken `main()`, style tags before single catalog write)

## How to run
```bash
cd free-font-site
python3 scripts/build_all.py --discover
python3 scripts/serve.py 8080
```

Add a verified font: edit `discovery/approved-candidates.json` → re-run `aggregate.py` or `build_all.py`.

## Next steps
- [ ] Merge PR to `main` and confirm GitHub Pages environment enabled
- [ ] Create Cursor Automation using `docs/cloud-agent-catalog-runbook.md` (weekly license review)
- [ ] Fix Fontshare discover false positives (64 “missing” names)

## Active decisions
- Free Faces = **candidates only**, never auto-merge
- `style_tags` applied every aggregate run from taxonomy + manual tags on approved entries
- Reports in `discovery/reports/` stay local/CI artifacts (gitignored)
