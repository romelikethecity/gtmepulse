# Phase 17: v4.0 Quality Sweep - Research

**Researched:** 2026-03-18
**Domain:** Build validation, content quality, static site integrity
**Confidence:** HIGH

## Summary

Phase 17 is a quality sweep following the same pattern as Phase 12 (v3.0 quality sweep). The current build produces 284 pages with exactly 8 warnings, all of which are QUAL2-04 word count violations on pre-existing tool review and roundup pages (not insight articles). None of the 20 insight articles from Phases 14-15 are triggering warnings.

The build already has a comprehensive `validate_pages()` function (lines 14360-14560 of build.py) that checks: title length (50-60 chars), description length (150-158 chars), H1 count, canonical/OG/Twitter tags, BreadcrumbList schema, internal links (3+), FAQPage schema, SoftwareApplication schema, word counts, source citations, banned words, em-dashes, false reframe patterns, OG image references, and duplicate title/description detection. Insight articles are already covered by the `insights/` prefix in DATA_DIRS, meaning they get word count checks (1300+ floor) and source citation checks.

**Primary recommendation:** Fix the 8 existing word count warnings (add 10-50 words to 7 tool reviews and 1 roundup that are each within 10 words of the 1000-word threshold), then run a full build with OG images to confirm zero warnings and no broken internal links.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| QUAL4-01 | All new article pages pass existing validation (title length, word count, internal links, schema) | validate_pages() already checks all insight articles under `insights/` prefix. Current build shows zero warnings from insight pages. Need to confirm Article JSON-LD schema presence on all 20 articles. |
| QUAL4-02 | Zero-warning build across all ~283+ pages after v4.0 additions | Current build has 8 warnings, all on pre-existing tool pages (word count 990-999 vs 1000 threshold). Fix these to achieve zero warnings. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python 3 | 3.x | Build system | Already used for all builds |
| build.py | ~15,300 lines | Page generation + validation | Single-file build with validate_pages() |
| Playwright | latest | OG image generation | Required for full build (or --skip-og) |

### Supporting
No additional libraries needed. This phase uses only existing tooling.

## Architecture Patterns

### Existing Validation Architecture
```
scripts/build.py
  validate_pages()          # Lines 14360-14560
    QUAL2-01: title length, description length, H1 count
    QUAL2-01: SEO metadata (canonical, OG, Twitter)
    OG-04:    og:image validation
    QUAL2-02: BreadcrumbList schema
    QUAL2-03: Internal links (3+ in content body)
    QUAL2-06: FAQPage on comparison pages
    QUAL2-08: Source citations on data pages
    QUAL2-09: Writing standards (banned words, em-dashes, false reframes)
    QUAL2-04/05: Word counts by page type
    QUAL3-01: SoftwareApplication on tool reviews
    QUAL3-02: FAQPage on comparisons/alternatives/roundups
    QUAL2-07: Duplicate title/description detection
```

### Insight Article Validation Coverage
Insight articles live under `insights/` which is in `DATA_DIRS`, so they get:
- Title length check (50-60 chars)
- Description length check (150-158 chars)
- Single H1 check
- Canonical/OG/Twitter meta tags
- OG image validation (when not --skip-og)
- BreadcrumbList schema check
- Internal links check (3+ required)
- Source citation check (via DATA_DIRS membership)
- Banned word / em-dash / false reframe checks
- Word count check (1300+ for insights/, set at line 14513)

### What Is NOT Checked by validate_pages()
- Article JSON-LD schema (no specific check for `"article"` @type on insight pages)
- Broken internal links (counts links but does not verify targets exist)
- Cross-page link integrity (a link to `/insights/foo/` could point to a nonexistent page)

### Pattern: Quality Sweep Plan (from Phase 12)
The Phase 12 quality sweep was a single plan with two tasks:
1. Task 1: Add new validation checks to validate_pages()
2. Task 2: Fix all warnings to achieve zero-warning build

Phase 17 follows the same pattern but is simpler: no new validation checks need to be added (insight articles are already covered by existing checks). The work is primarily fixing the 8 remaining warnings.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Link checking | Custom crawler | Simple file-existence check in validate_pages() | Only need to verify internal hrefs resolve to files in output/ |
| Article schema validation | Manual spot-check | Add `"article"` @type check to validate_pages() | Automated detection is more reliable than manual review |

## Common Pitfalls

### Pitfall 1: Word Count Marginal Fixes
**What goes wrong:** Adding filler content to hit word count thresholds creates low-quality pages.
**Why it happens:** The 8 failing pages are all within 10 words of 1000 (range: 990-999). Tempting to pad with empty phrases.
**How to avoid:** Add one substantive sentence (pricing detail, use case, integration note) to each page. The content modules for these reviews are in `content/tools_*.py` files. Expand `overview`, `gtm_use_cases`, or `criticism` sections with genuinely useful content.
**Warning signs:** Added text contains banned words or is vague/generic.

### Pitfall 2: OG Image Build Timeout
**What goes wrong:** Running full build with OG generation takes significant time (284 Playwright screenshots).
**Why it happens:** Each screenshot requires browser rendering.
**How to avoid:** Use `--skip-og` for iterative testing. Run full build once at the end for final verification.

### Pitfall 3: Missing Article Schema Check
**What goes wrong:** All 20 articles could be missing Article JSON-LD and the build would still say "all clear."
**Why it happens:** validate_pages() has SoftwareApplication checks for reviews and FAQPage checks for comparisons, but no Article schema check for insight pages.
**How to avoid:** Add a QUAL4-01 check: insight pages matching `insights/*/index.html` (excluding the index itself) should contain `"article"` @type in their JSON-LD. This mirrors the QUAL3-01 pattern.

### Pitfall 4: Broken Internal Links Go Undetected
**What goes wrong:** A page links to `/insights/nonexistent/` and the build says zero warnings.
**Why it happens:** QUAL2-03 counts internal links but does not verify they point to pages that exist in output/.
**How to avoid:** Add a broken link check to validate_pages(): collect all internal hrefs from all pages, verify each resolves to a file in output/. This is the "no broken internal links" success criterion.

## Code Examples

### Current Warning Output (8 warnings, all tool pages)
```
WARNING: QUAL2-04: tools/salesloft-review/index.html: word count 990 (want 1000+ for data page)
WARNING: QUAL2-04: tools/outreach-review/index.html: word count 990 (want 1000+ for data page)
WARNING: QUAL2-04: tools/fullenrich-review/index.html: word count 997 (want 1000+ for data page)
WARNING: QUAL2-04: tools/close-review/index.html: word count 996 (want 1000+ for data page)
WARNING: QUAL2-04: tools/best-workflow-automation-tools/index.html: word count 999 (want 1000+ for data page)
WARNING: QUAL2-04: tools/attio-review/index.html: word count 992 (want 1000+ for data page)
WARNING: QUAL2-04: tools/pipedrive-review/index.html: word count 992 (want 1000+ for data page)
WARNING: QUAL2-04: tools/smartlead-review/index.html: word count 991 (want 1000+ for data page)
```

### Content Module Pattern (where word count fixes go)
```python
# content/tools_crm.py (example)
TOOL_CONTENT = {
    "close": {
        "overview": "...",        # Expand this section
        "gtm_use_cases": "...",   # Or this section
        "criticism": "...",       # Or this section
    },
    # ...
}
```

### Adding Article Schema Check (recommended new validation)
```python
# Inside validate_pages(), after QUAL3-01 block:
# --- QUAL4-01: Article schema on insight pages ---
if re.match(r"insights/[^/]+/index\.html$", rel) and rel != "insights/index.html":
    if '"article"' not in html_lower and '"@type": "article"' not in html_lower:
        warnings.append(f"QUAL4-01: {rel}: insight article missing Article schema")
```

### Adding Broken Link Check (recommended new validation)
```python
# After the per-file loop, before duplicate detection:
# --- QUAL4-02: Broken internal links ---
built_paths = set()
for root2, dirs2, files2 in os.walk(OUTPUT_DIR):
    for f2 in files2:
        rel2 = os.path.relpath(os.path.join(root2, f2), OUTPUT_DIR)
        built_paths.add("/" + rel2.replace("index.html", "").rstrip("/"))
        built_paths.add("/" + rel2)

# Then check all collected internal links against built_paths
```

## State of the Art

| Old Approach (Phase 12) | Current Approach (Phase 17) | Impact |
|------------------------|----------------------------|--------|
| 97 warnings to fix across titles, word counts, citations | 8 warnings, all word count marginal misses | Much smaller scope |
| Added new QUAL3 validation checks | May add QUAL4 checks (Article schema, broken links) | Extends existing validator |
| 263 pages | 284 pages (+21 from v4.0: 20 insights + insights index) | More pages but same validation system |

## Open Questions

1. **Article JSON-LD schema check**
   - What we know: Insight articles should have Article schema per Phase 14 requirements. The validator does not currently check for this.
   - What's unclear: Whether all 20 articles actually have Article schema (they were built to spec, but no automated check enforces it).
   - Recommendation: Add a QUAL4-01 check in validate_pages() for Article schema on insight pages, then fix any failures.

2. **Broken internal link detection**
   - What we know: Success criteria explicitly require "no broken internal links across the entire site." The validator counts internal links but does not verify targets exist.
   - What's unclear: Whether any broken links exist (especially cross-references between insight articles and other sections).
   - Recommendation: Add a broken link check to validate_pages(). Collect all `href="/"` links from all pages, verify each resolves to an existing file in output/. This is a straightforward file-existence check.

3. **OG image completeness**
   - What we know: Phase 16 generated OG images for 284 pages. OG-04 validation already checks og:image tags and file existence.
   - What's unclear: Whether OG images still generate correctly after any content changes in this phase.
   - Recommendation: Run one full build (without --skip-og) as the final verification step.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Python build.py validate_pages() (built-in) |
| Config file | scripts/build.py (lines 14360-14560) |
| Quick run command | `python3 scripts/build.py --skip-og 2>&1 \| grep -E "WARNING\|all clear"` |
| Full suite command | `python3 scripts/build.py 2>&1 \| grep -E "WARNING\|all clear\|Build complete"` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| QUAL4-01 | All 20 insight articles pass validation | integration | `python3 scripts/build.py --skip-og 2>&1 \| grep "insights/"` | Partial (word count/links checked, Article schema not checked) |
| QUAL4-02 | Zero-warning build across all pages | integration | `python3 scripts/build.py --skip-og 2>&1 \| grep "all clear"` | Yes (validate_pages exists) |

### Sampling Rate
- **Per task commit:** `python3 scripts/build.py --skip-og 2>&1 | grep -E "WARNING|all clear"`
- **Per wave merge:** `python3 scripts/build.py 2>&1 | grep -E "WARNING|all clear|Build complete"`
- **Phase gate:** Full build (with OG) must show "Content validation: all clear" and "Build complete: 284 pages"

### Wave 0 Gaps
- [ ] Add QUAL4-01 Article schema check for insight pages in validate_pages()
- [ ] Add broken internal link check in validate_pages() (required by success criteria)

## Sources

### Primary (HIGH confidence)
- scripts/build.py lines 14360-14560: validate_pages() function (read directly)
- scripts/build.py lines 11984-12008: INSIGHT_PAGES and BUILT_INSIGHT_SLUGS (read directly)
- Build output: 8 warnings on 284-page build (executed directly)
- Phase 12 plan and verification: reference pattern for quality sweep phases

### Secondary (MEDIUM confidence)
- CLAUDE.md: Project conventions, writing standards, SEO requirements

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - no new libraries needed, existing build system
- Architecture: HIGH - validate_pages() read directly, warnings captured from live build
- Pitfalls: HIGH - based on direct observation of current build state and validator gaps

**Research date:** 2026-03-18
**Valid until:** 2026-04-18 (stable, no external dependencies)
