# Phase 16: OG Image Generation - Research

**Researched:** 2026-03-18
**Domain:** Playwright-based HTML-to-PNG OG image pipeline integrated into Python static site build
**Confidence:** HIGH

## Summary

This phase adds auto-generated Open Graph images (1200x630 PNG) for all 280+ pages on gtmepulse.com. The approach is straightforward: HTML templates with placeholder variables get rendered by Playwright's Chromium browser and screenshotted to PNG. The existing `og-templates/og-article.html` provides a proven starting template. The build pipeline (`build.py`) needs to call an OG generation step and the `get_html_head()` function needs an `og_image` parameter to inject `og:image` and `twitter:image` meta tags.

Playwright 1.58.0 is already installed on the build machine with working Chromium binaries. A test confirmed `page.set_content()` + `page.screenshot()` works at 1200x630. The main risks are font loading latency (Google Fonts over network) and build time for 280+ screenshots. Both are solvable with `wait_until="networkidle"` on `set_content()` and browser reuse across all pages.

**Primary recommendation:** Create a `scripts/generate_og_images.py` script that reads HTML templates from `og-templates/`, substitutes page-specific variables, renders via Playwright, and saves PNGs to `output/assets/og/`. Integrate as a post-build step in `main()` after all pages are written but before `validate_pages()`.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| OG-01 | Playwright-based OG image generator script (reads HTML templates, screenshots to PNG) | Playwright 1.58.0 installed, `set_content()` + `screenshot()` pattern verified working. Use sync API with single browser instance. |
| OG-02 | OG image HTML templates for each page type (salary, tool review, comparison, article, glossary) | Existing `og-article.html` template provides the design pattern. Need 5-6 template variants with `{{TITLE}}` / `{{SUBTITLE}}` / `{{CATEGORY}}` placeholders. |
| OG-03 | Build integration (generate OG images as part of build.py pipeline) | Call `generate_og_images()` in `main()` after all pages built, before `validate_pages()`. Uses `ALL_PAGES` list to know what pages exist. |
| OG-04 | All 280+ pages reference their generated OG image in meta tags | Add `og_image` parameter to `get_html_head()`. Requires either two-pass build (build pages, generate OG images, re-inject tags) or pre-compute OG image paths during page generation. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| playwright | 1.58.0 | Headless Chromium for HTML-to-PNG rendering | Already installed on build machine. Industry standard for programmatic screenshots. |
| Python 3.14 | 3.14 | Build script runtime | Already in use for build.py |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| (none needed) | - | - | Playwright + stdlib is sufficient |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Playwright | Pillow/PIL | No CSS/font rendering. Would need to hand-draw everything. |
| Playwright | puppeteer (Node) | Extra runtime. Python build already established. |
| Dynamic OG (server) | Cloudflare Worker | GitHub Pages is static-only. Pre-generation is the right call. |

**Installation:**
```bash
# Already installed:
pip install playwright  # v1.58.0 present
playwright install chromium  # Binaries present
```

## Architecture Patterns

### Recommended Project Structure
```
gtmepulse/
├── og-templates/
│   ├── og-default.html       # Fallback for core/misc pages
│   ├── og-article.html       # Insights + blog articles (EXISTS)
│   ├── og-salary.html        # Salary data pages (stat highlight)
│   ├── og-tool.html          # Tool reviews + comparisons
│   └── og-glossary.html      # Glossary term pages
├── scripts/
│   ├── generate_og_images.py # OG image generator (new)
│   ├── build.py              # Calls generate_og_images
│   └── templates.py          # Updated get_html_head with og_image
└── output/
    └── assets/
        └── og/               # Generated PNGs (gitignored with output/)
            ├── index.png
            ├── salary-index.png
            ├── salary-junior.png
            └── ...
```

### Pattern 1: Single Browser, Many Screenshots
**What:** Launch one Chromium instance, reuse it for all 280+ pages.
**When to use:** Always. Launching a browser per page would take minutes.
**Example:**
```python
# Source: Verified locally on build machine
from playwright.sync_api import sync_playwright
import os

def generate_og_images(pages_data, output_dir, templates_dir):
    """Generate OG images for all pages using a single browser instance."""
    os.makedirs(os.path.join(output_dir, "assets", "og"), exist_ok=True)

    # Load templates once
    templates = {}
    for tpl_file in os.listdir(templates_dir):
        if tpl_file.endswith(".html"):
            with open(os.path.join(templates_dir, tpl_file)) as f:
                templates[tpl_file.replace(".html", "")] = f.read()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 630})

        for page_info in pages_data:
            template = templates.get(page_info["template"], templates["og-default"])
            html = template.replace("{{TITLE}}", page_info["title"])
            html = html.replace("{{SUBTITLE}}", page_info.get("subtitle", ""))
            html = html.replace("{{CATEGORY}}", page_info.get("category", ""))

            page.set_content(html, wait_until="networkidle")

            og_path = os.path.join(output_dir, "assets", "og", page_info["og_filename"])
            page.screenshot(path=og_path)

        browser.close()
```

### Pattern 2: OG Image Path Convention
**What:** Deterministic OG image filenames derived from page paths.
**When to use:** Always. Makes it trivial to compute og_image path at build time.
**Example:**
```python
def og_filename_from_path(rel_path):
    """Convert page path to OG image filename.

    'salary/junior/index.html' -> 'salary-junior.png'
    'index.html' -> 'index.png'
    'glossary/api/index.html' -> 'glossary-api.png'
    """
    # Strip index.html, join path segments with hyphens
    path = rel_path.replace("/index.html", "").replace(".html", "")
    if not path:
        return "index.png"
    return path.replace("/", "-") + ".png"
```

### Pattern 3: Page Data Registry for OG Generation
**What:** Build a list of page metadata (title, subtitle, category, template type) alongside page generation, then pass to OG generator.
**When to use:** This avoids re-parsing generated HTML to extract titles.
**Example:**
```python
# In build.py, alongside ALL_PAGES tracking:
OG_PAGES = []  # List of dicts: {rel_path, title, subtitle, template, og_filename}

# Each build_* function appends:
OG_PAGES.append({
    "rel_path": "salary/junior/index.html",
    "title": "Junior GTM Engineer Salary",
    "subtitle": "$95K-$120K median base compensation",
    "template": "og-salary",
    "og_filename": "salary-junior.png",
})
```

### Pattern 4: Two-Pass Meta Tag Injection
**What:** First pass builds all pages without og:image tags. Second pass generates OG images and injects the meta tags into existing HTML files.
**When to use:** This is the cleanest approach since it avoids circular dependency (pages need og_image path, but OG images need pages to exist).
**Why this over pre-computing paths:** Pre-computing paths works too, but two-pass is cleaner because: (a) the OG filename convention is fragile if page paths change, (b) the meta tag injection is a simple string replacement, (c) it keeps page generation code unchanged.

**Alternative (simpler): Pre-compute paths inline.** Since the OG filename is deterministic from the page path, `get_html_head()` can compute it at build time without needing the image to exist yet. The image gets generated after. This avoids a second pass entirely.

**Recommendation:** Use the pre-compute approach. Add `og_image` parameter to `get_html_head()` and pass `/assets/og/{computed_name}.png` during page generation. Generate actual PNGs afterward. Simpler, no second HTML rewrite pass needed.

### Anti-Patterns to Avoid
- **Launching a new browser per page:** 280 cold starts would take 5+ minutes. Reuse one browser instance.
- **Loading Google Fonts from CDN in every template:** Network latency multiplied by 280 pages. Use `wait_until="networkidle"` and font caching (Chromium caches across pages in same browser session).
- **Storing OG images in git:** They belong in `output/` which is gitignored. Generated fresh each build.
- **Using full_page=True:** OG cards are exactly 1200x630. Viewport screenshot is correct. `full_page=True` would capture scrollable content.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| HTML to PNG rendering | Canvas/PIL drawing code | Playwright `set_content()` + `screenshot()` | CSS layout, fonts, SVG, gradients all work automatically |
| Font rendering | Bitmap font drawing | Google Fonts in HTML template | Browser handles kerning, anti-aliasing, weights |
| Image optimization | Custom PNG compression | Default Playwright PNG output | OG images are small (1200x630), compression gains minimal |
| Template variable substitution | Jinja2 or custom parser | Simple `str.replace()` | Only 3-4 variables per template. No logic needed. |

**Key insight:** The entire value of Playwright here is that you design OG cards with HTML/CSS (which you already know) and the browser does all the hard rendering work. No image manipulation code needed.

## Common Pitfalls

### Pitfall 1: Google Fonts Not Loaded in Screenshot
**What goes wrong:** OG images render with fallback system fonts instead of Sora/Plus Jakarta Sans.
**Why it happens:** `set_content()` defaults to `wait_until="load"` which may not wait for fonts from Google CDN.
**How to avoid:** Use `page.set_content(html, wait_until="networkidle")` which waits 500ms after last network request. Alternatively, add `page.wait_for_function("document.fonts.ready")` after `set_content()`.
**Warning signs:** OG images look "off" with serif or sans-serif system fonts.

### Pitfall 2: Title Text Overflow
**What goes wrong:** Long page titles overflow the 1200x630 card, getting cut off or wrapping uglily.
**Why it happens:** Some pages have titles up to 60 characters. At 52px font size, that can exceed the max-width.
**How to avoid:** Set `max-width` and rely on CSS `overflow: hidden` / `text-overflow: ellipsis` with `-webkit-line-clamp` for multi-line clamping. Test with longest titles.
**Warning signs:** Titles running off the right edge or overlapping the pulse wave SVG decoration.

### Pitfall 3: Missing OG Image for New Pages
**What goes wrong:** A new page is added to build.py but not registered in the OG generation list, so it has no OG image.
**Why it happens:** OG registration is a separate step from `write_page()`.
**How to avoid:** Either (a) integrate OG metadata collection into `write_page()` itself, or (b) add a validation check that every page in `ALL_PAGES` has a corresponding OG image file.
**Warning signs:** `validate_pages()` can check for missing `og:image` meta tags.

### Pitfall 4: Build Time Explosion
**What goes wrong:** Generating 280+ screenshots takes too long (>2 minutes).
**Why it happens:** Each `set_content()` + font loading + `screenshot()` cycle.
**How to avoid:** Single browser instance (not per-page launch). Font caching across pages. Expect ~0.3-0.5s per page = ~90-140s total. Acceptable for a build that already takes time.
**Warning signs:** Build time doubling. If it becomes a problem, add `--skip-og` flag.

### Pitfall 5: Absolute URL Required for og:image
**What goes wrong:** Social platforms can't find the OG image because the path is relative.
**Why it happens:** Using `/assets/og/foo.png` instead of `https://gtmepulse.com/assets/og/foo.png`.
**How to avoid:** Always use absolute URL with `SITE_URL` prefix in the `og:image` meta tag.
**Warning signs:** Social preview shows no image despite correct HTML.

## Code Examples

### Existing OG Template Structure (from og-templates/og-article.html)
```html
<!-- Source: /Users/rome/Documents/projects/gtmepulse/og-templates/og-article.html -->
<!-- Key features:
  - 1200x630 viewport, dark (#111111) background
  - Sora 700 for title (52px), Plus Jakarta Sans for subtitle
  - Accent color #FF4F1F bar + pulse wave SVG decoration
  - Grid pattern overlay + radial gradient wash
  - Logo mark (orange rounded square + pulse waveform SVG)
  - {{TITLE}} and {{SUBTITLE}} placeholders
-->
```

### Updated get_html_head with og_image Support
```python
# Source: Pattern needed for templates.py
def get_html_head(title, description, canonical_path, extra_head="", og_image=""):
    """Generate complete <head> section."""
    canonical = f"{SITE_URL}{canonical_path}"
    full_title = f"{title} - {SITE_NAME}" if title != SITE_NAME else SITE_NAME

    # OG image meta tags
    og_image_tags = ""
    if og_image:
        og_image_url = f"{SITE_URL}{og_image}"
        og_image_tags = f"""
    <meta property="og:image" content="{og_image_url}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:image" content="{og_image_url}">"""

    # ... rest of head (inject og_image_tags after existing OG tags)
```

### OG Filename Convention
```python
# Source: Deterministic path computation
def og_image_path(rel_path):
    """Compute OG image path from page path.
    'salary/junior/index.html' -> '/assets/og/salary-junior.png'
    'index.html' -> '/assets/og/index.png'
    """
    stem = rel_path.replace("/index.html", "").replace(".html", "")
    filename = stem.replace("/", "-") if stem else "index"
    return f"/assets/og/{filename}.png"
```

### Template Selection Logic
```python
# Source: Pattern for mapping page paths to templates
def og_template_for_path(rel_path):
    """Select OG template based on page path."""
    if rel_path.startswith("salary/"):
        return "og-salary"
    if rel_path.startswith("tools/"):
        return "og-tool"
    if rel_path.startswith("insights/") or rel_path.startswith("blog/"):
        return "og-article"
    if rel_path.startswith("glossary/"):
        return "og-glossary"
    return "og-default"
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| No OG images | Pre-generated PNG via Playwright | Phase 16 | Social shares show branded cards |
| Manual OG image creation (Figma) | Automated from HTML templates | N/A | Scales to 280+ pages without manual work |

**Current state of get_html_head():**
- Has `og:title`, `og:description`, `og:url`, `og:site_name`
- Has `twitter:card`, `twitter:title`, `twitter:description`
- Missing: `og:image`, `og:image:width`, `og:image:height`, `twitter:image`
- The `og_image` parameter mentioned in CLAUDE.md does NOT exist yet in the code. It needs to be added.

**Current state of write_page():**
- Signature: `write_page(rel_path, content)` -- takes pre-assembled HTML
- Does not accept og_image parameter directly
- The og_image injection happens upstream in `get_page_wrapper()` -> `get_html_head()`

**Current state of get_page_wrapper():**
- Signature: `get_page_wrapper(title, description, canonical_path, body_content, active_path="", extra_head="", body_class="")`
- Does not pass og_image to get_html_head()
- Needs `og_image` parameter added

## Open Questions

1. **Should OG images be generated in parallel?**
   - What we know: Playwright supports async API. 280 sequential screenshots at ~0.4s each = ~112s.
   - What's unclear: Whether async provides meaningful speedup (browser is single-threaded internally).
   - Recommendation: Start with sync. Add `--skip-og` flag for dev builds. Optimize only if build time is a problem.

2. **Should template subtitles be page-specific or generic?**
   - What we know: Some page types have natural subtitles (salary pages have dollar ranges, tool reviews have category names).
   - What's unclear: Whether every page warrants a unique subtitle or if category-level defaults suffice.
   - Recommendation: Use page-specific subtitles where data is available (salary ranges, tool categories). Fall back to section-level defaults ("GTM Engineer Career Intelligence", "Tool Review", "GTM Glossary").

3. **How to propagate og_image through 133 write_page call sites?**
   - What we know: Every page goes through `get_page_wrapper()` which calls `get_html_head()`.
   - Recommendation: Add `og_image=""` param to `get_page_wrapper()`. Compute the og_image path inside `get_page_wrapper()` automatically from `canonical_path` using the deterministic convention. This way zero call sites need to change -- the og_image path is auto-derived.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Built-in `validate_pages()` in build.py (no external test framework) |
| Config file | N/A -- validation is inline in build.py |
| Quick run command | `cd /Users/rome/Documents/projects/gtmepulse && python3 scripts/build.py 2>&1 \| tail -20` |
| Full suite command | `cd /Users/rome/Documents/projects/gtmepulse && python3 scripts/build.py` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| OG-01 | Playwright script generates PNGs from HTML templates | smoke | `python3 scripts/generate_og_images.py --dry-run` (check a few pages) | No -- Wave 0 |
| OG-02 | Templates exist for each page type | unit | `ls og-templates/og-*.html \| wc -l` (expect 5+) | Partial (1 exists) |
| OG-03 | Build pipeline generates OG images | integration | `python3 scripts/build.py 2>&1 \| grep "OG images"` | No -- Wave 0 |
| OG-04 | All pages have og:image meta tag | validation | Existing `validate_pages()` extended to check og:image | No -- needs check added |

### Sampling Rate
- **Per task commit:** `python3 scripts/build.py 2>&1 | tail -30` (check OG generation output + zero warnings)
- **Per wave merge:** Full build + manual spot-check of 3-5 OG images
- **Phase gate:** Full build green, all pages have og:image, manual test paste URL into Twitter card validator

### Wave 0 Gaps
- [ ] `scripts/generate_og_images.py` -- OG image generation script
- [ ] `og-templates/og-default.html` -- fallback template
- [ ] `og-templates/og-salary.html` -- salary page template
- [ ] `og-templates/og-tool.html` -- tool page template
- [ ] `og-templates/og-glossary.html` -- glossary page template
- [ ] Add `og:image` / `twitter:image` validation check to `validate_pages()`

## Sources

### Primary (HIGH confidence)
- Playwright Python 1.58.0 -- installed and verified locally on build machine
- Local test: `page.set_content()` + `page.screenshot()` at 1200x630 confirmed working
- Existing template: `og-templates/og-article.html` -- design pattern established
- Existing code: `scripts/templates.py` -- `get_html_head()`, `get_page_wrapper()`, `write_page()` signatures verified

### Secondary (MEDIUM confidence)
- [Playwright Python Screenshots docs](https://playwright.dev/python/docs/screenshots) -- screenshot API parameters
- [Playwright GitHub Issue #18118](https://github.com/microsoft/playwright/issues/18118) -- HTML to image pattern
- [Playwright GitHub Issue #18640](https://github.com/microsoft/playwright/issues/18640) -- Font loading with set_content

### Tertiary (LOW confidence)
- Build time estimates (~0.3-0.5s per page) based on local single-page test, not verified at 280+ page scale

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- Playwright already installed and verified working
- Architecture: HIGH -- Template pattern exists, code integration points identified
- Pitfalls: HIGH -- Font loading and viewport issues are well-documented Playwright behaviors

**Research date:** 2026-03-18
**Valid until:** 2026-04-18 (stable domain, no fast-moving dependencies)
