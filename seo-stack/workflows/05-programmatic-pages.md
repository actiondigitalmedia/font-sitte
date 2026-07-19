# Workflow 05 — Programmatic Page Build

## Goal

Generate thousands of unique-enough static pages from catalog data.

## Pipeline

```
catalog.json
    │
    ├─► build_font_pages()      → /fonts/{slug}/index.html
    ├─► build_hub_pages()       → /category|source|licenses|tags|use/
    ├─► build_sitemap()
    ├─► inject_json_ld()
    └─► inject_internal_links()
```

## Uniqueness checklist (per font page)

Must vary by family:

- [ ] Title / H1 with name + category
- [ ] License name + URL
- [ ] Source name + outbound download
- [ ] Variant/weight list
- [ ] Specimen rendering that family
- [ ] Similar set (computed)
- [ ] Optional: 1–2 sentence "best for" from category×tags heuristic

Optional LLM only if heuristic sentence is identical across many pages.

## Anti-spam rules

1. No spun paragraphs
2. No fake reviews
3. No indexing empty categories
4. No doorway pages for every keyword synonym — cluster owns one URL

## Cursor prompt

```
Implement a static page builder reading free-font-site/data/output/catalog.json
emitting pages per plans/03-page-taxonomy.md and templates/*.
Add npm/python script + CI step. Include tests for slug uniqueness and schema presence.
```

## Acceptance tests

- Random sample 20 pages: unique title, valid JSON-LD, ≥3 internal links
- Sitemap URL count ≈ fonts + hubs
- Lighthouse CWV pass on sample font page (mobile)
