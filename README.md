# font-sitte

Free/libre font catalog aggregation + SEO operations.

## Active workstreams

| Stream | Branch | Status |
|--------|--------|--------|
| Font catalog + browse UI | `cursor/free-font-aggregation-43e3` | PR #1 |
| SEO strategy & stack plans | `cursor/seo-strategy-plans-d92e` | This branch |

## SEO plans + builder

See [`seo-stack/README.md`](seo-stack/README.md) for strategy.

**SSG (locked):** Python + Jinja2 — [`free-font-site/scripts/build_site.py`](free-font-site/scripts/build_site.py), standards in [`free-font-site/seo/STANDARDS.md`](free-font-site/seo/STANDARDS.md).

```bash
cd free-font-site && pip install -r requirements.txt && python3 scripts/build_site.py && python3 scripts/verify_seo.py
```

**Platform:** custom static site (not WordPress). **Goal:** programmatic SEO for commercial-safe free font discovery.
