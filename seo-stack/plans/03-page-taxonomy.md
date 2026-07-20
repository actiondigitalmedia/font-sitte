# Page Taxonomy & Information Architecture

Programmatic page map for font-sitte. Every URL must be generable from `catalog.json` (+ small editorial overlays).

## URL scheme (canonical)

```
/                              Home — browse + trust pitch
/fonts/{slug}/                 Font family entity (PRIMARY)
/category/{category}/          Style hubs (sans-serif, serif, display, handwriting, monospace, …)
/source/{source}/              Source hubs (google-fonts, fontshare, …)
/licenses/{license}/           License hubs (ofl, apache, …)
/tags/{tag}/                   Curated tags (variable, featured, usable-fonts, …)
/use/{use-case}/               Intent hubs (logos, websites, invitations, coding, …)
/commercial-use/               Money-page hub
/alternatives/{paid-slug}/     Later: free alternatives to paid classics
/blog/{slug}/                  Later: editorial only (thin budget)
/sitemap.xml
/robots.txt
```

**Slug rules:** lowercase kebab-case from family name; collision → append source short code.

## Page budgets (what lives on each template)

### `/fonts/{slug}/` — entity page (must rank)

| Block | Source | SEO job |
|-------|--------|---------|
| H1: `{Name} — Free {Category} Font` | catalog | Primary entity |
| License badge + commercial-use yes/no | catalog | Trust + modifier keywords |
| Live specimen (multi-weight) | CSS APIs / preview URLs | Engagement + uniqueness |
| Meta title/description | template | SERP CTR |
| Weights / variable axes | catalog | Unique facts |
| Source + download outbound | catalog | Conversion + E-E-A-T |
| Similar fonts (5–8) | same category / tags | Internal links |
| Pairings (2–3) | heuristic or curated | Depth |
| JSON-LD | template | Entity understanding |
| FAQ (3 Qs, templated) | fields + license | Optional FAQ rich result |

**Do not:** put ads over download; thin AI essay.

### Category / source / license / tag hubs

- H1 intent phrase ("Free Sans Serif Fonts for Commercial Use")
- 80–150 word unique intro (LLM once, human edit, store in `content/hubs/*.md`)
- Grid of top fonts (featured first)
- Pagination: prefer `?page=` with rel next/prev **or** `/page/2/` — pick one; canonicalize page 1
- Links to sibling hubs

### `/use/{use-case}/`

Map use-cases to tags/categories:

| Use case | Mapping heuristic |
|----------|-------------------|
| logos | display, sans, featured |
| websites | sans, serif, variable |
| invitations | handwriting, script, display |
| coding | monospace, nerd-fonts |
| presentations | sans, display |

## Schema (JSON-LD)

Per font page (sketch):

```json
{
  "@context": "https://schema.org",
  "@type": ["CreativeWork", "SoftwareApplication"],
  "name": "Roboto",
  "applicationCategory": "DesignApplication",
  "operatingSystem": "Windows, macOS, Linux",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "license": "https://scripts.sil.org/OFL",
  "isAccessibleForFree": true,
  "creator": { "@type": "Organization", "name": "Google" },
  "url": "https://YOURDOMAIN/fonts/roboto/"
}
```

Plus `BreadcrumbList` and sitewide `WebSite` + `SearchAction` on home.

Templates live in [`../templates/`](../templates/).

## Internal linking graph

```
Home ──► categories, commercial-use, featured
Font ◄──► category, source, license, tags
Font ──► similar fonts, pairings
Hub  ──► top N fonts + sibling hubs
```

**Orphan rule:** every font page ≥ 3 inbound internal links (category + source + ≥1 similar/hub).

**Cannibalization rule:** one primary keyword owner per cluster; alternatives get `rel=related` not competing H1s.

## Facets & crawl budget

| Facet combo | Index? |
|-------------|--------|
| Single category/source/license/tag | Yes |
| Multi-filter browse UI state | Noindex or client-only |
| Sort/pagination deep pages | Canonical to page 1 after N or noindex deep pages |

## Sitemap strategy

Generate at build:

1. `sitemap-fonts.xml` — all families
2. `sitemap-hubs.xml` — categories/sources/licenses/tags/use
3. `sitemap-index.xml`

Submit in GSC after deploy. Cap changefreq realistically (`weekly` catalog, `monthly` hubs).

## From SPA modal → static pages

Current UI uses a detail **modal**. SEO requires:

1. Build static HTML (or SSG) for each font at `/fonts/{slug}/`
2. Keep SPA browse as progressive enhancement **or** link cards to static pages
3. Modal OK as overlay on static URL, not as only representation

Recommended SSG: **Astro** (fast static, simple data load from JSON) or **Eleventy**. Vanilla generator script is fine for v1.
