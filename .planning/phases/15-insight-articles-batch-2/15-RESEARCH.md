# Phase 15: Insight Articles Batch 2 - Research

**Researched:** 2026-03-18
**Domain:** Static site content generation (Python build system, insight article expansion)
**Confidence:** HIGH

## Summary

Phase 15 adds 10 more insight articles at `/insights/[slug]/` following the identical pattern established in Phase 14. All infrastructure is already built: `get_article_schema()` helper in templates.py, `INSIGHT_PAGES` list, `BUILT_INSIGHT_SLUGS` set, `insight_related_links()` helper, `build_insights_index()` with card grid, validator checks for insights/ pages, and nav/footer integration. The only work is: (1) add 10 new entries to `INSIGHT_PAGES`, (2) add 10 new slugs to `BUILT_INSIGHT_SLUGS`, (3) write 10 new `build_insight_*()` functions, and (4) add 10 new dispatch calls in `main()`.

ART-17 (monthly pulse report template) is the one article with a special requirement: it must pull data from existing JSON data files. The `data/jobs.json` file exists with structured job posting data (title, company, location, salary, remote flag, seniority, posted date). The article can read this JSON at build time and render current stats into the page. This follows the same pattern used by `build_job_board()` which already loads `data/jobs.json` at line 13544.

**Primary recommendation:** Clone the exact Phase 14 article function pattern for all 10 articles. Add all 10 entries to `INSIGHT_PAGES` and `BUILT_INSIGHT_SLUGS`. For ART-17, load `data/jobs.json` at the top of the function and render aggregate stats inline. The insights index will automatically display all 20 articles via the existing `build_insights_index()` logic. build.py is currently 14,123 lines; expect it to grow to ~15,200 lines.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| ART-11 | Data enrichment waterfall strategy article | Standard insight article pattern, references tool categories and enrichment tools already in build.py |
| ART-12 | GTM Engineer hiring guide for managers | Standard insight article pattern, references salary data and career content |
| ART-13 | Freelance GTM Engineering rate guide | Standard insight article pattern, references salary and career pages |
| ART-14 | GTM Engineer vs SDR team ROI analysis | Standard insight article pattern, references salary comparisons already built |
| ART-15 | Intent data buying guide | Standard insight article pattern, references intent data tool category |
| ART-16 | CRM hygiene automation playbook | Standard insight article pattern, references CRM tool category |
| ART-17 | Monthly pulse report template page (auto-populated from data) | Loads data/jobs.json at build time, renders aggregate stats. Pattern from build_job_board() |
| ART-18 | GTM Engineer tech stack audit checklist | Standard insight article pattern, references all tool categories |
| ART-19 | Revenue attribution for GTM Engineers | Standard insight article pattern, references analytics tool category |
| ART-20 | Remote GTM Engineering market report | Standard insight article pattern, references salary by-location and remote data |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python 3 | 3.x | Static site generator | Existing build system |
| build.py | N/A | Page generator functions | All pages built here, 14,123 lines |
| templates.py | N/A | HTML components + schema helpers | `write_page()`, `get_page_wrapper()`, `get_article_schema()` |
| nav_config.py | N/A | Nav items, footer columns, site constants | Already has /insights/ in nav and footer |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| json (stdlib) | N/A | JSON-LD schema + data file loading | Article schema + ART-17 data pull |

### Alternatives Considered
None. The build system is fixed. No new dependencies needed.

## Architecture Patterns

### No New Files or Directories Needed

Everything goes into existing files:

```
scripts/
  build.py       # Extend INSIGHT_PAGES list, add 10 build_insight_*() functions, add main() calls
```

### Pattern 1: Article Page Function (established in Phase 14)

**What:** Each insight article is a standalone function in build.py with inline HTML content.
**When to use:** Every ART-* requirement.

**Exact pattern (from existing Phase 14 articles at line 12079):**
```python
def build_insight_enrichment_waterfall():
    """ART-11: Data enrichment waterfall strategy."""
    title = "Data Enrichment Waterfall Strategy for GTM Engineers"
    description = pad_description("Multi-vendor enrichment pipelines, cost optimization, and accuracy benchmarks for GTM data operations.")

    crumbs = [("Home", "/"), ("Insights", "/insights/"), ("Enrichment Waterfall", None)]
    bc_html = breadcrumb_html(crumbs)
    article_schema = get_article_schema(title=title, description=description, slug="enrichment-waterfall", date_published="2026-03-18", word_count=XXXX)

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Playbook</div>
        <h1>{title}</h1>
        <p>Subtitle line.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">XX</span>
        <span class="stat-label">Label</span>
    </div>
    <!-- 3-4 stat cards -->
</div>

<div class="salary-content">
    <p class="byline"><strong>By Rome Thorndike</strong> | March 2026</p>
    <!-- 1,500-2,500 words with h2/h3 sections, 3+ internal links, 2+ outbound citations -->
    {insight_related_links("enrichment-waterfall")}
</div>'''
    body += source_citation_html()
    body += newsletter_cta_html("Context-specific CTA.")

    extra_head = get_breadcrumb_schema(crumbs) + article_schema
    page = get_page_wrapper(title=title, description=description, canonical_path="/insights/enrichment-waterfall/",
        body_content=body, active_path="/insights/", extra_head=extra_head, body_class="page-inner")
    write_page("insights/enrichment-waterfall/index.html", page)
    print(f"  Built: insights/enrichment-waterfall/index.html")
```

### Pattern 2: ART-17 Data-Driven Pulse Report Template

**What:** Load `data/jobs.json` at build time and render aggregate stats into the article.
**When to use:** ART-17 only.

**Example (derived from build_job_board() at line 13544):**
```python
def build_insight_pulse_report():
    """ART-17: Monthly pulse report template page."""
    # Load current job data
    jobs_path = os.path.join(DATA_DIR, "jobs.json")
    jobs = []
    if os.path.exists(jobs_path):
        with open(jobs_path, "r", encoding="utf-8") as f:
            jobs = json.load(f)

    total_roles = len(jobs)
    remote_count = sum(1 for j in jobs if j.get("remote"))
    remote_pct = round(remote_count / total_roles * 100) if total_roles > 0 else 0
    salaries = [j["salary_min"] for j in jobs if j.get("salary_min")]
    median_salary = sorted(salaries)[len(salaries)//2] if salaries else 0

    # Use stats in article content...
```

### Pattern 3: INSIGHT_PAGES List Extension

**What:** Add 10 new entries to the existing INSIGHT_PAGES list at line 11967.
**When to use:** Phase 15 setup.

```python
# Add after existing 10 entries in INSIGHT_PAGES:
    {"slug": "enrichment-waterfall", "title": "Data Enrichment Waterfall Strategy", "description": "...", "category": "Playbook"},
    {"slug": "hiring-guide", "title": "GTM Engineer Hiring Guide for Managers", "description": "...", "category": "Guide"},
    {"slug": "freelance-rates", "title": "Freelance GTM Engineering Rate Guide", "description": "...", "category": "Market Analysis"},
    {"slug": "gtme-vs-sdr-roi", "title": "GTM Engineer vs SDR Team: ROI Analysis", "description": "...", "category": "Market Analysis"},
    {"slug": "intent-data-guide", "title": "Intent Data Buying Guide for GTM Engineers", "description": "...", "category": "Guide"},
    {"slug": "crm-hygiene", "title": "CRM Hygiene Automation Playbook", "description": "...", "category": "Playbook"},
    {"slug": "pulse-report-template", "title": "Monthly GTM Pulse Report Template", "description": "...", "category": "Template"},
    {"slug": "tech-stack-audit", "title": "GTM Engineer Tech Stack Audit Checklist", "description": "...", "category": "Guide"},
    {"slug": "revenue-attribution", "title": "Revenue Attribution for GTM Engineers", "description": "...", "category": "Playbook"},
    {"slug": "remote-market-report", "title": "Remote GTM Engineering Market Report", "description": "...", "category": "Market Analysis"},
```

### Anti-Patterns to Avoid
- **Creating new content modules in content/:** Insight articles are inline in build.py, matching blog pattern.
- **New CSS files or classes:** Reuse `salary-header`, `salary-content`, `salary-stats`, `salary-stat-card`, `salary-eyebrow`, `salary-index-card` classes.
- **Modifying build_insights_index():** The existing index function already iterates all `INSIGHT_PAGES` entries in `BUILT_INSIGHT_SLUGS`. Adding new entries to both lists is sufficient. The index will automatically show all 20.
- **Modifying insight_related_links():** The existing helper already iterates all `INSIGHT_PAGES` and caps at 12 links. No changes needed.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Article schema | Custom JSON | `get_article_schema()` in templates.py | Already built in Phase 14 |
| Page shell | Custom HTML | `get_page_wrapper()` | Handles nav, footer, JS, CSS |
| Breadcrumbs | Manual HTML | `breadcrumb_html()` + `get_breadcrumb_schema()` | Visual + schema |
| Meta description | Manual padding | `pad_description()` | Ensures 150-158 char range |
| Related links | Manual link lists | `insight_related_links()` | Already built, auto-updates |
| Source citations | Inline text | `source_citation_html()` | Standardized block |
| Newsletter CTA | Custom blocks | `newsletter_cta_html(context)` | Already wired to signup worker |
| Insights index update | Manual index changes | Just add to INSIGHT_PAGES + BUILT_INSIGHT_SLUGS | Index auto-renders |

## Common Pitfalls

### Pitfall 1: INSIGHT_PAGES list and BUILT_INSIGHT_SLUGS desync
**What goes wrong:** Adding a function without adding the slug to `BUILT_INSIGHT_SLUGS` means the article won't appear in the index or in related links. Adding to `INSIGHT_PAGES` without a matching function means a card with a broken link.
**How to avoid:** Add all 10 entries to `INSIGHT_PAGES` and all 10 slugs to `BUILT_INSIGHT_SLUGS` in the same task as creating the functions.

### Pitfall 2: Em-dash and banned word violations
**What goes wrong:** 10 articles of 1,500-2,500 words = 15,000-25,000 words of content. Banned word violations are statistically likely if not carefully avoided.
**How to avoid:** Follow CLAUDE.md writing rules strictly. The validator catches em-dashes (U+2014) and 25+ banned words. Common traps: "leverage" (use "use"), "enhance" (use "improve" or "strengthen"), "seamless" (just describe the experience), "landscape" (say "market" or "field").

### Pitfall 3: Insufficient internal links
**What goes wrong:** Each article needs 3+ internal links in the body content (between header and footer, not counting nav/related links section). Short or focused articles can miss this.
**How to avoid:** Each article should naturally reference salary pages, tool reviews, career guides, other insight articles, blog posts, or glossary terms. Plan link targets before writing.

### Pitfall 4: Missing outbound citations
**What goes wrong:** CLAUDE.md requires 2+ outbound links to authoritative sources per content page. Phase 14 Plan 04 was entirely dedicated to fixing this gap. Don't repeat that.
**How to avoid:** Include 2+ outbound citations (target="_blank" rel="noopener") in every article from the start. Use authoritative sources: industry reports, vendor documentation, government data (BLS), research papers.

### Pitfall 5: ART-17 data file not found
**What goes wrong:** `data/jobs.json` may have a different path or structure than expected.
**How to avoid:** Use `os.path.exists()` check with fallback defaults (as the job board does at line 13544). If no data file, render with placeholder stats and a note that data updates on next scraper run.

### Pitfall 6: Word count inflation from HTML
**What goes wrong:** The validator strips HTML tags and counts words in the text between `</header>` and `<footer`. Stat cards, breadcrumbs, and related links sections count toward word count. But the 1,300 floor is easy to meet. The real target is 1,500-2,500 words of actual prose.
**How to avoid:** Write 1,500-2,500 words of content. Don't pad with HTML structure.

### Pitfall 7: Title/description length
**What goes wrong:** Title must be 50-60 chars. Description must be 150-158 chars (via `pad_description()`). 10 articles means 10 chances to violate.
**How to avoid:** Check title length before writing. Use `pad_description()` for all descriptions.

### Pitfall 8: main() dispatch calls missing
**What goes wrong:** Writing the function but forgetting to call it in `main()` means the page never builds.
**How to avoid:** Add all 10 calls to `main()` right after the existing insight article calls (after line 14098).

## Code Examples

### INSIGHT_PAGES extension (add after line 11977)
```python
    # Batch 2 (Phase 15)
    {"slug": "enrichment-waterfall", "title": "Data Enrichment Waterfall Strategy", "description": "...", "category": "Playbook"},
    {"slug": "hiring-guide", "title": "GTM Engineer Hiring Guide for Managers", "description": "...", "category": "Guide"},
    # ... 8 more entries
```

### BUILT_INSIGHT_SLUGS extension (update line 11980)
```python
BUILT_INSIGHT_SLUGS = {
    "job-market-2026", "salary-trends", "tool-adoption", "state-of-gtme-2026",
    "clay-ecosystem", "outbound-stack", "clay-playbook", "linkedin-outreach",
    "email-deliverability", "api-integration",
    # Batch 2
    "enrichment-waterfall", "hiring-guide", "freelance-rates", "gtme-vs-sdr-roi",
    "intent-data-guide", "crm-hygiene", "pulse-report-template", "tech-stack-audit",
    "revenue-attribution", "remote-market-report",
}
```

### main() dispatch (add after line 14098)
```python
    build_insight_enrichment_waterfall()
    build_insight_hiring_guide()
    build_insight_freelance_rates()
    build_insight_gtme_vs_sdr_roi()
    build_insight_intent_data()
    build_insight_crm_hygiene()
    build_insight_pulse_report()
    build_insight_tech_stack_audit()
    build_insight_revenue_attribution()
    build_insight_remote_market()
```

### ART-17 data loading pattern
```python
# From build_job_board() at line 13544:
jobs_path = os.path.join(DATA_DIR, "jobs.json")
if os.path.exists(jobs_path):
    with open(jobs_path, "r", encoding="utf-8") as f:
        jobs = json.load(f)
```

### Outbound citation pattern (inline, from Phase 14-04)
```python
# Good: inline within analysis paragraph
'<p>According to <a href="https://www.bls.gov/ooh/..." target="_blank" rel="noopener">Bureau of Labor Statistics data</a>, ...'

# Bad: appended as a list at the end
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 10 insight articles | 20 insight articles (10 + 10) | Phase 15 | Complete content coverage across market analysis, playbooks, guides, and templates |
| Static article content only | ART-17 pulls live data from JSON | Phase 15 | First article with build-time data injection |

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
| ART-11 | Enrichment waterfall article at /insights/enrichment-waterfall/ | build validation | `python3 scripts/build.py` | Will be created |
| ART-12 | Hiring guide article at /insights/hiring-guide/ | build validation | `python3 scripts/build.py` | Will be created |
| ART-13 | Freelance rates article at /insights/freelance-rates/ | build validation | `python3 scripts/build.py` | Will be created |
| ART-14 | GTM vs SDR ROI article at /insights/gtme-vs-sdr-roi/ | build validation | `python3 scripts/build.py` | Will be created |
| ART-15 | Intent data guide at /insights/intent-data-guide/ | build validation | `python3 scripts/build.py` | Will be created |
| ART-16 | CRM hygiene playbook at /insights/crm-hygiene/ | build validation | `python3 scripts/build.py` | Will be created |
| ART-17 | Pulse report template at /insights/pulse-report-template/ | build validation | `python3 scripts/build.py` | Will be created |
| ART-18 | Tech stack audit at /insights/tech-stack-audit/ | build validation | `python3 scripts/build.py` | Will be created |
| ART-19 | Revenue attribution at /insights/revenue-attribution/ | build validation | `python3 scripts/build.py` | Will be created |
| ART-20 | Remote market report at /insights/remote-market-report/ | build validation | `python3 scripts/build.py` | Will be created |

### Sampling Rate
- **Per task commit:** `python3 scripts/build.py 2>&1 | tail -30` (check for warnings)
- **Per wave merge:** Full build + manual spot-check of 2-3 articles in browser
- **Phase gate:** Zero-warning build, all 20 articles accessible, Article JSON-LD present on all

### Wave 0 Gaps
None. All infrastructure was built in Phase 14:
- `get_article_schema()` exists in templates.py
- `insights/` is in `DATA_DIRS` for validation
- `insights/` word count check (1300+ floor) is active
- Nav and footer include /insights/
- `insight_related_links()` helper works
- `build_insights_index()` auto-discovers built slugs

## Suggested Article Slugs and Categories

| Req | Slug | Category | Key Internal Link Targets |
|-----|------|----------|---------------------------|
| ART-11 | enrichment-waterfall | Playbook | /tools/category/data-enrichment/, /tools/clay-review/, /tools/apollo-review/ |
| ART-12 | hiring-guide | Guide | /salary/, /careers/what-is-gtm-engineer/, /careers/gtm-engineer-interview-questions/ |
| ART-13 | freelance-rates | Market Analysis | /salary/, /careers/freelance-consulting/, /insights/salary-trends/ |
| ART-14 | gtme-vs-sdr-roi | Market Analysis | /salary/gtm-engineer-vs-sdr/, /insights/job-market-2026/, /salary/ |
| ART-15 | intent-data-guide | Guide | /tools/category/intent-signal-data/, /comparisons/6sense-vs-bombora/, /tools/ |
| ART-16 | crm-hygiene | Playbook | /tools/category/crm/, /comparisons/hubspot-vs-salesforce/, /glossary/ |
| ART-17 | pulse-report-template | Template | /insights/, /salary/, /jobs/, /insights/job-market-2026/ |
| ART-18 | tech-stack-audit | Guide | /tools/, /tools/category/*, /insights/tool-adoption/, /insights/outbound-stack/ |
| ART-19 | revenue-attribution | Playbook | /tools/category/analytics-product-signals/, /salary/, /careers/ |
| ART-20 | remote-market-report | Market Analysis | /salary/by-location/remote/, /salary/by-location/*, /insights/salary-trends/ |

## Suggested Outbound Citation Sources

| Article | Source 1 | Source 2 |
|---------|----------|----------|
| ART-11 (enrichment waterfall) | Clay docs on enrichment | ZoomInfo/Apollo accuracy reports |
| ART-12 (hiring guide) | LinkedIn Talent Solutions data | Greenhouse hiring benchmarks |
| ART-13 (freelance rates) | Upwork rate reports | Toptal compensation data |
| ART-14 (GTME vs SDR ROI) | Bridge Group SDR metrics | Forrester B2B sales research |
| ART-15 (intent data) | 6sense buyer intent research | Bombora company surge methodology |
| ART-16 (CRM hygiene) | Salesforce data quality reports | HubSpot CRM best practices |
| ART-17 (pulse report) | BLS employment data | LinkedIn Economic Graph |
| ART-18 (tech stack audit) | Gartner MarTech survey | ChiefMartec Marketing Technology Landscape |
| ART-19 (revenue attribution) | Bizible/Marketo attribution models | HubSpot attribution research |
| ART-20 (remote market) | Owl Labs remote work report | LinkedIn remote job trends |

## Open Questions

1. **ART-17 data freshness**
   - What we know: `data/jobs.json` has 7 job entries (as noted in CLAUDE.md). The scraper runs Tue/Fri and will grow this dataset.
   - What's unclear: Whether 7 entries provide enough data for meaningful aggregate stats.
   - Recommendation: Render whatever data exists with a "Last updated: [date]" note. Use fallback stats from the survey data (228 respondents, 3,342 postings analyzed) for context when live data is thin. The template page is about the format/methodology, not the specific numbers.

2. **Category labels for Batch 2**
   - What we know: Phase 14 used "Market Analysis" and "Playbook" categories. Batch 2 introduces "Guide" and "Template" categories.
   - Recommendation: Add "Guide" and "Template" as new category values. The card badge in `build_insights_index()` already renders `page["category"]` dynamically. No code changes needed for new categories.

3. **Build time impact**
   - What we know: build.py is 14,123 lines. Adding 10 more articles (~1,000 lines of code generating ~15,000-25,000 words of HTML) will push it to ~15,200 lines.
   - Recommendation: This is manageable. Content modules are an option for future phases but not needed here. The blog section (14 articles) and Batch 1 insights (10 articles) follow the same inline pattern.

## Sources

### Primary (HIGH confidence)
- `/Users/rome/Documents/projects/gtmepulse/scripts/build.py` lines 11967-11980 (INSIGHT_PAGES, BUILT_INSIGHT_SLUGS)
- `/Users/rome/Documents/projects/gtmepulse/scripts/build.py` lines 11983-12003 (insight_related_links)
- `/Users/rome/Documents/projects/gtmepulse/scripts/build.py` lines 12006-12076 (build_insights_index)
- `/Users/rome/Documents/projects/gtmepulse/scripts/build.py` lines 12079-12185 (build_insight_job_market example)
- `/Users/rome/Documents/projects/gtmepulse/scripts/build.py` lines 13237-13380 (validator: DATA_DIRS, word count, source citation)
- `/Users/rome/Documents/projects/gtmepulse/scripts/build.py` lines 14087-14098 (main dispatch)
- `/Users/rome/Documents/projects/gtmepulse/scripts/build.py` line 13544 (jobs.json loading pattern)
- `/Users/rome/Documents/projects/gtmepulse/data/jobs.json` (job data structure)
- `/Users/rome/Documents/projects/gtmepulse/CLAUDE.md` (writing standards, SEO, schema requirements)
- Phase 14 research, plans, and summaries (established pattern)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - existing codebase, no new dependencies, identical to Phase 14
- Architecture: HIGH - direct clone of proven pattern, all infrastructure exists
- Pitfalls: HIGH - all identified from reading validator source and Phase 14 gap closure history
- Content quality: MEDIUM - depends on writing execution, but validator catches violations

**Research date:** 2026-03-18
**Valid until:** 2026-04-18 (stable, no external dependencies)
