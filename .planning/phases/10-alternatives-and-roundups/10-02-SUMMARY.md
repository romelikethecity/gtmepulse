---
phase: 10-alternatives-and-roundups
plan: 02
subsystem: content
tags: [roundups, best-for, tool-reviews, seo, faq-schema, build-system]

# Dependency graph
requires:
  - phase: 10-alternatives-and-roundups (10-01)
    provides: TOOL_ALTERNATIVES data list, _load_alternative_content, generate_tool_alternative, build_tool_alternatives patterns
provides:
  - 10 roundup pages at /tools/best-[topic]/
  - TOOL_ROUNDUPS data list and generator infrastructure
  - 3 content modules (roundups_startup, roundups_free, roundups_category)
affects: [tools-index, sitemap, phase-11-glossary]

# Tech tracking
tech-stack:
  added: []
  patterns: [ROUNDUPS dict in content modules, generate_tool_roundup() page generator, roundup_related_links() cross-linking]

key-files:
  created:
    - content/roundups_startup.py
    - content/roundups_free.py
    - content/roundups_category.py
  modified:
    - scripts/build.py

key-decisions:
  - "Roundup pages reuse salary-header/salary-content CSS pattern, consistent with reviews, comparisons, and alternatives"
  - "Each ranked tool links to its review page when one exists, with category badge and pricing info"
  - "Added G2 Buyer Intent as third intent data platform to meet 3-tool minimum requirement"

patterns-established:
  - "ROUNDUPS dict in content modules keyed by roundup slug, with intro, ranked tools list, verdict with quick-pick table, and FAQ tuples"
  - "roundup_related_links() cross-links other roundup pages, alternatives pages, and category indexes"

requirements-completed: [TBST-01, TBST-02, TBST-03, TBST-04, TBST-05, TBST-06, TBST-07, TBST-08, TBST-09, TBST-10]

# Metrics
duration: 10min
completed: 2026-03-14
---

# Phase 10 Plan 02: Tool Roundups Summary

**10 best-for roundup pages with ranked tool lists, quick-pick verdict tables, FAQ schemas, and cross-links to reviews, comparisons, and alternatives across startup, enterprise, free, AI, and 6 category-specific topics**

## Performance

- **Duration:** 10 min
- **Started:** 2026-03-14T16:55:46Z
- **Completed:** 2026-03-14T17:05:27Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Created 3 content modules with opinionated, ranked tool recommendations across 10 best-for topics
- Built generator infrastructure in build.py (TOOL_ROUNDUPS, _load_roundup_content, roundup_related_links, generate_tool_roundup, build_tool_roundups)
- Each page has FAQPage + BreadcrumbList JSON-LD, affiliate disclosures, and related links grid
- Build produces 211 total pages (201 existing + 10 new roundup pages)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create roundup content modules** - `bcb6960` (feat)
2. **Task 2: Add roundup generator infrastructure to build.py** - `83f0442` (feat)

## Files Created/Modified
- `content/roundups_startup.py` - Startup and enterprise tool roundups (6 and 5 tools respectively)
- `content/roundups_free.py` - Free GTM tools and AI-powered GTM tools (5 and 4 tools)
- `content/roundups_category.py` - Enrichment (8), outbound (6), CRM (5), automation (3), LinkedIn (3), intent data (3) roundups
- `scripts/build.py` - TOOL_ROUNDUPS data, generator functions, main() call

## Decisions Made
- Roundup pages reuse salary-header/salary-content CSS from reviews, comparisons, and alternatives (no new CSS needed)
- Each ranked tool entry includes a linked heading (to review page), category badge, best-for summary, why-picked paragraph, and pricing
- Quick-pick verdict tables summarize recommendations in scannable format
- Added G2 Buyer Intent as third intent data platform to satisfy the 3-tool minimum on every roundup page

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed banned words and false reframe pattern in content**
- **Found during:** Task 2 (build verification)
- **Issue:** QUAL2-09 warnings for "game-changer" (1), "actually" (2), and false reframe pattern "isn't X. It's Y" (1) in roundup content
- **Fix:** Replaced "game-changer" with "transform your pipeline targeting", removed "actually" (2 instances), rewrote false reframe as direct statement
- **Files modified:** content/roundups_category.py, content/roundups_free.py
- **Verification:** Rebuild shows zero QUAL2-09 warnings on roundup pages
- **Committed in:** 83f0442 (Task 2 commit)

**2. [Rule 2 - Missing Critical] Added G2 Buyer Intent to intent data roundup**
- **Found during:** Task 1 (content verification)
- **Issue:** Plan specified only 6sense and Bombora for intent data, but verification requires 3+ tools per roundup
- **Fix:** Added G2 Buyer Intent as third entry with review-site intent positioning
- **Files modified:** content/roundups_category.py
- **Committed in:** bcb6960 (Task 1 commit, after fix)

---

**Total deviations:** 2 auto-fixed (1 banned words/patterns, 1 content completeness)
**Impact on plan:** Minor content fixes for CLAUDE.md compliance and verification requirements. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 10 (Alternatives & Roundups) fully complete
- All 20 new pages (10 alternatives + 10 roundups) cross-linked with reviews, comparisons, and categories
- Build runs clean at 211 pages
- Ready for Phase 11 (Glossary) or Phase 12 (Final Quality)

---
*Phase: 10-alternatives-and-roundups*
*Completed: 2026-03-14*
