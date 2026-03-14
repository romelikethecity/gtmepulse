---
phase: 09-tool-categories-and-comparisons
plan: 01
subsystem: ui
tags: [html, seo, json-ld, faq-schema, breadcrumbs, content-modules]

# Dependency graph
requires:
  - phase: 08-tool-reviews
    provides: "30 tool review pages with TOOL_REVIEWS data structure and content module pattern"
provides:
  - "8 tool category index pages at /tools/category/[slug]/"
  - "10 tool-vs-tool comparison pages at /tools/[slug]/"
  - "TOOL_CATEGORIES data structure for category page generation"
  - "TOOL_COMPARISONS data structure for comparison page generation"
  - "_load_comparison_content() module loader for comparison prose"
  - "4 comparison content modules (enrichment, outbound, crm, automation)"
affects: [09-02-PLAN, 10-alternatives-and-roundups]

# Tech tracking
tech-stack:
  added: []
  patterns: [comparison content modules with COMPARISONS dict, category index with card grid, tool_comparison_related_links cross-linking]

key-files:
  created:
    - content/comparisons_enrichment.py
    - content/comparisons_outbound.py
    - content/comparisons_crm.py
    - content/comparisons_automation.py
  modified:
    - scripts/build.py
    - scripts/nav_config.py

key-decisions:
  - "Renamed comparison_related_links to tool_comparison_related_links to avoid conflict with pre-existing function"
  - "Category intros inlined in TOOL_CATEGORIES data structure (not separate content modules) due to short length"
  - "Comparison content split across 4 modules by category for maintainability"
  - "lemlist-vs-instantly placed in comparisons_enrichment.py alongside other enrichment matchups despite being cross-category"

patterns-established:
  - "Comparison content module pattern: COMPARISONS dict with intro, feature_table, tool_a_strengths, tool_b_strengths, pricing_comparison, verdict, faq keys"
  - "Category index pattern: TOOL_CATEGORIES list with tools_in_category referencing TOOL_REVIEWS slugs"

requirements-completed: [TCAT-01, TCAT-02, TCAT-03, TCAT-04, TCAT-05, TCAT-06, TCAT-07, TCAT-08, TCMP-01, TCMP-02, TCMP-03, TCMP-04, TCMP-05, TCMP-06, TCMP-07, TCMP-08, TCMP-09, TCMP-10]

# Metrics
duration: 16min
completed: 2026-03-14
---

# Phase 9 Plan 1: Tool Categories & Comparisons Summary

**8 category index pages and 10 head-to-head comparison pages with feature tables, pricing breakdowns, FAQPage schema, and content modules**

## Performance

- **Duration:** 16 min
- **Started:** 2026-03-14T15:45:40Z
- **Completed:** 2026-03-14T16:01:32Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments
- 8 category index pages built with tool card grids linking to reviews
- 10 comparison pages with 3,000-5,000 word content per matchup
- FAQPage JSON-LD schema on all 10 comparison pages (4-5 Q&A each)
- BreadcrumbList JSON-LD schema on all 18 new pages
- Nav dropdown and footer updated with Tool Categories link
- Total page count increased from 163 to 181

## Task Commits

Each task was committed atomically:

1. **Task 1: Build 8 category index pages** - `945e67a` (feat)
2. **Task 2: Build 10 comparison pages with content modules** - `1ea8bd3` (feat)

## Files Created/Modified
- `scripts/build.py` - TOOL_CATEGORIES data, TOOL_COMPARISONS data, generate_category_index(), generate_tool_comparison(), _load_comparison_content(), build functions
- `scripts/nav_config.py` - Added Tool Categories link to nav dropdown and footer
- `content/comparisons_enrichment.py` - Comparison content for clay-vs-apollo, clay-vs-zoominfo, apollo-vs-zoominfo, clay-vs-clearbit, lemlist-vs-instantly
- `content/comparisons_outbound.py` - Comparison content for instantly-vs-smartlead, outreach-vs-salesloft
- `content/comparisons_crm.py` - Comparison content for hubspot-vs-salesforce
- `content/comparisons_automation.py` - Comparison content for make-vs-n8n, make-vs-zapier

## Decisions Made
- Renamed comparison_related_links to tool_comparison_related_links to avoid name collision with pre-existing function at line ~9249
- Category intros kept inline in TOOL_CATEGORIES (150-300 words each, too short for separate content modules)
- Comparison content split across 4 modules by category for maintainability

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Function name collision with comparison_related_links**
- **Found during:** Task 2 (comparison page generation)
- **Issue:** Pre-existing function comparison_related_links(current_slug) at line ~9249 shadowed the new two-argument version, causing TypeError
- **Fix:** Renamed new function to tool_comparison_related_links(current_slug, category)
- **Files modified:** scripts/build.py
- **Verification:** Build completes without errors
- **Committed in:** 1ea8bd3 (Task 2 commit)

**2. [Rule 1 - Bug] Banned words and false reframe patterns in comparison content**
- **Found during:** Task 2 (post-build validation)
- **Issue:** QUAL2-09 warnings for "seamless", "actually", "exceed", "empower", "really", "landscape", and false reframe patterns ("isn't X. It's Y")
- **Fix:** Replaced all instances with compliant alternatives
- **Files modified:** content/comparisons_enrichment.py, content/comparisons_outbound.py, content/comparisons_automation.py
- **Verification:** Rebuild shows zero QUAL2-09 warnings on comparison pages
- **Committed in:** 1ea8bd3 (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (1 blocking, 1 bug)
**Impact on plan:** Both fixes necessary for correctness. No scope creep.

## Issues Encountered
None beyond the auto-fixed deviations above.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Category and comparison infrastructure ready for Plan 02 (10 more comparisons)
- Content module pattern established and working for all 4 category files
- TOOL_COMPARISONS and BUILT_COMPARISON_SLUGS set ready for expansion

---
*Phase: 09-tool-categories-and-comparisons*
*Completed: 2026-03-14*
