# Phase 1: Build System and HTML Shell - Research

**Researched:** 2026-03-10
**Domain:** Python static site generator build system, CSS architecture, HTML shell with schema markup
**Confidence:** HIGH

## Summary

Phase 1 builds the foundation every subsequent page depends on: the 3-file Python build system (build.py, templates.py, nav_config.py), the 3-layer CSS cascade (tokens.css already exists, components.css and styles.css need creation), the responsive HTML shell (head/nav/footer/wrapper), schema markup helpers (Organization+WebSite, BreadcrumbList, FAQPage), and content standards enforcement (title lengths, meta descriptions, banned words). This is a direct clone of the SultanOfSaaS architecture, which generates 145+ pages from the same pattern. Every technology is proven, every pattern is production-tested, and the tokens.css + all logo/favicon assets already exist in the project.

The build produces a complete output/ directory from a single `python3 scripts/build.py` command using only Python stdlib (os, json, shutil, datetime). No external dependencies. The sitemap, robots.txt, and CNAME are auto-generated. CSS cache-busting uses a `?v=N` query param from nav_config.py. Pages use directory-based clean URLs (salary/junior/index.html serves as /salary/junior/).

**Primary recommendation:** Clone the SultanOfSaaS 3-file pattern directly, adapting brand constants, logo SVG references, font declarations, and token variable names to match GTME Pulse's Volt design direction. Build a minimal test page (or two: one homepage-like, one inner page) to prove the full pipeline end-to-end before Phase 2 adds real content.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| BUILD-01 | 3-file Python build system generates all pages to output/ | Direct clone of SultanOfSaaS pattern. nav_config.py (~100 lines), templates.py (~350-450 lines), build.py (starts ~200 lines for skeleton). |
| BUILD-02 | CSS architecture with 3 layers using design token variables | tokens.css already exists (124 lines). components.css and styles.css need creation. All selectors reference --gtme-* variables. |
| BUILD-03 | write_page() writes HTML and registers in ALL_PAGES for sitemap | Exact pattern from SultanOfSaaS templates.py line 213-219. Module-level ALL_PAGES list, append on every write. |
| BUILD-04 | Auto-generated sitemap.xml from ALL_PAGES | SultanOfSaaS build.py lines 3308-3333. Converts index.html paths to clean URLs. |
| BUILD-05 | Auto-generated robots.txt with sitemap reference | SultanOfSaaS build.py lines 3336-3346. 4-line robots.txt. |
| BUILD-06 | Auto-generated CNAME file (gtmepulse.com) | Single-line file write after sitemap/robots in main(). |
| BUILD-07 | Build copies assets/ to output/ with cache-busted CSS links | shutil.copytree() for assets. CSS_VERSION from nav_config.py appended as ?v=N in get_html_head(). |
| BUILD-08 | Build prints summary with page count | SultanOfSaaS main() pattern: print total from len(ALL_PAGES). |
| HTML-01 | get_html_head() with title, meta, canonical, OG, Twitter, favicons, fonts, CSS | SultanOfSaaS templates.py lines 63-104. Adapt for GTME favicon paths, Google Fonts (Sora/Plus Jakarta Sans/Source Code Pro), and --gtme-* tokens. |
| HTML-02 | get_nav_html() with logo, menu, dropdowns, mobile hamburger, CTA button | SultanOfSaaS templates.py lines 111-140. Adapt logo to use logo-horizontal-light.svg via img tag (not inline SVG). Add CTA button from nav_config CTA_HREF/CTA_LABEL. |
| HTML-03 | get_footer_html() with columns, newsletter mini-signup, copyright | SultanOfSaaS templates.py lines 147-171. Add newsletter mini-form (email input + submit button calling handleSignup()). |
| HTML-04 | get_page_wrapper() assembles full page | SultanOfSaaS templates.py lines 178-206. Includes inline JS for mobile nav toggle and dropdown behavior. |
| HTML-05 | Mobile-responsive at 375px, 768px, 1024px | @media breakpoints in styles.css. Nav collapses to hamburger at 768px. Tables become card stacks below 768px. |
| SEO-01 | Organization + WebSite JSON-LD on homepage (@graph) | New helper function in templates.py. Uses json.dumps() for safe serialization. @graph array combines both types. |
| SEO-02 | BreadcrumbList JSON-LD on all inner pages | SultanOfSaaS templates.py lines 226-245 (get_breadcrumb_schema). Direct clone. |
| SEO-03 | FAQPage JSON-LD on salary breakdown and comparison pages | SultanOfSaaS templates.py lines 248-265 (get_faq_schema). Direct clone. Phase 1 builds the helper; Phase 3 uses it. |
| SEO-04 | All schema uses json.dumps() for safe serialization | Already the pattern in SultanOfSaaS. All schema helpers return `json.dumps(schema)` inside script tags. |
| CONTENT-01 | Title tags 50-60 chars, keyword-first, hyphens not pipes | Enforced in get_html_head(). Title format: `{page_title} - {SITE_NAME}` using hyphens. Build-time validation optional but recommended. |
| CONTENT-02 | Meta descriptions 150-158 chars, action-oriented, unique | Per-page descriptions passed to get_html_head(). Dedup check in build pipeline (compare ALL_PAGES descriptions). |
| CONTENT-03 | One H1 per page, 46-60 chars | Convention enforced by page generator functions. Single h1 in body content. |
| CONTENT-04 | No banned words | Writing convention from CLAUDE.md. Build-time validator can scan generated HTML for banned words list. |
| CONTENT-05 | No em-dashes | Writing convention. Build-time check: scan for unicode em-dash (U+2014) and flag violations. |
| CONTENT-06 | No false reframes | Writing convention. Cannot be automated; enforced during content authoring. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python 3.12+ (stdlib only) | 3.12 in CI, 3.14 local | Static site generator | Runs 5+ production sites in this portfolio. Zero pip dependencies for build. |
| f-string HTML templates | stdlib | Page generation | Proven across SultanOfSaaS (145 pages), b2bsalestools (196 pages). Templates are Python functions, not files. |
| os, json, shutil, datetime | stdlib | File ops, data serialization, asset copying, dates | The only imports needed. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| python3 -m http.server | stdlib | Local preview server | `cd output && python3 -m http.server 8090` during development |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| f-strings | Jinja2 | Adds dependency, file-based templates fight data-driven generation. No benefit. |
| CSS custom properties | Tailwind / Sass | Adds Node build step. Utility classes harder in programmatic HTML. tokens.css already covers everything. |
| Custom build.py | Pelican / Hugo | Wrong paradigm. Pages generated from Python dicts, not Markdown files. |

**Installation:**
```bash
# Zero dependencies. Just run:
python3 scripts/build.py
```

## Architecture Patterns

### Recommended Project Structure
```
scripts/
  build.py          # Data + page generators + main() pipeline
  templates.py      # HTML shell (head/nav/footer/wrapper) + schema helpers + write_page()
  nav_config.py     # Site constants, NAV_ITEMS, FOOTER_COLUMNS (pure data, zero logic)
content/
  __init__.py       # Auto-discovery loader (get_content())
assets/
  css/
    tokens.css      # ALREADY EXISTS (124 lines, all --gtme-* variables)
    components.css  # TO CREATE (cards, buttons, tables, breadcrumbs, CTAs, stat grids)
    styles.css      # TO CREATE (nav, footer, page-type scoped styles, responsive breakpoints)
  logos/            # ALREADY EXISTS (5 SVG files)
  favicons/         # ALREADY EXISTS (12 files including webmanifest)
  images/           # ALREADY EXISTS (empty, for future use)
output/             # Generated site (gitignored)
```

### Pattern 1: 3-File Split
**What:** Strict separation of concerns across nav_config.py (pure config), templates.py (HTML shell + helpers), build.py (data + generators).
**When to use:** Always. This is the architectural foundation.
**Example (nav_config.py):**
```python
# Source: SultanOfSaaS /scripts/nav_config.py (adapted for GTME Pulse)
SITE_NAME = "GTME Pulse"
SITE_URL = "https://gtmepulse.com"
SITE_TAGLINE = "Career intelligence for GTM Engineers"
COPYRIGHT_YEAR = "2026"
CURRENT_YEAR = 2026
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
            {"href": "/salary/by-company-stage/", "label": "By Company Stage"},
            {"href": "/salary/comparisons/", "label": "Comparisons"},
            {"href": "/salary/calculator/", "label": "Salary Calculator"},
        ],
    },
    {"href": "/tools/", "label": "Tools"},
    {"href": "/careers/", "label": "Careers"},
    {"href": "/newsletter/", "label": "Newsletter"},
]

FOOTER_COLUMNS = {
    "Salary Data": [
        {"href": "/salary/", "label": "Salary Index"},
        {"href": "/salary/by-seniority/", "label": "By Seniority"},
        {"href": "/salary/by-location/", "label": "By Location"},
        {"href": "/salary/by-company-stage/", "label": "By Stage"},
        {"href": "/salary/comparisons/", "label": "Comparisons"},
    ],
    "Resources": [
        {"href": "/tools/", "label": "GTM Tools"},
        {"href": "/careers/", "label": "Career Guides"},
        {"href": "/newsletter/", "label": "Newsletter"},
        {"href": "/about/", "label": "About"},
    ],
    "Site": [
        {"href": "/privacy/", "label": "Privacy Policy"},
        {"href": "/terms/", "label": "Terms of Service"},
        {"href": "/salary/methodology/", "label": "Methodology"},
    ],
}
```

### Pattern 2: write_page() + ALL_PAGES Tracking
**What:** Every page write registers the path for automatic sitemap generation.
**When to use:** Every single page generated by build.py.
**Example:**
```python
# Source: SultanOfSaaS /scripts/templates.py lines 213-219
ALL_PAGES = []
OUTPUT_DIR = ""

def write_page(rel_path, content):
    """Write an HTML file and register it for sitemap."""
    full_path = os.path.join(OUTPUT_DIR, rel_path.lstrip("/"))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    ALL_PAGES.append(rel_path)
```

### Pattern 3: Schema Helpers with json.dumps()
**What:** All JSON-LD schema generated by Python functions using json.dumps() for safe serialization.
**When to use:** Every schema block. Never concatenate JSON strings manually.
**Example (Organization + WebSite @graph for homepage):**
```python
def get_homepage_schema():
    """Generate Organization + WebSite @graph schema for homepage."""
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "name": SITE_NAME,
                "url": SITE_URL,
                "description": SITE_TAGLINE,
                "logo": f"{SITE_URL}/assets/logos/icon-mark.svg",
            },
            {
                "@type": "WebSite",
                "name": SITE_NAME,
                "url": SITE_URL,
                "description": SITE_TAGLINE,
            },
        ],
    }
    return f'    <script type="application/ld+json">{json.dumps(schema)}</script>\n'
```

### Pattern 4: CSS 3-Layer Cascade
**What:** tokens.css (variables only) -> components.css (reusable classes) -> styles.css (page-scoped). All selectors reference --gtme-* tokens. Zero hardcoded colors.
**When to use:** All styling. Never add inline styles or !important.
**Key rules:**
- tokens.css: Only `:root` selectors and media queries. No element selectors.
- components.css: BEM-ish naming (.card, .card-grid, .btn, .btn--primary). Reference tokens only.
- styles.css: Page-type scoping via body classes or section classes. Responsive breakpoints at bottom.
- Cache-busted: `?v={CSS_VERSION}` on components.css and styles.css links.

### Pattern 5: build.py main() Pipeline
**What:** Deterministic build order: clean -> copy assets -> set OUTPUT_DIR -> generate pages -> sitemap -> robots -> CNAME -> summary.
**Example:**
```python
# Source: SultanOfSaaS /scripts/build.py lines 3353-3423 (adapted)
def main():
    print(f"\n{'='*60}")
    print(f"  GTME Pulse Build")
    print(f"  {BUILD_DATE}")
    print(f"{'='*60}\n")

    # Clean output
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Copy assets
    shutil.copytree(ASSETS_DIR, os.path.join(OUTPUT_DIR, "assets"))
    print(f"  Copied assets/")

    # Build pages
    print(f"\n  Building pages...")
    build_placeholder_page()  # Phase 1: minimal test page(s)

    # Meta files
    build_sitemap()
    build_robots()

    # CNAME
    with open(os.path.join(OUTPUT_DIR, "CNAME"), "w") as f:
        f.write("gtmepulse.com")
    print("  CNAME")

    # Summary
    total = len(ALL_PAGES)
    print(f"\n{'='*60}")
    print(f"  BUILD COMPLETE: {total} pages generated")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  Preview: cd output && python3 -m http.server 8090")
    print(f"{'='*60}\n")
```

### Anti-Patterns to Avoid
- **Jinja2 or any templating engine:** Adds a dependency, splits HTML across template files and Python data. f-strings keep everything in Python.
- **One giant file:** nav config, HTML helpers, and generators in one file becomes 6,000+ lines. Use the 3-file split.
- **External data for everything:** Structural data belongs inline in build.py as Python dicts. JSON in data/ only for volatile scraper outputs.
- **Incremental builds:** Full rebuild every time. Under 5 seconds at 200 pages. Incremental adds complexity for zero benefit.
- **Client-side rendering:** All data rendered as static HTML at build time. JS only for mobile nav toggle and newsletter form.
- **Hardcoded colors in CSS:** Every color value must reference a --gtme-* token. Zero hex codes in components.css or styles.css.
- **!important declarations:** Zero tolerance. If specificity is wrong, fix the selector, don't force it.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| JSON-LD schema | String concatenation of JSON | `json.dumps()` via schema helper functions | Unescaped quotes, missing commas, and malformed JSON break silently. json.dumps() guarantees valid JSON every time. |
| Responsive nav | Custom JS framework | Inline ~15 lines of vanilla JS (toggle classes) | SultanOfSaaS pattern: classList.toggle on click. No framework needed for a hamburger menu. |
| CSS variable system | Sass variables or JS theming | Native CSS custom properties in tokens.css | Already built. 97%+ browser support. Sass adds a build dependency for zero benefit. |
| Sitemap generation | Manual URL list | Automatic from ALL_PAGES in write_page() | Every page auto-registered. Zero maintenance. |
| Cache busting | Content hashing / fingerprinting | `?v=N` query param from CSS_VERSION | Simple, proven, zero build tooling. Increment the integer when CSS changes. |

**Key insight:** The entire build system has zero external dependencies because Python stdlib handles everything a static site generator needs. Adding any package manager or build tool is pure overhead.

## Common Pitfalls

### Pitfall 1: Circular Import Between build.py and templates.py
**What goes wrong:** build.py imports from templates.py, and templates.py tries to import from build.py for data.
**Why it happens:** Temptation to access build data (like page counts or category lists) from template helpers.
**How to avoid:** templates.py ONLY imports from nav_config.py. build.py imports from both. Data flows one direction: build.py -> templates.py via function arguments. The OUTPUT_DIR is set via `templates.OUTPUT_DIR = OUTPUT_DIR` (mutable module attribute), not an import.
**Warning signs:** ImportError at build time, or templates.py growing data that belongs in build.py.

### Pitfall 2: Mismatched Favicon Paths
**What goes wrong:** Favicon references in HTML head point to wrong paths, causing 404s or missing favicons.
**Why it happens:** Different projects use different favicon directory structures.
**How to avoid:** GTME Pulse favicons are at `/assets/favicons/`. The actual files are: favicon.svg, favicon.ico, favicon-16x16.png, favicon-32x32.png, apple-touch-icon.png, android-chrome-192x192.png, android-chrome-512x512.png, site.webmanifest. Reference these exact paths in get_html_head().
**Warning signs:** Browser tab shows default icon, not the GTME Pulse mark.

### Pitfall 3: Google Fonts Request Bloat
**What goes wrong:** Multiple separate Google Fonts requests instead of one combined request.
**Why it happens:** Adding fonts one at a time without combining into a single URL.
**How to avoid:** Single combined request: `fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Source+Code+Pro:wght@400;500;600;700&display=swap`. Two preconnect hints before it.
**Warning signs:** Lighthouse Performance audit shows multiple font requests.

### Pitfall 4: CSS Variable Name Mismatch
**What goes wrong:** components.css references `--gtme-bg-primary` but tokens.css defines it as `--bg-primary` (or vice versa).
**Why it happens:** Copying from SultanOfSaaS which uses `--sultan-*` or `--sos-*` prefix conventions.
**How to avoid:** GTME Pulse tokens.css already uses `--gtme-*` prefix consistently. All new CSS must use this prefix. Grep for any non-prefixed custom property references before committing.
**Warning signs:** Elements rendering with browser defaults (no background color, wrong font) instead of design tokens.

### Pitfall 5: Mobile Nav Not Toggling
**What goes wrong:** Hamburger menu click does nothing, or dropdown stays open.
**Why it happens:** Inline JS in get_page_wrapper() uses querySelector for specific class names that don't match the HTML.
**How to avoid:** Keep the JS and HTML class names in sync. SultanOfSaaS pattern: `.nav-mobile-toggle` button, `.nav-links` list, `.nav-item--dropdown` for dropdowns. Test at 375px width in browser dev tools.
**Warning signs:** Menu items invisible on mobile, no way to navigate.

### Pitfall 6: Title Tag Format Inconsistency
**What goes wrong:** Some pages use pipes (`|`), some use hyphens (`-`), some append site name, some don't.
**Why it happens:** get_html_head() title formatting logic not consistent.
**How to avoid:** Single format: `{page_title} - GTME Pulse`. Always append site name via get_html_head(). The `title` parameter is the page-specific part only. CONTENT-01 says hyphens not pipes.
**Warning signs:** Google Search Console showing inconsistent title formats.

## Code Examples

Verified patterns from production reference implementations.

### get_html_head() for GTME Pulse
```python
# Adapted from SultanOfSaaS templates.py lines 63-104
def get_html_head(title, description, canonical_path, extra_head=""):
    """Generate complete <head> section."""
    canonical = f"{SITE_URL}{canonical_path}"
    full_title = f"{title} - {SITE_NAME}" if title != SITE_NAME else SITE_NAME

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#FF4F1F">
    <title>{full_title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical}">
    <meta name="robots" content="max-snippet:-1, max-image-preview:large, max-video-preview:-1">

    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{full_title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="{SITE_NAME}">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{full_title}">
    <meta name="twitter:description" content="{description}">

    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="/assets/favicons/favicon.svg">
    <link rel="icon" type="image/x-icon" href="/assets/favicons/favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicons/favicon-16x16.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/favicons/apple-touch-icon.png">
    <link rel="manifest" href="/assets/favicons/site.webmanifest">

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Source+Code+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">

    <!-- CSS -->
    <link rel="stylesheet" href="/assets/css/tokens.css">
    <link rel="stylesheet" href="/assets/css/components.css?v={CSS_VERSION}">
    <link rel="stylesheet" href="/assets/css/styles.css?v={CSS_VERSION}">
{extra_head}
</head>'''
```

### BreadcrumbList Schema Helper
```python
# Source: SultanOfSaaS templates.py lines 226-245 (unchanged)
def get_breadcrumb_schema(items):
    """Generate BreadcrumbList JSON-LD. items = [(label, url), ...]"""
    list_items = []
    for i, (label, url) in enumerate(items, 1):
        item = {"@type": "ListItem", "position": i, "name": label}
        if url:
            item["item"] = f"{SITE_URL}{url}"
        list_items.append(item)

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": list_items,
    }
    return f'    <script type="application/ld+json">{json.dumps(schema)}</script>\n'
```

### Visual Breadcrumb HTML
```python
# Source: SultanOfSaaS templates.py lines 323-331
def breadcrumb_html(crumbs):
    """Generate visual breadcrumb. crumbs = [(label, url), ...] last item is current page."""
    parts = []
    for i, (label, url) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            parts.append(f'<span class="breadcrumb-current">{label}</span>')
        else:
            parts.append(f'<a href="{url}" class="breadcrumb-link">{label}</a><span class="breadcrumb-sep">/</span>')
    return f'<nav class="breadcrumb" aria-label="Breadcrumb">{"".join(parts)}</nav>'
```

### CSS Component Skeleton (components.css)
```css
/* Components to define in Phase 1 */

/* Reset */
*, *::before, *::after { box-sizing: border-box; }
body { margin: 0; font-family: var(--gtme-font-body); color: var(--gtme-text-primary); background: var(--gtme-bg-primary); line-height: 1.65; }

/* Container */
.container { max-width: 1200px; margin: 0 auto; padding: 0 var(--gtme-space-6); }

/* Buttons */
.btn { display: inline-flex; align-items: center; gap: var(--gtme-space-2); padding: var(--gtme-space-3) var(--gtme-space-6); border-radius: var(--gtme-radius-md); font-family: var(--gtme-font-body); font-weight: var(--gtme-weight-semibold); font-size: var(--gtme-text-sm); text-decoration: none; cursor: pointer; transition: all var(--gtme-duration-fast) var(--gtme-ease); border: none; }
.btn--primary { background: var(--gtme-accent); color: var(--gtme-text-on-accent); }
.btn--primary:hover { background: var(--gtme-accent-hover); box-shadow: var(--gtme-shadow-accent); }
.btn--ghost { background: transparent; color: var(--gtme-text-primary); border: 1px solid var(--gtme-border); }

/* Cards */
.card { background: var(--gtme-bg-surface); border: 1px solid var(--gtme-border-subtle); border-radius: var(--gtme-radius-lg); padding: var(--gtme-space-6); }
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: var(--gtme-space-6); }

/* Stat blocks */
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: var(--gtme-space-4); }
.stat-block { text-align: center; }
.stat-value { font-family: var(--gtme-font-mono); font-size: var(--gtme-text-2xl); font-weight: var(--gtme-weight-bold); color: var(--gtme-accent); }
.stat-label { font-size: var(--gtme-text-sm); color: var(--gtme-text-secondary); margin-top: var(--gtme-space-1); }

/* Breadcrumb */
.breadcrumb { font-size: var(--gtme-text-sm); color: var(--gtme-text-secondary); margin-bottom: var(--gtme-space-4); }
.breadcrumb-link { color: var(--gtme-text-secondary); text-decoration: none; }
.breadcrumb-link:hover { color: var(--gtme-accent); }
.breadcrumb-sep { margin: 0 var(--gtme-space-2); }
.breadcrumb-current { color: var(--gtme-text-primary); }

/* Tables */
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: var(--gtme-space-3) var(--gtme-space-4); text-align: left; border-bottom: 1px solid var(--gtme-border-subtle); }
.data-table th { font-weight: var(--gtme-weight-semibold); font-size: var(--gtme-text-sm); color: var(--gtme-text-secondary); }

/* FAQ */
.faq-section { margin-top: var(--gtme-space-12); }
.faq-item { border-bottom: 1px solid var(--gtme-border-subtle); padding: var(--gtme-space-4) 0; }
.faq-question { font-family: var(--gtme-font-heading); font-weight: var(--gtme-weight-semibold); }
.faq-answer { color: var(--gtme-text-secondary); margin-top: var(--gtme-space-2); }

/* Newsletter CTA */
.newsletter-cta { background: var(--gtme-bg-tinted); border-radius: var(--gtme-radius-lg); padding: var(--gtme-space-8); text-align: center; }

/* Page header */
.page-header { padding: var(--gtme-space-12) 0 var(--gtme-space-8); }
.page-header h1 { font-family: var(--gtme-font-heading); font-weight: var(--gtme-weight-bold); letter-spacing: -0.5px; }

/* Related links */
.related-links { margin-top: var(--gtme-space-12); padding-top: var(--gtme-space-8); border-top: 1px solid var(--gtme-border-subtle); }
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Estimated salary schema | Deprecated by Google | Sep 2025 | Do NOT add Occupation/estimatedSalary JSON-LD. It was removed from search results. |
| Sass variables | CSS custom properties | 2020+ (mainstream) | No preprocessor needed. 97%+ browser support. tokens.css uses native properties. |
| Separate font requests | Combined Google Fonts URL | Always best practice | Single request for all 3 families + display=swap. |
| Viewport meta: width=device-width only | width=device-width, initial-scale=1.0 | Standard | Both attributes required for consistent mobile behavior. |

## Open Questions

1. **Newsletter mini-form in footer (Phase 1 vs Phase 2)**
   - What we know: HTML-03 specifies footer with newsletter mini-signup. But the Cloudflare Worker is a Phase 2 deliverable (NEWS-01 through NEWS-06).
   - What's unclear: Should Phase 1 include the form HTML with a non-functional placeholder, or omit it until Phase 2?
   - Recommendation: Include the form HTML structure in Phase 1 (it's part of the footer template). Wire up the JS handler in Phase 2 when the Worker exists. In Phase 1, the form can show a "Coming soon" state or simply collect no submissions.

2. **Test/placeholder page for Phase 1**
   - What we know: Phase 1 builds the system, not content pages. But the build needs at least one page to prove the pipeline works.
   - What's unclear: Build a minimal homepage placeholder, or build a generic test page?
   - Recommendation: Build a minimal index.html (homepage skeleton) and one inner page (e.g., about/index.html placeholder) to validate both the homepage schema (Organization+WebSite) and inner page schema (BreadcrumbList). These get replaced with real content in Phase 2.

3. **Content standards validation automation**
   - What we know: CONTENT-01 through CONTENT-05 are enforceable via build-time checks.
   - What's unclear: Should validation be a separate script or integrated into build.py?
   - Recommendation: Integrate a `validate_pages()` function at the end of main(), after all pages are built. Check title lengths, description lengths, duplicate titles/descriptions, banned words, em-dashes. Print warnings, don't fail the build (to allow WIP during development).

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Python unittest (stdlib) |
| Config file | None needed (stdlib) |
| Quick run command | `python3 -m pytest tests/ -x` or `python3 scripts/build.py && python3 tests/test_build.py` |
| Full suite command | `python3 scripts/build.py && python3 -m pytest tests/ -v` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| BUILD-01 | 3-file build generates pages to output/ | smoke | `python3 scripts/build.py && test -d output` | No (Wave 0) |
| BUILD-03 | write_page() registers in ALL_PAGES | unit | `python3 -c "from scripts.templates import write_page, ALL_PAGES; ..."` | No (Wave 0) |
| BUILD-04 | sitemap.xml contains all page URLs | smoke | `python3 scripts/build.py && grep '<loc>' output/sitemap.xml` | No (Wave 0) |
| BUILD-05 | robots.txt references sitemap | smoke | `python3 scripts/build.py && grep 'Sitemap' output/robots.txt` | No (Wave 0) |
| BUILD-06 | CNAME contains gtmepulse.com | smoke | `python3 scripts/build.py && cat output/CNAME` | No (Wave 0) |
| BUILD-07 | CSS links have ?v= cache bust | smoke | `grep 'v=' output/index.html` | No (Wave 0) |
| HTML-01 | Head has title, meta, OG, fonts, CSS | unit | Check generated HTML for required tags | No (Wave 0) |
| HTML-05 | Responsive breakpoints in CSS | manual-only | Visual check at 375/768/1024px | N/A |
| SEO-01 | Homepage has Organization+WebSite schema | smoke | `grep 'Organization' output/index.html && grep 'WebSite' output/index.html` | No (Wave 0) |
| SEO-02 | Inner pages have BreadcrumbList | smoke | `grep 'BreadcrumbList' output/about/index.html` | No (Wave 0) |
| SEO-04 | Schema uses json.dumps | unit | Verify schema helper functions produce valid JSON | No (Wave 0) |
| CONTENT-01 | Titles 50-60 chars | unit | Parse generated HTML, check title lengths | No (Wave 0) |
| CONTENT-05 | No em-dashes | smoke | `grep -r '\xe2\x80\x94' output/ && echo FAIL \|\| echo PASS` | No (Wave 0) |

### Sampling Rate
- **Per task commit:** `python3 scripts/build.py` (must succeed with zero errors)
- **Per wave merge:** Full build + validate all generated pages
- **Phase gate:** Build succeeds, output/ contains expected files, visual check at 3 breakpoints

### Wave 0 Gaps
- [ ] `tests/test_build.py` -- smoke tests for build output (sitemap, robots, CNAME, page count)
- [ ] `tests/test_templates.py` -- unit tests for schema helpers (valid JSON output, correct structure)
- [ ] `tests/test_content_standards.py` -- title length, description length, banned words, em-dash checks
- [ ] Build-time `validate_pages()` function integrated into main()

## Sources

### Primary (HIGH confidence)
- SultanOfSaaS production codebase: `/Users/rome/Documents/projects/sultanofsaas/scripts/` (templates.py 332 lines, nav_config.py 93 lines, build.py 3,423 lines, content/__init__.py 98 lines -- all directly inspected)
- GTME Pulse assets verified: tokens.css (124 lines), 5 logo SVGs, 12 favicon files all present in project
- GTME Pulse CLAUDE.md architecture spec (defines exact patterns, brand tokens, content standards)

### Secondary (MEDIUM confidence)
- GTME Pulse research documents (.planning/research/ARCHITECTURE.md, STACK.md, SUMMARY.md) -- comprehensive analysis already performed

### Tertiary (LOW confidence)
- None. All findings verified against production code.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- exact clone of 5+ production sites, zero unknowns
- Architecture: HIGH -- direct inspection of SultanOfSaaS reference implementation, every function signature verified
- Pitfalls: HIGH -- based on actual differences between SultanOfSaaS and GTME Pulse (favicon paths, font families, token prefixes, logo format)
- CSS: HIGH -- tokens.css already exists and was inspected; components.css and styles.css follow established pattern

**Research date:** 2026-03-10
**Valid until:** 2026-04-10 (stable patterns, no external API dependencies)
