---
phase: 07-comparisons-blog-articles-and-quality-sweep
plan: 01
subsystem: content
tags: [comparisons, seo, faq-schema, cross-links, nav]

requires:
  - phase: 06-tools-and-benchmarks
    provides: BENCH_PAGES array, bench_related_links pattern, benchmark index
provides:
  - COMP_PAGES array (6 entries) for comparison page generation and cross-linking
  - comparison_related_links() cross-linking function
  - 7 new pages (6 comparisons + index) at /comparisons/
  - Nav and footer entries for Comparisons section
affects: [07-02, 07-03, 07-04]

tech-stack:
  added: []
  patterns: [COMP_PAGES array mirrors BENCH_PAGES pattern, comparison_related_links follows bench_related_links pattern]

key-files:
  created:
    - output/comparisons/index.html
    - output/comparisons/engineer-vs-operator/index.html
    - output/comparisons/in-house-vs-agency/index.html
    - output/comparisons/engineer-vs-ai-sdr/index.html
    - output/comparisons/us-vs-europe-vs-apac/index.html
    - output/comparisons/seed-vs-series-b/index.html
    - output/comparisons/technical-vs-low-code/index.html
  modified:
    - scripts/build.py
    - scripts/nav_config.py

key-decisions:
  - "COMP_PAGES array follows BENCH_PAGES pattern as single source of truth for index and cross-links"
  - "Comparisons nav entry as simple link (like Benchmarks) since 6 pages don't need dropdown"
  - "comparison_related_links() cross-links all comparison pages plus salary/tools/careers/benchmarks indexes (limit 12)"
  - "CSS_VERSION bumped to 13 for nav/footer structural changes"

patterns-established:
  - "COMP_PAGES array pattern: slug, title, description, emoji, stat fields"
  - "Comparison page structure: salary-header + salary-stats + salary-content + FAQ + related links + source citation + newsletter CTA"

requirements-completed: [COMP-01, COMP-02, COMP-03, COMP-04, COMP-05, COMP-06]

duration: 8min
completed: 2026-03-14
---

# Phase 7 Plan 1: Comparison Pages Summary

**6 data-backed comparison pages with FAQPage schema, BreadcrumbList, source citations, and cross-links to salary/tools/careers/benchmarks sections. 118 total pages (was 111).**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-14T04:25:25Z
- **Completed:** 2026-03-14T04:33:30Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- 6 comparison pages with 1,500-2,200 words each, covering engineer vs operator, in-house vs agency, engineer vs AI SDR, US vs global salaries, seed vs series B compensation, and technical vs low-code
- Comparisons index page with 6-card grid and 800+ word intro
- COMP_PAGES array (6 entries) and comparison_related_links() for cross-linking
- Nav and footer updated with Comparisons entry, CSS_VERSION bumped to 13

## Task Commits

Each task was committed atomically:

1. **Task 1: Comparisons index + COMP_PAGES array + first 3 comparison pages** - `c24eae5` (feat)
2. **Task 2: Remaining 3 comparison pages + nav/footer update** - `2c37b5f` (feat)

## Files Created/Modified
- `scripts/build.py` - COMP_PAGES array, comparison_related_links(), build_comp_index(), 6 build_comp_* functions
- `scripts/nav_config.py` - Comparisons nav entry, footer link, CSS_VERSION 13

## Decisions Made
- COMP_PAGES array follows BENCH_PAGES pattern as single source of truth
- Comparisons nav is a simple link (not dropdown) since only 6 pages
- comparison_related_links() includes all comparison pages + 4 cross-section indexes (limit 12)
- CSS_VERSION bumped to 13

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed banned word "leverage" in 3 comparison pages**
- **Found during:** Task 1 (build verification)
- **Issue:** "leverage" appeared in 3 places across comparison pages, flagged by content validator
- **Fix:** Replaced with "most impactful," "stronger negotiating position," and "pays off fast"
- **Files modified:** scripts/build.py
- **Verification:** Rebuild produces zero warnings
- **Committed in:** c24eae5 (Task 1 commit)

**2. [Rule 1 - Bug] Fixed meta description length on US vs Europe vs APAC page**
- **Found during:** Task 2 (build verification)
- **Issue:** Description was 149 chars (validator requires 150-158)
- **Fix:** Adjusted wording to "non-US peers" and "fastest growth markets"
- **Verification:** Rebuild produces zero warnings
- **Committed in:** 2c37b5f (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (2 bugs)
**Impact on plan:** Minor content fixes. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Comparison pages complete, ready for blog articles (07-02) and quality sweep (07-03, 07-04)
- Cross-links from comparison pages to salary, tools, careers, and benchmarks sections are active
- 118 total pages building cleanly with zero warnings

---
*Phase: 07-comparisons-blog-articles-and-quality-sweep*
*Completed: 2026-03-14*
