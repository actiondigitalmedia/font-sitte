# Workflow 04 — Automated Internal Linking

## Goal

Every font page has enough inbound links; hubs push equity to best commercial-safe fonts; avoid cannibalization.

## Data sources

- `catalog.json` (category, source, tags, license)
- Optional: crawl of own site via sitemap (post-deploy)

## Graph rules

1. **Category edge:** font ↔ `/category/{cat}/`
2. **Source edge:** font ↔ `/source/{source}/`
3. **License edge:** font ↔ `/licenses/{license}/`
4. **Similar:** same category, prefer featured / shared tags, exclude self (5–8 links)
5. **Pairings:** sans↔serif heuristic or curated pairs file
6. **Hub injections:** `/commercial-use/` links top N `commercial_use:true` featured fonts

## Orphan detection

```
orphan = inbound_internal_count < 3
```

Emit `orphans.csv` and auto-add similar-font modules.

## Cannibalization check

If two hubs share >40% keyword ownership in `keyword-map.csv`, merge or differentiate H1s.

## Cursor prompt

```
Build link graph from catalog.json using rules in this workflow.
Write link suggestions into build pipeline (not a one-off HTML edit).
Report orphans and overlinked hubs.
```

## Implementation note

Links should be generated at **build time** in the SSG/static builder so 2k pages stay consistent.
