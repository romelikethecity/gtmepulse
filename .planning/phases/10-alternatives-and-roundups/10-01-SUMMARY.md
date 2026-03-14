---
phase: 10-alternatives-and-roundups
plan: 01
subsystem: content
tags: [alternatives, tool-reviews, seo, faq-schema, build-system]

# Dependency graph
requires:
  - phase: 09-tool-categories-and-comparisons
    provides: TOOL_COMPARISONS list, comparison content modules, comparison generator pattern
provides:
  - 10 alternatives pages at /tools/[tool]-alternatives/
  - TOOL_ALTERNATIVES data list and generator infrastructure
  - 6 content modules (alternatives_enrichment, alternatives_outbound, alternatives_crm, alternatives_automation, alternatives_intent, alternatives_linkedin)
affects: [10-02 roundups, tools-index, sitemap]

# Tech tracking
tech-stack:
  added: []
  patterns: [alternatives content module with ALTERNATIVES dict, generate_tool_alternative() page generator]

key-files:
  created:
    - content/alternatives_enrichment.py
    - content/alternatives_outbound.py
    - content/alternatives_crm.py
    - content/alternatives_automation.py
    - content/alternatives_intent.py
    - content/alternatives_linkedin.py
  modified:
    - scripts/build.py

key-decisions:
  - "Alternatives pages reuse salary-header/salary-content CSS pattern from reviews and comparisons"
  - "Each alternative entry has numbered headings with review links, pros/cons grid, pricing, and verdict"
  - "Related links include tool review, relevant comparisons, and other alternatives pages"

patterns-established:
  - "ALTERNATIVES dict in content modules keyed by tool slug, with intro, alternatives list, and faq tuples"
  - "alternative_related_links() cross-links reviews, comparisons, and other alternatives pages"

requirements-completed: [TALT-01, TALT-02, TALT-03, TALT-04, TALT-05, TALT-06, TALT-07, TALT-08, TALT-09, TALT-10]

# Metrics
duration: 12min
completed: 2026-03-14
---

# Phase 10 Plan 01: Tool Alternatives Summary

**10 alternatives pages (Clay, Apollo, ZoomInfo, Instantly, Outreach, HubSpot, Salesforce, Zapier, 6sense, Sales Navigator) with 5-8 alternatives each, FAQ schemas, and cross-links to reviews and comparisons**

## Performance

- **Duration:** 12 min
- **Started:** 2026-03-14T16:41:11Z
- **Completed:** 2026-03-14T16:53:14Z
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments
- Created 6 content modules with opinionated, vendor-neutral alternatives for 10 tools
- Built generator infrastructure in build.py (TOOL_ALTERNATIVES, _load_alternative_content, generate_tool_alternative, build_tool_alternatives)
- Each page has FAQPage + BreadcrumbList JSON-LD, affiliate disclosures, and related links grid
- Build produces 201 total pages (191 existing + 10 new alternatives)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create alternatives content modules** - `1e4d358` (feat)
2. **Task 2: Add alternatives generator infrastructure to build.py** - `674e0c1` (feat)

## Files Created/Modified
- `content/alternatives_enrichment.py` - Clay, Apollo, ZoomInfo alternatives (5-7 alternatives each)
- `content/alternatives_outbound.py` - Instantly, Outreach alternatives (5-6 alternatives each)
- `content/alternatives_crm.py` - HubSpot, Salesforce alternatives (5-6 alternatives each)
- `content/alternatives_automation.py` - Zapier alternatives (5 alternatives)
- `content/alternatives_intent.py` - 6sense alternatives (6 alternatives)
- `content/alternatives_linkedin.py` - LinkedIn Sales Navigator alternatives (6 alternatives)
- `scripts/build.py` - TOOL_ALTERNATIVES data, generator functions, main() call

## Decisions Made
- Alternatives pages reuse salary-header/salary-content CSS from reviews and comparisons (no new CSS)
- Each alternative entry includes numbered h2 headings with optional review links
- Pros/cons displayed in two-column grid with green/red accent colors
- Related links prioritize the tool's own review, then comparisons involving that tool, then other alternatives pages

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed banned words and false reframe pattern in content**
- **Found during:** Task 2 (build verification)
- **Issue:** QUAL2-09 warnings for "exceed" (2 instances), "genuinely" (1 instance), and false reframe pattern "isn't X. It's Y" (1 instance)
- **Fix:** Replaced "exceed" with "surpass"/"top"/"outperform", "genuinely" with "surprisingly", rewrote false reframe sentence
- **Files modified:** content/alternatives_enrichment.py, content/alternatives_crm.py, content/alternatives_outbound.py, content/alternatives_linkedin.py
- **Verification:** Rebuild shows zero QUAL2-09 warnings on alternatives pages
- **Committed in:** 674e0c1 (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (banned words/patterns)
**Impact on plan:** Minor content fixes to comply with CLAUDE.md writing rules. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Alternatives pages complete, ready for Phase 10 Plan 02 (roundups)
- All 10 alternatives pages are cross-linked with reviews and comparisons
- Build runs clean at 201 pages

---
*Phase: 10-alternatives-and-roundups*
*Completed: 2026-03-14*
