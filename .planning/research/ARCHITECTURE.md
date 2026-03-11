# Architecture Patterns

**Domain:** Python static site generator for programmatic SEO (200+ pages)
**Researched:** 2026-03-10
**Confidence:** HIGH (based on direct inspection of 2 production reference implementations: SultanOfSaaS at 145+ pages, b2bsalestools at 196 pages)

## Recommended Architecture

### System Overview

A zero-dependency Python static site generator using f-string HTML generation, structured as a 3-file core with optional content modules and a JSON data layer. No frameworks, no JS build tools, no templating engines. The build script is the entire application: it reads data, generates every HTML page, copies assets, and produces sitemap/robots/CNAME in a single `python3 scripts/build.py` invocation.

```
                       nav_config.py
                      (constants, nav,
                       footer config)
                            |
                            v
 data/*.json -----> build.py -------> templates.py
 (salary data,      (data structs,    (HTML components,
  job postings,      page generators,  schema helpers,
  market stats)      build pipeline)   write_page + ALL_PAGES)
                        |
                        v
                   content/*.py
                   (prose modules,
                    auto-discovered)
                        |
                        v
                    output/
                    (complete static site)
```

### Component Boundaries

| Component | Responsibility | Communicates With | File Size Target |
|-----------|---------------|-------------------|------------------|
| `scripts/build.py` | All structural data (dicts/lists), page generator functions, build orchestration | Imports from templates.py, nav_config.py, content/ | 3,000-5,000 lines |
| `scripts/templates.py` | HTML shell (head/nav/footer/wrapper), write_page(), schema JSON-LD helpers, visual component helpers | Imports from nav_config.py. Exports ALL_PAGES list and OUTPUT_DIR mutable | 300-500 lines |
| `scripts/nav_config.py` | Site constants (name, URL, tagline, CSS_VERSION), NAV_ITEMS list, FOOTER_COLUMNS dict | Pure data, no imports | 80-120 lines |
| `content/*.py` | Extended prose content (overviews, expanded pros/cons, FAQs, long-form analysis) | Loaded by build.py via content/__init__.py auto-discovery | 200-600 lines per module |
| `data/*.json` | Volatile/frequently updated data (salary benchmarks, job counts, market stats) | Read by build.py at build time | Varies |
| `assets/css/` | 3-layer CSS (tokens, components, styles) | Referenced by templates.py HTML head | See CSS section |
| `assets/` (other) | Logos, favicons, images | Copied wholesale to output/ by build.py | Static files |

### Data Flow

```
1. build.py main() starts
2. Clean output/ directory (shutil.rmtree + mkdir)
3. Copy assets/ tree to output/assets/ (shutil.copytree)
4. Set templates.OUTPUT_DIR so write_page() knows where to write
5. For each page type:
   a. Generator function in build.py constructs body HTML from inline data + content modules + JSON data
   b. Calls templates.get_page_wrapper(title, desc, canonical, body) to wrap in full HTML
   c. Calls templates.write_page(rel_path, html) which:
      - Writes file to output/{rel_path}
      - Appends rel_path to ALL_PAGES list
6. After all pages built:
   a. build_sitemap() iterates ALL_PAGES to generate sitemap.xml
   b. build_robots() writes robots.txt with sitemap reference
   c. Write CNAME file (gtmepulse.com)
7. Print build summary with page count
```

## The 3-File Split Pattern (Proven)

This is the core architectural decision. Each file has a strict, non-overlapping responsibility.

### File 1: nav_config.py (Pure Configuration)

**What goes here:** Every site-wide constant and navigational data structure. Zero logic, zero imports.

```python
# scripts/nav_config.py

SITE_NAME = "GTME Pulse"
SITE_URL = "https://gtmepulse.com"
SITE_TAGLINE = "Career intelligence for GTM Engineers"
COPYRIGHT_YEAR = "2026"
CSS_VERSION = "1"

CTA_HREF = "/newsletter/"
CTA_LABEL = "Get the Weekly Pulse"

NAV_ITEMS = [
    {
        "href": "/salary/",
        "label": "Salary Data",
        "children": [
            {"href": "/salary/", "label": "Salary Index"},
            {"href": "/salary/by-seniority/", "label": "By Seniority"},
            {"href": "/salary/by-location/", "label": "By Location"},
            # ...
        ],
    },
    {"href": "/tools/", "label": "Tools"},
    {"href": "/careers/", "label": "Careers"},
    {"href": "/glossary/", "label": "Glossary"},
    {"href": "/newsletter/", "label": "Newsletter"},
]

FOOTER_COLUMNS = {
    "Salary Data": [ ... ],
    "Tools": [ ... ],
    "Resources": [ ... ],
    "Site": [ ... ],
}
```

**Why this boundary matters:** When you need to add a nav item or change the CTA, you edit one 80-line file and rebuild. No risk of breaking page generators or HTML structure. Designers/non-devs can safely edit this file.

### File 2: templates.py (HTML Shell + Helpers)

**What goes here:** Everything that produces reusable HTML fragments. The "chrome" of every page (head, nav, footer, wrapper). Schema markup generators. Component helpers (breadcrumbs, FAQ blocks, newsletter CTAs). The write_page() function and ALL_PAGES tracking list.

**Critical exports:**
- `get_html_head(title, description, canonical_path, og_image, extra_head)` -- meta, fonts, CSS links
- `get_nav_html(active_page)` -- responsive nav with dropdowns + mobile toggle
- `get_footer_html()` -- multi-column footer
- `get_page_wrapper(title, description, canonical_path, body_content, active_page, extra_head)` -- full HTML document
- `write_page(rel_path, content)` -- write to disk + register in ALL_PAGES
- `breadcrumb_html(crumbs)` + `breadcrumb_schema(crumbs)` -- visual + JSON-LD
- `faq_schema_and_html(qa_pairs)` -- FAQPage schema + visible accordion
- `newsletter_cta_html(context)` -- contextual email capture block

**Key design choices:**
- `ALL_PAGES = []` is a module-level mutable list. Every call to `write_page()` appends to it. At the end of the build, `build_sitemap()` iterates this list. This eliminates any need for separate page tracking.
- `OUTPUT_DIR = ""` is set by build.py at startup (`templates.OUTPUT_DIR = OUTPUT_DIR`). This avoids circular imports while keeping write_page() in templates.py where it belongs.
- Inline `<script>` for mobile nav toggle and dropdown behavior goes in `get_page_wrapper()`. No external JS files needed for the core site.

### File 3: build.py (Data + Generators + Pipeline)

**What goes here:** All structured data (inline dicts or JSON loads), every page generator function, and the main() build orchestrator.

**Structure pattern:**
```python
# 1. Imports from templates.py + nav_config.py
# 2. Path constants (OUTPUT_DIR, ASSETS_DIR, BUILD_DATE)
# 3. Set templates.OUTPUT_DIR
# 4. Data structures (inline dicts/lists, or JSON loads from data/)
# 5. Helper/utility functions
# 6. Page generator functions: build_homepage(), build_salary_pages(), etc.
# 7. Sitemap/robots/CNAME generators
# 8. main() orchestrator
# 9. if __name__ == "__main__": main()
```

**Each page generator function:**
1. Constructs body HTML using f-strings + data from module-level dicts
2. Optionally pulls extended prose from content modules
3. Calls `get_page_wrapper()` to wrap in full HTML
4. Calls `write_page()` to write and register

**Data organization for GTME Pulse specifically:**

```python
# Inline in build.py (structural, rarely changes):
SENIORITY_LEVELS = {
    "junior": {"label": "Junior", "range": "$95K-$130K", ...},
    "mid": {"label": "Mid-Level", "range": "$125K-$165K", ...},
    ...
}

LOCATIONS = {
    "san-francisco": {"label": "San Francisco", "median": "$175K", ...},
    ...
}

COMPARISONS = {
    "revops": {"label": "RevOps", "their_range": "$90K-$150K", ...},
    ...
}

# Loaded from data/*.json (volatile, updated by scrapers):
with open(os.path.join(DATA_DIR, "salary_data.json")) as f:
    SALARY_DATA = json.load(f)
```

## Content Module Auto-Discovery

### Pattern

Content modules live in `content/` as Python files exporting a `CONTENT` dict (or domain-specific variant like `TOOL_CONTENT`). The `content/__init__.py` provides a loader that auto-discovers and merges all modules.

```
content/
  __init__.py           # Auto-discovery loader
  salary_insights.py    # Extended prose for salary pages
  tools_enrichment.py   # Tool review deep content
  tools_sequencing.py   # Tool review deep content
  comparisons.py        # Comparison page extended analysis
  career_guides.py      # Career guide long-form content
```

### __init__.py Pattern

```python
"""Content auto-discovery for GTME Pulse."""
import os
import importlib

_ALL_CONTENT = {}
_loaded = False

def _load_all():
    global _loaded
    if _loaded:
        return
    content_dir = os.path.dirname(os.path.abspath(__file__))
    for fname in os.listdir(content_dir):
        if fname.startswith("_") or not fname.endswith(".py"):
            continue
        mod_name = fname[:-3]
        mod = importlib.import_module(f"content.{mod_name}")
        # Each module exports a dict keyed by slug
        for attr in ("CONTENT", "TOOL_CONTENT", "SALARY_CONTENT",
                      "COMPARISON_CONTENT", "CAREER_CONTENT"):
            if hasattr(mod, attr):
                _ALL_CONTENT.update(getattr(mod, attr))
    _loaded = True

def get_content(slug):
    """Return extended content for a slug, or None."""
    _load_all()
    return _ALL_CONTENT.get(slug)
```

### Key Design Principle: Graceful Degradation

Every page generator must render a complete, valid page even when no content module exists for that slug. Content modules add depth (multi-paragraph overviews, expanded analysis, FAQs) but are never required. This means:

- Wave 1 can ship with zero content modules (all data inline in build.py)
- Content modules are added incrementally per page/category
- Build never fails due to missing content

```python
def build_salary_page(slug, data):
    content = get_content(slug)
    overview = ""
    if content and "overview" in content:
        overview = "".join(f"<p>{p}</p>" for p in content["overview"])
    else:
        overview = f"<p>{data['default_overview']}</p>"
    # ... rest of page generation
```

## CSS Architecture (3-Layer System)

### Layer 1: tokens.css (Design Tokens)

Pure CSS custom properties. No selectors beyond `:root` and `@media (prefers-color-scheme: dark)`. This file is generated from the brand kit and rarely edited manually.

```css
:root {
    /* Colors */
    --gtme-accent: #FF4F1F;
    --gtme-bg-primary: #FAFAFA;
    --gtme-bg-surface: #FFFFFF;
    --gtme-text-primary: #111111;
    /* ... */

    /* Typography */
    --font-heading: 'Sora', sans-serif;
    --font-body: 'Plus Jakarta Sans', sans-serif;
    --font-mono: 'Source Code Pro', monospace;

    /* Spacing scale */
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 1.5rem;
    --space-xl: 2rem;
    --space-2xl: 3rem;
    --space-3xl: 4rem;

    /* Radii, shadows, transitions */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
}

@media (prefers-color-scheme: dark) {
    :root { /* dark overrides */ }
}
[data-theme="dark"] { /* explicit dark overrides */ }
```

**Size:** 100-200 lines. Changes here cascade everywhere.

### Layer 2: components.css (Reusable Components)

Styles for components used across multiple page types. Each component is a self-contained block with BEM-ish naming.

```
Components to define:
- .card, .card-grid          (salary cards, tool cards, comparison cards)
- .stat-block, .stat-grid    (hero stats, salary stats)
- .tag, .badge               (seniority tags, location badges, tool categories)
- .btn, .btn--primary, .btn--ghost
- .table-wrap, .data-table   (salary tables, comparison tables)
- .breadcrumb                (visual breadcrumb nav)
- .faq-section, .faq-item    (FAQ accordion)
- .newsletter-cta            (email capture block)
- .related-links             (bottom-of-page link grid)
- .page-header               (standard h1 + subtitle + breadcrumb area)
```

**Size:** 300-500 lines. Add new components as new page types are built.

### Layer 3: styles.css (Page-Specific Styles)

Styles scoped to specific page types or sections. Organized by page type with clear section comments.

```
Sections:
- Site nav (.site-nav, .nav-container, mobile toggle)
- Footer (.site-footer, footer grid)
- Homepage (.hero, .hero-stats, .section-preview)
- Salary pages (.salary-header, .salary-range-visual, .comp-table)
- Tool pages (.tool-header, .tool-score, .verdict-badge)
- Comparison pages (.comparison-header, .comparison-matrix)
- Career pages (.career-header, .skills-grid)
- Glossary pages (.glossary-index, .term-card)
- Responsive overrides (@media queries at the bottom)
```

**Size:** 1,500-2,500 lines. Grows with each wave.

### CSS Cache Busting

`CSS_VERSION` in nav_config.py is appended as `?v={CSS_VERSION}` to the styles.css link (and optionally components.css). Increment on every CSS change. tokens.css does not need cache busting (changes are rare and cascade through variables).

```html
<link rel="stylesheet" href="/assets/css/tokens.css">
<link rel="stylesheet" href="/assets/css/components.css?v={CSS_VERSION}">
<link rel="stylesheet" href="/assets/css/styles.css?v={CSS_VERSION}">
```

## Asset Management

### Directory Structure

```
assets/
  css/
    tokens.css        # Design tokens (from brand kit)
    components.css    # Reusable component styles
    styles.css        # Page-specific styles
  logos/
    logo-horizontal-light.svg
    logo-horizontal-dark.svg
    icon-mark.svg
    wordmark-light.svg
    wordmark-dark.svg
  favicons/
    favicon.svg
    favicon.ico
    favicon-16x16.png
    favicon-32x32.png
    apple-touch-icon.png
    android-chrome-192x192.png
    android-chrome-512x512.png
    site.webmanifest
  images/
    og-default.png    # Default OG image
    # Per-page OG images added later
```

### Copy Strategy

The entire `assets/` directory is copied wholesale to `output/assets/` via `shutil.copytree()` at the start of each build. This is simple, fast (< 1 second for typical asset sizes), and guarantees output always matches source. No selective copying, no fingerprinting, no asset pipeline.

```python
# In main():
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR)
shutil.copytree(ASSETS_DIR, os.path.join(OUTPUT_DIR, "assets"))
```

### Image Rules

- Prefer SVG for logos and icons (resolution-independent, small)
- Use WebP for photographs/screenshots (when added in later waves)
- Always include `width` and `height` attributes on `<img>` tags to prevent CLS
- No external image hosting. Everything self-contained in assets/

## Sitemap Generation

Automatic, zero-config. Every call to `write_page()` registers the path. After all pages are built, `build_sitemap()` iterates the list.

```python
def build_sitemap():
    urls = ""
    for page_path in ALL_PAGES:
        if page_path.endswith("index.html"):
            url_path = page_path.replace("index.html", "")
        else:
            url_path = page_path
        if not url_path.startswith("/"):
            url_path = "/" + url_path
        urls += f'  <url>\n    <loc>{SITE_URL}{url_path}</loc>\n    <lastmod>{BUILD_DATE}</lastmod>\n  </url>\n'

    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>'
    write_file(os.path.join(OUTPUT_DIR, "sitemap.xml"), sitemap)
```

This pattern has been verified to correctly handle both `salary/junior/index.html` -> `https://gtmepulse.com/salary/junior/` and flat paths. GitHub Pages serves `/salary/junior/` from `/salary/junior/index.html` automatically.

## Build Pipeline Pattern

### Execution Order (Dependencies Matter)

```
Phase 1: Setup
  1. Clean output/ (shutil.rmtree)
  2. Create output/ directory
  3. Copy assets/ to output/assets/
  4. Set templates.OUTPUT_DIR

Phase 2: Data Loading
  5. Load data/*.json files into module-level dicts
  6. Content modules loaded lazily on first get_content() call

Phase 3: Page Generation (order matters for internal link validation)
  7. Homepage (references all sections, must know what exists)
  8. Core pages (about, newsletter, privacy, terms, 404)
  9. Salary index (needs to know all salary sub-pages)
  10. Salary sub-pages (by-seniority, by-location, by-stage, vs-comparison)
  11. Salary calculator + methodology
  12. [Wave 2+: Tool pages, comparisons, alternatives]
  13. [Wave 3+: Career guides, glossary]
  14. [Wave 4+: Job board, articles]

Phase 4: Meta Files
  15. sitemap.xml (must be last page-related step, uses ALL_PAGES)
  16. robots.txt
  17. CNAME

Phase 5: Report
  18. Print build summary with total page count
```

### Build Performance

At 200 pages, the build completes in under 3 seconds. The SultanOfSaaS build (145 pages, 3,423-line build.py) runs in ~1 second. At 500+ pages, expect 5-8 seconds. No parallelization needed. No incremental builds needed. Full rebuild every time is fast enough and eliminates stale page bugs.

### URL Structure Convention

Every content page uses the `directory/index.html` pattern for clean URLs:

```
output/
  index.html                          -> /
  about/index.html                    -> /about/
  salary/index.html                   -> /salary/
  salary/junior/index.html            -> /salary/junior/
  salary/san-francisco/index.html     -> /salary/san-francisco/
  salary/vs-revops/index.html         -> /salary/vs-revops/
  tools/index.html                    -> /tools/
  tools/clay/index.html               -> /tools/clay/
```

## Patterns to Follow

### Pattern 1: Data Registration Functions

For page types with many instances (tools, salary breakdowns), use a registration function that builds module-level dicts.

```python
SENIORITY_PAGES = {}

def S(slug, label, range_low, range_high, median, ...):
    """Register a seniority salary page."""
    SENIORITY_PAGES[slug] = {
        "slug": slug, "label": label,
        "range_low": range_low, "range_high": range_high,
        "median": median, ...
    }

S("junior", "Junior GTM Engineer", 95000, 130000, 110000, ...)
S("mid", "Mid-Level GTM Engineer", 125000, 165000, 145000, ...)
```

This keeps data declarations compact and readable compared to raw dict literals.

### Pattern 2: Generator Function Per Page Type

Each page type gets its own `build_*()` function that iterates data and generates all pages of that type.

```python
def build_seniority_pages():
    for slug, data in SENIORITY_PAGES.items():
        content = get_content(f"salary-{slug}")
        body = f'''
        <section class="page-header">
            {breadcrumb_html([("Home", "/"), ("Salary", "/salary/"), (data["label"], None)])}
            <h1>{data["label"]} Salary ({CURRENT_YEAR})</h1>
            ...
        </section>
        '''
        page = get_page_wrapper(
            f'{data["label"]} Salary - {CURRENT_YEAR} Data',
            f'{data["label"]} salary range: {data["range"]}...',
            f'/salary/{slug}/',
            body,
        )
        write_page(f'salary/{slug}/index.html', page)
```

### Pattern 3: Cross-Linking via Data References

Internal links are generated from data structures, not hardcoded. This ensures links stay valid as pages are added/removed.

```python
def related_salary_links(current_slug):
    """Generate related links section excluding current page."""
    links = []
    for slug, data in SENIORITY_PAGES.items():
        if slug != current_slug:
            links.append(f'<a href="/salary/{slug}/">{data["label"]} Salary</a>')
    # Also pull 2-3 location pages and 2-3 comparison pages
    ...
    return f'<div class="related-links"><h2>Related Salary Data</h2>{"".join(links)}</div>'
```

### Pattern 4: Schema Markup as Template Functions

Schema JSON-LD is generated by helper functions in templates.py, injected via the `extra_head` parameter of `get_page_wrapper()`.

```python
schema = breadcrumb_schema([("Home", "/"), ("Salary", "/salary/"), ("Junior", None)])
schema += faq_schema(page_faqs)
page = get_page_wrapper(title, desc, canonical, body, extra_head=schema)
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Jinja2 or Any Templating Engine
**What:** Adding jinja2, mako, or any templating library.
**Why bad:** Adds a dependency, introduces a second "language" (template syntax), splits HTML generation across .html template files and Python data. The f-string approach keeps everything in Python, is faster, and is easier to debug (just print the string).
**Instead:** f-string HTML in build.py generator functions. Templates.py for reusable shell components.

### Anti-Pattern 2: One Giant build.py
**What:** Putting nav config, HTML helpers, and page generators all in one file.
**Why bad:** At 200+ pages, build.py will be 3,000-5,000 lines. Adding nav/footer/head templates pushes it to 6,000+. A 6,000-line file is painful to navigate and creates merge conflicts when multiple things change.
**Instead:** The 3-file split. nav_config.py is ~100 lines. templates.py is ~400 lines. build.py stays focused on data + generators.

### Anti-Pattern 3: External Data for Everything
**What:** Moving all data to JSON/YAML files, even structural data that rarely changes.
**Why bad:** Adds indirection. You need to open two files (data file + build.py) to understand a page. JSON lacks comments, can't have computed fields, and is harder to diff in code review.
**Instead:** Inline data in build.py for structural/rarely-changing data (tool names, categories, seniority levels). JSON in data/ only for volatile data updated by external processes (scraper outputs, market stats).

### Anti-Pattern 4: Incremental Builds
**What:** Only rebuilding pages whose source data changed.
**Why bad:** Internal links, nav items, and footer content appear on every page. A nav change requires rebuilding all 200+ pages anyway. Incremental build logic adds complexity for near-zero benefit when full builds take < 5 seconds.
**Instead:** Full rebuild every time. `shutil.rmtree(OUTPUT_DIR)` at the start.

### Anti-Pattern 5: Client-Side Rendering for Data
**What:** Shipping JSON to the browser and rendering salary tables/charts with JavaScript.
**Why bad:** Search engines may not execute JS reliably. Programmatic SEO depends on content being in the HTML source. Also adds unnecessary complexity.
**Instead:** All data rendered as static HTML at build time. JavaScript only for interactivity (mobile nav toggle, salary calculator input handling, newsletter form submission).

## Suggested Build Order (Implementation Phases)

Dependencies flow top-to-bottom. Each step depends on the one above.

```
Step 1: nav_config.py + templates.py skeleton
  - Site constants, nav structure, footer columns
  - get_html_head, get_nav_html, get_footer_html, get_page_wrapper, write_page
  - breadcrumb_html, breadcrumb_schema
  WHY FIRST: Every page depends on these. Build the shell before any content.

Step 2: CSS foundation (tokens.css already exists, add components.css + styles.css)
  - tokens.css: already in project from brand kit
  - components.css: cards, buttons, tags, tables, breadcrumbs, CTA blocks
  - styles.css: nav, footer, homepage hero, page-header pattern
  WHY SECOND: Pages need styles to look right during development/preview.

Step 3: build.py skeleton + core pages
  - main() pipeline (clean, copy assets, generate, sitemap, robots, CNAME)
  - Homepage, About, Newsletter, Privacy, Terms, 404
  WHY THIRD: Proves the full pipeline end-to-end with simple pages.

Step 4: Salary data structures + salary page generators
  - Inline salary data dicts (seniority, location, stage, comparison)
  - build_salary_index(), build_seniority_pages(), build_location_pages(),
    build_stage_pages(), build_comparison_pages()
  - faq_schema_and_html() for comparison/breakdown pages
  - newsletter_cta_html() for email capture blocks
  WHY FOURTH: Salary is the anchor differentiator. 35+ pages from data structures.

Step 5: content/ module system
  - content/__init__.py auto-discovery
  - salary_insights.py (extended prose for salary pages)
  WHY FIFTH: Pages already render without content modules. This adds depth.

Step 6: Newsletter infrastructure
  - Cloudflare Worker for signup (worker/subscribe.js)
  - Wire handleSignup() JS into newsletter CTA blocks
  WHY SIXTH: Depends on pages existing to embed the form.

Step 7 (Wave 2): Tool data + tool page generators
Step 8 (Wave 3): Career guides + glossary
Step 9 (Wave 4): Job board + articles + email automation
```

## Scalability Considerations

| Concern | At 50 pages (Wave 1) | At 200 pages (Wave 2) | At 500+ pages (Wave 4) |
|---------|----------------------|----------------------|----------------------|
| Build time | < 1 second | 2-3 seconds | 5-8 seconds |
| build.py size | ~1,500 lines | ~3,500 lines | ~5,000 lines (consider splitting generators into separate files) |
| Content modules | 0-1 modules | 5-8 modules | 10-15 modules |
| Data files | 1-2 JSON files | 3-5 JSON files | 5-8 JSON files |
| Memory | Negligible | Negligible | Negligible (all text, no images in memory) |

At 500+ pages, consider splitting build.py generator functions into separate files (e.g., `scripts/generators/salary.py`, `scripts/generators/tools.py`) imported by build.py. But this is a Wave 4 concern, not a Wave 1 concern. Don't prematurely split.

## Sources

- SultanOfSaaS production codebase: `/Users/rome/Documents/projects/sultanofsaas/scripts/` (3,847 lines across 3 files, 145+ pages, direct inspection)
- b2bsalestools production codebase: `/Users/rome/Documents/projects/b2bsalestools/build.py` (2,988 lines, 196 pages, direct inspection)
- GTME Pulse CLAUDE.md architecture spec (defines the target pattern)
- GTME Pulse PROJECT.md requirements (defines page types and waves)
