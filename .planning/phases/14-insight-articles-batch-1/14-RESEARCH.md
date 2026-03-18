# Phase 14: Insight Articles Batch 1 - Research

**Researched:** 2026-03-17
**Domain:** Static site content generation (Python build system, Article JSON-LD, insight articles)
**Confidence:** HIGH

## Summary

Phase 14 adds 10 insight articles at `/insights/[slug]/` with an index page at `/insights/`. The existing codebase has a proven pattern for long-form content pages via the `/blog/` section (14 articles, each as a standalone `build_blog_*()` function in `build.py`). The insight articles follow an identical technical pattern but live under a new `/insights/` URL prefix and use Article JSON-LD schema (new for this project, not yet implemented in templates.py).

The build system is a 3-file Python split: `build.py` (data + generators), `templates.py` (HTML components + schema helpers), `nav_config.py` (nav/footer/constants). Each page is a function that constructs HTML, calls `get_page_wrapper()`, and writes via `write_page()`. Content modules in `content/` handle prose but are optional (pages render with defaults if missing). The insights articles will follow the blog article pattern: inline content in build.py functions, no content module needed.

**Primary recommendation:** Clone the blog article pattern exactly. Add an `article_schema()` helper to templates.py for Article + Person JSON-LD. Build 10 `build_insight_*()` functions and one `build_insights_index()` function. Add "insights/" to `DATA_DIRS` in the validator. Update nav_config.py to include Insights in the nav dropdown and footer.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| ART-01 | Job market analysis article | Blog article function pattern, uses job posting stats from existing data references |
| ART-02 | Salary trends deep dive | Blog article pattern, references salary data already in build.py |
| ART-03 | Tool adoption report | Blog article pattern, references tool categories already in build.py |
| ART-04 | State of GTME 2026 summary | Blog article pattern, REPORT_CITATION constant already exists |
| ART-05 | Clay ecosystem breakdown | Blog article pattern, Clay data in tool reviews |
| ART-06 | Outbound automation stack guide | Blog article pattern (playbook format) |
| ART-07 | Building first Clay table playbook | Blog article pattern (step-by-step playbook) |
| ART-08 | LinkedIn outreach automation playbook | Blog article pattern (playbook) |
| ART-09 | Email deliverability guide | Blog article pattern (playbook) |
| ART-10 | API integration patterns guide | Blog article pattern (playbook) |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python 3 | 3.x | Static site generator | Existing build system |
| build.py | N/A | Page generator functions | All pages built here |
| templates.py | N/A | HTML components + schema helpers | `write_page()`, `get_page_wrapper()`, `get_breadcrumb_schema()` |
| nav_config.py | N/A | Nav items, footer columns, site constants | `NAV_ITEMS`, `FOOTER_COLUMNS`, `CSS_VERSION` |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| json (stdlib) | N/A | JSON-LD schema generation | Article schema markup |
| re (stdlib) | N/A | Validation patterns | Word count, link checks in `validate_pages()` |

### Alternatives Considered
None. The build system is fixed. No external dependencies needed.

## Architecture Patterns

### Recommended Structure

No new files or directories needed. Everything goes into existing files:

```
scripts/
  build.py       # Add INSIGHT_PAGES list, build_insights_index(), 10x build_insight_*() functions
  templates.py   # Add get_article_schema() helper
  nav_config.py  # Update NAV_ITEMS + FOOTER_COLUMNS to include /insights/
```

### Pattern 1: Article Page Function (clone of blog pattern)

**What:** Each insight article is a standalone function in build.py that constructs inline HTML content.

**When to use:** Every ART-* requirement.

**Example (derived from existing blog pattern at line 10549):**
```python
INSIGHT_PAGES = [
    {"slug": "job-market-analysis-2026", "title": "GTM Engineer Job Market: 2026 Analysis", ...},
    # ... 10 entries
]

BUILT_INSIGHT_SLUGS = {"job-market-analysis-2026", ...}  # Track which are implemented

def insight_related_links(current_slug):
    """Generate related insight article links plus cross-section links."""
    links = [("/insights/", "Insights Index")]
    for page in INSIGHT_PAGES:
        if page["slug"] != current_slug and page["slug"] in BUILT_INSIGHT_SLUGS:
            links.append((f"/insights/{page['slug']}/", page["title"]))
    # Cross-section links
    links.append(("/salary/", "Salary Data"))
    links.append(("/tools/", "Tool Reviews"))
    links.append(("/blog/", "Blog"))
    links.append(("/careers/", "Career Guides"))
    related_html = '<div class="related-links"><h2>More Insights</h2><ul>'
    for href, label in links:
        related_html += f'<li><a href="{href}">{label}</a></li>'
    related_html += '</ul></div>'
    return related_html

def build_insight_job_market():
    """ART-01: Job market analysis article."""
    title = "GTM Engineer Job Market: 2026 Analysis"
    description = pad_description("...")
    crumbs = [("Home", "/"), ("Insights", "/insights/"), ("Job Market Analysis", None)]
    bc_html = breadcrumb_html(crumbs)

    # Article schema (new helper from templates.py)
    article_schema = get_article_schema(
        title=title,
        description=description,
        slug="job-market-analysis-2026",
        date_published="2026-03-17",
        word_count=2000,
    )

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Insights</div>
        <h1>{title}</h1>
        <p class="byline"><strong>By Rome Thorndike</strong> | March 2026</p>
    </div>
</section>
<div class="salary-content">
    ... 1,500-2,500 words of content ...
    {insight_related_links("job-market-analysis-2026")}
</div>'''
    body += source_citation_html()
    body += newsletter_cta_html("Weekly GTM job market data.")

    extra_head = get_breadcrumb_schema(crumbs) + article_schema
    page = get_page_wrapper(
        title=title, description=description,
        canonical_path="/insights/job-market-analysis-2026/",
        body_content=body, active_path="/insights/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("insights/job-market-analysis-2026/index.html", page)
```

### Pattern 2: Article JSON-LD Schema (new helper for templates.py)

**What:** Generate Article schema with author Person markup per CLAUDE.md requirement.

**Example:**
```python
def get_article_schema(title, description, slug, date_published, word_count):
    """Generate Article JSON-LD with author Person markup."""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "author": {
            "@type": "Person",
            "name": "Rome Thorndike",
            "url": f"{SITE_URL}/about/",
        },
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": SITE_URL,
        },
        "datePublished": date_published,
        "dateModified": date_published,
        "url": f"{SITE_URL}/insights/{slug}/",
        "wordCount": word_count,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"{SITE_URL}/insights/{slug}/",
        },
    }
    return f'    <script type="application/ld+json">{json.dumps(schema)}</script>\n'
```

### Pattern 3: Insights Index Page (clone of blog index pattern)

**What:** Card grid listing all 10 articles with title, description, and link.

**Example (derived from `build_blog_index()` at line 10472):**
```python
def build_insights_index():
    """Insights index page at /insights/ with card grid."""
    title = "GTM Engineering Insights: Market Data and Playbooks"
    crumbs = [("Home", "/"), ("Insights", None)]
    # Card grid using salary-index-card class (reused across site)
    for page in INSIGHT_PAGES:
        if page["slug"] not in BUILT_INSIGHT_SLUGS:
            continue
        cards_html += f'''<a href="/insights/{page["slug"]}/" class="salary-index-card">
            <h3>{page["title"]}</h3>
            <p>{page["description"]}</p>
        </a>'''
```

### Anti-Patterns to Avoid
- **Content modules for articles:** Blog articles are inline in build.py, not in content/ modules. Insights should follow the same pattern. Content modules are for structural data (tool reviews, comparisons) that share rendering logic.
- **Separate CSS file for insights:** Reuse existing `salary-header`, `salary-content`, `salary-eyebrow`, `salary-stat-card`, `salary-index-card` classes. The blog pages already reuse these successfully.
- **Building all 10 articles in one function:** Each article must be its own function for readability and the `main()` dispatch pattern.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Schema markup | Custom JSON string building | `get_article_schema()` helper | Consistent structure, reusable for Phase 15 |
| Page shell | Custom HTML assembly | `get_page_wrapper()` | Handles nav, footer, JS, CSS automatically |
| Breadcrumbs | Manual breadcrumb HTML | `breadcrumb_html()` + `get_breadcrumb_schema()` | Visual + schema in one call |
| Meta description | Manual string padding | `pad_description()` | Ensures 150-158 char range |
| Related links | Manual link lists | `insight_related_links()` helper | Blog has `blog_related_links()`, mirror it |
| Source citations | Inline citation text | `source_citation_html()` | Standardized citation block |
| Newsletter CTA | Custom CTA blocks | `newsletter_cta_html(context)` | Already wired to signup worker |
| Page registration | Manual file tracking | `write_page()` | Automatically adds to `ALL_PAGES` for sitemap |

## Common Pitfalls

### Pitfall 1: Validation failures from missing DATA_DIRS entry
**What goes wrong:** `validate_pages()` checks word count and source citations only for pages in `DATA_DIRS` (line 11976). If "insights/" is not added to `DATA_DIRS`, insight articles will skip validation entirely.
**How to avoid:** Add `"insights/"` to the `DATA_DIRS` tuple at line 11976.

### Pitfall 2: Word count threshold mismatch
**What goes wrong:** The validator checks `blog/` pages for 1300+ words (line 12106-12108) and generic data pages for 1000+ words (line 12114). The CLAUDE.md target is 1,500-2,500 words for insight articles.
**How to avoid:** Add a specific word count check for `insights/` pages at 1300+ (matching blog threshold). The 1,500 target is a content goal, not a hard validation gate. 1300 is the existing blog floor.

### Pitfall 3: Missing insights/ in SKIP_SOURCE_CITATION exception
**What goes wrong:** All data pages require a source citation (line 12068-12073). Playbook articles (ART-06 through ART-10) may not have survey data citations. They need the "State of GTM" text somewhere in the page, or the validator will flag them.
**How to avoid:** Include at least one reference to the State of GTM Engineering Report or use `source_citation_html()` on every article. The playbook articles can cite the report for context stats even if they're primarily how-to content.

### Pitfall 4: Nav integration gaps
**What goes wrong:** Homepage already links to `/insights/` (line 555), but `NAV_ITEMS` and `FOOTER_COLUMNS` in nav_config.py have no insights entry. Users can't navigate to insights from the nav.
**How to avoid:** Add `/insights/` to the Resources dropdown in `NAV_ITEMS` and to `FOOTER_COLUMNS["Resources"]`.

### Pitfall 5: Em-dash and banned word violations
**What goes wrong:** The validator checks every HTML page for em-dashes (U+2014) and 25+ banned words. With 10 articles of 1,500-2,500 words each, violations are likely if content isn't carefully written.
**How to avoid:** Follow CLAUDE.md writing rules strictly. Use commas and periods instead of em-dashes. Avoid words like "robust", "leverage", "seamless", "enhance", "unlock", "delve", etc.

### Pitfall 6: Internal link minimum not met
**What goes wrong:** Every page needs 3+ internal links in the content body (beyond nav/footer). Short articles may not naturally include enough cross-links.
**How to avoid:** Each article should reference at least 3 other pages on the site (salary pages, tool reviews, career guides, blog articles, glossary terms). The `insight_related_links()` helper generates a related links section, but these must be in addition to inline links within the article body, since the validator counts links between breadcrumb end and footer start.

### Pitfall 7: Title and description length constraints
**What goes wrong:** Title must be 50-60 chars. Description must be 150-158 chars. With 10 articles, it's easy to go over/under.
**How to avoid:** Use `pad_description()` for descriptions. Keep `<title>` tags tight. The H1 can be longer and more descriptive than the `<title>`.

## Code Examples

### Main function dispatch (add to main() around line 12822)
```python
    print("\n  Building insight articles...")
    build_insights_index()
    build_insight_job_market()
    build_insight_salary_trends()
    build_insight_tool_adoption()
    build_insight_state_of_gtme()
    build_insight_clay_ecosystem()
    build_insight_outbound_stack()
    build_insight_clay_playbook()
    build_insight_linkedin_outreach()
    build_insight_email_deliverability()
    build_insight_api_integration()
```

### Validator update (add to DATA_DIRS at line 11976)
```python
DATA_DIRS = ("salary/", "careers/", "tools/", "benchmarks/", "comparisons/", "blog/", "insights/")
```

### Word count check (add after blog check at line 12108)
```python
elif rel.startswith("insights/"):
    if word_count < 1300:
        warnings.append(f"QUAL4-01: {rel}: word count {word_count} (want 1300+ for insight article)")
```

### Nav config update
```python
# In NAV_ITEMS, add to Resources dropdown:
{"href": "/insights/", "label": "Insights"},

# In FOOTER_COLUMNS["Resources"], add:
{"href": "/insights/", "label": "Insights"},
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Blog articles only at /blog/ | Separate /insights/ section for data articles + playbooks | Phase 14 | Blog = opinion pieces (State of GTME data). Insights = market analysis + how-to playbooks. |
| No Article schema | Article JSON-LD with Person author | Phase 14 | Google rich results for article pages |

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Build-time validator in `build.py:validate_pages()` |
| Config file | None (inline in build.py) |
| Quick run command | `cd /Users/rome/Documents/projects/gtmepulse && python3 scripts/build.py 2>&1 \| tail -30` |
| Full suite command | `cd /Users/rome/Documents/projects/gtmepulse && python3 scripts/build.py` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ART-01 | Job market article at /insights/job-market-analysis-2026/ | build validation | `python3 scripts/build.py` | Will be created |
| ART-02 | Salary trends article | build validation | `python3 scripts/build.py` | Will be created |
| ART-03 | Tool adoption article | build validation | `python3 scripts/build.py` | Will be created |
| ART-04 | State of GTME article | build validation | `python3 scripts/build.py` | Will be created |
| ART-05 | Clay ecosystem article | build validation | `python3 scripts/build.py` | Will be created |
| ART-06 | Outbound stack guide | build validation | `python3 scripts/build.py` | Will be created |
| ART-07 | Clay playbook | build validation | `python3 scripts/build.py` | Will be created |
| ART-08 | LinkedIn outreach playbook | build validation | `python3 scripts/build.py` | Will be created |
| ART-09 | Email deliverability guide | build validation | `python3 scripts/build.py` | Will be created |
| ART-10 | API integration guide | build validation | `python3 scripts/build.py` | Will be created |

### Sampling Rate
- **Per task commit:** `python3 scripts/build.py 2>&1 | tail -30` (check for warnings)
- **Per wave merge:** Full build + manual spot-check of 2-3 articles in browser
- **Phase gate:** Zero-warning build, all 10 articles accessible, Article JSON-LD present

### Wave 0 Gaps
- [ ] `get_article_schema()` helper in templates.py (does not exist yet)
- [ ] `insights/` added to `DATA_DIRS` in validator
- [ ] `insights/` word count check added to validator
- [ ] Nav + footer integration for `/insights/`

## Open Questions

1. **Article slugs**
   - What we know: Blog uses short slugs like "equity-gap", "coding-premium". Insights should follow a similar pattern.
   - What's unclear: Exact slug naming convention for 10 articles. Should they be short ("job-market") or descriptive ("gtm-engineer-job-market-analysis-2026")?
   - Recommendation: Use descriptive but not excessively long slugs. Include keywords. Examples: "job-market-2026", "salary-trends", "tool-adoption", "state-of-gtme-2026", "clay-ecosystem", "outbound-stack", "clay-playbook", "linkedin-outreach", "email-deliverability", "api-integration".

2. **Blog vs Insights distinction**
   - What we know: Existing `/blog/` has 14 opinion pieces based on survey data. `/insights/` is for market analysis + playbooks.
   - What's unclear: Should there be cross-links between blog and insights sections?
   - Recommendation: Yes. Include blog articles in `insight_related_links()` cross-section links and vice versa. Both are long-form content targeting the same audience.

3. **Byline date**
   - What we know: Blog articles use "March 2026" format on the byline. Article schema needs ISO 8601 date.
   - Recommendation: Use "March 2026" for visible byline, "2026-03-17" for schema `datePublished`.

## Sources

### Primary (HIGH confidence)
- `/Users/rome/Documents/projects/gtmepulse/scripts/build.py` lines 10426-10654 (blog article pattern)
- `/Users/rome/Documents/projects/gtmepulse/scripts/templates.py` lines 170-321 (page wrapper, schema helpers)
- `/Users/rome/Documents/projects/gtmepulse/scripts/nav_config.py` lines 21-99 (nav items, footer columns)
- `/Users/rome/Documents/projects/gtmepulse/scripts/build.py` lines 11967-12154 (validator)
- `/Users/rome/Documents/projects/gtmepulse/CLAUDE.md` (writing standards, SEO requirements, schema requirements)

### Secondary (MEDIUM confidence)
- Schema.org Article type specification (well-established, stable standard)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - existing codebase, no new dependencies
- Architecture: HIGH - direct clone of proven blog article pattern
- Pitfalls: HIGH - all identified from reading the validator source code
- Content quality: MEDIUM - depends on writing execution, but validation catches issues

**Research date:** 2026-03-17
**Valid until:** 2026-04-17 (stable, no external dependencies)
