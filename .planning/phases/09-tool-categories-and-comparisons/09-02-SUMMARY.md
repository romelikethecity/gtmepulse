---
phase: 09-tool-categories-and-comparisons
plan: 02
subsystem: content
tags: [comparisons, intent-data, analytics, linkedin, enrichment, outbound, crm, seo, faq-schema]

requires:
  - phase: 09-01
    provides: "TOOL_COMPARISONS infrastructure, generate_tool_comparison(), content module pattern"
provides:
  - "10 additional tool comparison pages (20 total)"
  - "Content modules: comparisons_intent.py, comparisons_analytics.py, comparisons_linkedin.py"
  - "Extended content in comparisons_enrichment.py, comparisons_outbound.py, comparisons_crm.py"
affects: [10-alternatives-and-roundups]

tech-stack:
  added: []
  patterns: ["Content modules split by tool category with COMPARISONS dict pattern"]

key-files:
  created:
    - content/comparisons_intent.py
    - content/comparisons_analytics.py
    - content/comparisons_linkedin.py
  modified:
    - scripts/build.py
    - content/comparisons_enrichment.py
    - content/comparisons_outbound.py
    - content/comparisons_crm.py

key-decisions:
  - "Intent data category gets dedicated content module (comparisons_intent.py)"
  - "Analytics category covers Reverse ETL tools (Hightouch, Census) alongside product analytics"
  - "LinkedIn category covers both automation tools and prospecting platform comparisons"

patterns-established:
  - "Content modules per category: max ~3-4 comparisons per file for maintainability"

requirements-completed: [TCMP-11, TCMP-12, TCMP-13, TCMP-14, TCMP-15, TCMP-16, TCMP-17, TCMP-18, TCMP-19, TCMP-20]

duration: 11min
completed: 2026-03-14
---

# Phase 9 Plan 02: Remaining Tool Comparisons Summary

**10 new tool-vs-tool comparison pages covering intent data, analytics, LinkedIn, enrichment, outbound, and CRM categories, completing all 20 planned comparisons for Phase 9**

## Performance

- **Duration:** 11 min
- **Started:** 2026-03-14T16:04:24Z
- **Completed:** 2026-03-14T16:16:07Z
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments
- Created 3 new content modules (intent, analytics, linkedin) and extended 3 existing ones (enrichment, outbound, crm)
- All 10 new comparison pages built with feature tables, pricing breakdowns, verdicts, and 4-5 FAQ pairs each
- Every comparison page has FAQPage + BreadcrumbList JSON-LD schema
- Build runs clean at 191 pages with no banned word violations in new content

## Task Commits

Each task was committed atomically:

1. **Task 1: Create content modules for remaining 10 comparisons** - `f48dd1d` (feat)
2. **Task 2: Add 10 comparison entries to build.py and generate all 20 pages** - `cca7d8c` (feat)

## Files Created/Modified
- `content/comparisons_intent.py` - 6sense vs Bombora comparison content
- `content/comparisons_analytics.py` - Mixpanel vs Amplitude, Segment vs PostHog, Hightouch vs Census
- `content/comparisons_linkedin.py` - HeyReach vs Expandi, LinkedIn Sales Nav vs Apollo
- `content/comparisons_enrichment.py` - Added cognism-vs-zoominfo and leadiq-vs-lusha entries
- `content/comparisons_outbound.py` - Added smartlead-vs-lemlist entry
- `content/comparisons_crm.py` - Added close-vs-pipedrive entry
- `scripts/build.py` - 10 new TOOL_COMPARISONS entries with SEO titles and meta descriptions

## Decisions Made
- Intent data gets its own content module since it's a distinct category from enrichment
- Analytics category includes Reverse ETL (Hightouch/Census) since they're in the same infrastructure layer
- Tools without review pages (Mixpanel, Amplitude, Hightouch, Census, Expandi) link to category index pages instead

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed banned words in comparison content**
- **Found during:** Task 2 (build verification)
- **Issue:** QUAL2-09 flagged "cutting-edge", "quite", "exceed", "actually" in new content modules
- **Fix:** Replaced with non-banned alternatives: "advanced", removed "quite", "pass", "deliver"
- **Files modified:** content/comparisons_analytics.py, content/comparisons_intent.py, content/comparisons_enrichment.py
- **Verification:** Rebuild shows zero QUAL2-09 warnings for new comparison pages
- **Committed in:** cca7d8c (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Minor content quality fix. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 9 complete: 8 category pages + 20 comparison pages = 28 new tool pages
- Ready for Phase 10 (alternatives and roundups) which will link to these comparison pages
- All comparison content modules and build infrastructure reusable for future comparisons

---
*Phase: 09-tool-categories-and-comparisons*
*Completed: 2026-03-14*

## Self-Check: PASSED
- 3 created content modules: all found
- 2 task commits: all found
- 20 comparison output pages: all found
