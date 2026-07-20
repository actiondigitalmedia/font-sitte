# Workflow 01 — Keyword Cluster → Page Map

## Goal

Turn seed keywords into a prioritized map of **which URL owns which query**, without cannibalization.

## Inputs

- Seed list (`seo-stack/data/seeds.txt`)
- Live or planned URL taxonomy (`plans/03-page-taxonomy.md`)
- DataForSEO / OpenSEO MCP

## Seeds (starting set)

```
free fonts
free commercial fonts
free fonts for commercial use
open source fonts
OFL fonts
google fonts download
free sans serif fonts
free serif fonts
free script fonts
free monospace fonts
free fonts for logos
best free fonts for websites
[font name] font
[font name] font download
roboto font
inter font free
```

## Steps

1. **Expand** each seed via Keywords Data / Labs (related + suggestions).
2. **Filter** volume ≥ threshold (start low, e.g. any volume) and relevant to fonts/licenses.
3. **Cluster** by SERP similarity (same top-10 hosts → same cluster) or embedding cluster offline.
4. **Assign owner URL**
   - Exact font name → `/fonts/{slug}/`
   - Style → `/category/{style}/`
   - Commercial/OFL → `/commercial-use/` or `/licenses/ofl/`
   - Use-case → `/use/{case}/`
5. **Export** `keyword-map.csv`: `keyword,volume,kd,cluster,owner_url,priority`
6. **Rank-track** top 50–100 only.

## Cursor prompt (agent)

```
Using OpenSEO/DataForSEO MCP, expand seeds in seo-stack/data/seeds.txt.
Cluster by SERP overlap. Assign each cluster to a URL from plans/03-page-taxonomy.md.
Write seo-stack/data/keyword-map.csv. Do not call Backlinks API.
Cache raw API JSON under seo-stack/data/cache/. Respect spend cap $X.
```

## Outputs

- `seo-stack/data/keyword-map.csv`
- Updated hub priority list for Phase 3

## Cost control

- One expansion pass per seed family
- Cache forever until manual refresh
- No daily re-expansion
