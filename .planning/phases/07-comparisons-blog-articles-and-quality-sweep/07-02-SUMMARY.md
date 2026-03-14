---
phase: 07-comparisons-blog-articles-and-quality-sweep
plan: 02
subsystem: content
tags: [blog, articles, opinion, data-backed, gtm-engineering, seo]

requires:
  - phase: 07-01
    provides: COMP_PAGES array and comparison_related_links() pattern
provides:
  - BLOG_PAGES array with 14 entries for all planned blog articles
  - BUILT_BLOG_SLUGS set tracking 7 published articles
  - blog_related_links() cross-linking function
  - Blog index at /blog/ with card grid
  - 7 data-backed opinion articles (1,500+ words each)
affects: [07-03, 07-04]

tech-stack:
  added: []
  patterns: [BLOG_PAGES/BUILT_BLOG_SLUGS incremental publishing pattern]

key-files:
  created: []
  modified: [scripts/build.py]

key-decisions:
  - "BLOG_PAGES array follows COMP_PAGES pattern with 14 entries defined upfront, BUILT_BLOG_SLUGS controls which are published"
  - "Blog articles use salary-header/salary-content CSS classes for visual consistency with rest of site"
  - "Each article has byline (By Rome Thorndike, March 2026) for author attribution"

patterns-established:
  - "Blog article pattern: salary-header with eyebrow, H1, subtitle + salary-stats cards + salary-content body + source_citation + newsletter_cta + blog_related_links"
  - "BUILT_BLOG_SLUGS gating: same incremental publishing pattern as BUILT_TOOL_SLUGS"

requirements-completed: [BLOG-01, BLOG-02, BLOG-03, BLOG-04, BLOG-05, BLOG-06, BLOG-07]

duration: 15min
completed: 2026-03-14
---

# Phase 7 Plan 2: Blog Articles Summary

**7 data-backed opinion articles (equity gap, coding premium, work hours, Gen Z, Clay love/hate, LATAM/APAC agencies, title dilution) with blog index, cross-links, and BreadcrumbList schema**

## Performance

- **Duration:** 15 min
- **Started:** 2026-03-14T04:36:46Z
- **Completed:** 2026-03-14T04:52:22Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Blog index page at /blog/ showing all 7 published articles in card grid
- BLOG_PAGES array with 14 entries (7 built now, 7 reserved for future)
- blog_related_links() cross-linking blog articles with salary, career, comparisons, tools, and benchmarks sections
- 7 opinion articles each 1,500+ words with specific theses backed by State of GTME Report data
- Build produces 126 pages with zero content validation warnings

## Task Commits

Each task was committed atomically:

1. **Task 1: Blog index + BLOG_PAGES + blog_related_links + first 4 articles** - `52cd0ef` (feat)
2. **Task 2: Blog articles 5-7 (Clay, LATAM/APAC, title dilution)** - `712567e` (feat)

## Files Created/Modified
- `scripts/build.py` - Added BLOG_PAGES array (14 entries), BUILT_BLOG_SLUGS (7), blog_related_links(), build_blog_index(), and 7 article build functions

## Decisions Made
- BLOG_PAGES follows COMP_PAGES pattern with all 14 entries defined upfront for future expansion
- Blog articles reuse salary-header/salary-content/salary-stats CSS classes (no new CSS needed)
- Each article includes author byline with date for editorial credibility

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed banned words in article content**
- **Found during:** Task 1 and Task 2
- **Issue:** "leverage" appeared in coding-premium article and BLOG_PAGES description; "actually" and "positioning" appeared in title-dilution article
- **Fix:** Replaced with non-banned alternatives (bargaining power, compounding returns, Internal credibility)
- **Files modified:** scripts/build.py
- **Verification:** Content validation passes with zero warnings
- **Committed in:** 52cd0ef and 712567e (part of task commits)

---

**Total deviations:** 1 auto-fixed (banned word violations)
**Impact on plan:** Minor text corrections required by content validator. No scope creep.

## Issues Encountered
- Initial article word counts were under 1,500 threshold. Expanded each article with additional substantive sections (geographic dimension, agency exception, compensation equation, burnout risk, credit economy, etc.) to meet the 1,500+ word requirement.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Blog section complete with 7 articles, ready for quality sweep in 07-03
- BLOG_PAGES has 7 more entries reserved for future articles (07-04 or beyond)
- Blog index auto-updates when new slugs are added to BUILT_BLOG_SLUGS

---
*Phase: 07-comparisons-blog-articles-and-quality-sweep*
*Completed: 2026-03-14*
