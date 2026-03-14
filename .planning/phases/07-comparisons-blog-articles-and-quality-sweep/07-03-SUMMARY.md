---
phase: 07-comparisons-blog-articles-and-quality-sweep
plan: 03
subsystem: content
tags: [blog, articles, opinion, data-backed, gtm-engineering, seo, navigation]

requires:
  - phase: 07-02
    provides: BLOG_PAGES array (14 entries), BUILT_BLOG_SLUGS (7), blog_related_links(), blog index
provides:
  - BUILT_BLOG_SLUGS expanded to 14 entries (all blog articles published)
  - 7 new blog articles (pre-seed equity, self-taught, lead gen myth, all-in-one tool, bonus data, december explosion, mid-size pay)
  - Blog nav entry and footer link
  - CSS_VERSION bumped to 14
affects: [07-04]

tech-stack:
  added: []
  patterns: [Blog article pattern reused for all 7 new articles]

key-files:
  created: []
  modified: [scripts/build.py, scripts/nav_config.py]

key-decisions:
  - "Blog nav entry placed as simple link after Comparisons and before Careers (not dropdown since articles share one index)"
  - "CSS_VERSION bumped to 14 for nav/footer structural changes"
  - "All 14 BLOG_PAGES now in BUILT_BLOG_SLUGS, completing the blog section"

patterns-established:
  - "Blog articles 8-14 follow same pattern as 1-7: salary-header + salary-stats + salary-content + source_citation + newsletter_cta + blog_related_links"

requirements-completed: [BLOG-08, BLOG-09, BLOG-10, BLOG-11, BLOG-12, BLOG-13, BLOG-14]

duration: 9min
completed: 2026-03-14
---

# Phase 7 Plan 3: Blog Articles (8-14) + Blog Navigation Summary

**7 remaining blog articles (pre-seed equity, self-taught path, lead gen scope, all-in-one tool gap, bonus data, December 2025 explosion, mid-size company pay) with Blog added to site navigation and footer**

## Performance

- **Duration:** 9 min
- **Started:** 2026-03-14T04:54:53Z
- **Completed:** 2026-03-14T05:04:11Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- 7 new blog articles (BLOG-08 through BLOG-14), each 1,500+ words with specific data-backed theses
- BUILT_BLOG_SLUGS expanded to 14 entries, completing the full blog section
- Blog index now shows all 14 articles in card grid
- Blog entry added to nav (after Comparisons, before Careers) and footer Resources
- Build produces 133 pages with zero content validation warnings

## Task Commits

Each task was committed atomically:

1. **Task 1: Blog articles 8-11 (pre-seed equity, self-taught, lead gen, all-in-one)** - `ae20308` (feat)
2. **Task 2: Blog articles 12-14 + nav/footer Blog entry** - `477a204` (feat)

## Files Created/Modified
- `scripts/build.py` - Added 7 blog article build functions, expanded BUILT_BLOG_SLUGS to 14, added build calls to main()
- `scripts/nav_config.py` - Added Blog to NAV_ITEMS and FOOTER_COLUMNS, bumped CSS_VERSION to 14

## Decisions Made
- Blog nav entry as simple link (not dropdown) matching Comparisons and Benchmarks pattern
- Blog placed after Comparisons and before Careers in nav order
- CSS_VERSION bumped to 14 for nav/footer structural changes

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed banned words in article content**
- **Found during:** Task 1 and Task 2
- **Issue:** "robust" in all-in-one-tool article, "resonates" in lead-gen-myth article, "leverage" in mid-size-pay article
- **Fix:** Replaced with non-banned alternatives (mature full-featured, operations leaders care about, more meaningful)
- **Files modified:** scripts/build.py
- **Verification:** Content validation passes with zero warnings
- **Committed in:** ae20308 and 477a204 (part of task commits)

**2. [Rule 1 - Bug] Fixed description lengths below 150 characters**
- **Found during:** Task 1 and Task 2
- **Issue:** all-in-one-tool description (148 chars) and bonus-data description (149 chars) fell below 150 minimum
- **Fix:** Added words to bring descriptions to 150+ characters
- **Files modified:** scripts/build.py
- **Verification:** Content validation passes with zero warnings
- **Committed in:** ae20308 and 477a204 (part of task commits)

---

**Total deviations:** 2 auto-fixed (banned word violations, description length)
**Impact on plan:** Minor text corrections required by content validator. No scope creep.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All 14 blog articles complete with cross-links to salary, career, comparison, tool, and benchmark pages
- Blog section accessible from site navigation and footer
- Ready for quality sweep in 07-04

## Self-Check: PASSED

All 7 blog article output files verified. Both task commits (ae20308, 477a204) verified in git log.

---
*Phase: 07-comparisons-blog-articles-and-quality-sweep*
*Completed: 2026-03-14*
