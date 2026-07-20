# Workflow 03 — GSC CTR Repair Loop

## Goal

Raise CTR on URLs that already get impressions.

## Rule

Flag pages where:

- `impressions >= 1000` (adjust down early: 100 while site is new)
- `ctr < 0.02`
- Position roughly 4–20 (title changes help most here)

## Steps

1. Pull last 28 days from Search Console API (page × query).
2. Aggregate by page; compute CTR.
3. For each loser, list top queries.
4. LLM proposes 3 title + meta variants **including commercial-safe modifiers** when relevant.
5. Human/agent picks one; commit; deploy.
6. Annotate date; re-check after 14–28 days.

## Title patterns that work in this niche

```
{Name}: Free {Category} Font (Commercial Use / OFL)
Download {Name} Font Free — {N} Styles, OFL License
{Name} Font Free Download | Open Source {Category}
```

Avoid clickbait ("100% FREE!!!") — trust niche.

## Cursor prompt

```
Connect to GSC export CSV (or API). Filter impressions>=THRESHOLD and ctr<0.02.
For each URL, propose title/meta using templates/title-meta.md and top queries.
Output seo-stack/data/ctr-repair.csv with columns:
url,impressions,ctr,position,top_query,title_current,title_proposed,meta_proposed
```

## Outputs

- `ctr-repair.csv`
- PR updating page frontmatter / meta fields

## Cost

$0 (GSC) + optional tiny LLM spend
