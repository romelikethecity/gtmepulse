---
phase: 06-tools-and-benchmarks
plan: 02
subsystem: ui
tags: [tools, frustrations, exciting, unify, annual-spend, zoominfo, apollo, wishlist]

requires:
  - phase: 06-tools-and-benchmarks
    plan: 01
    provides: TOOL_PAGES array, BUILT_TOOL_SLUGS set, tool_related_links(), tools index
provides:
  - 6 new tool pages (frustrations, most-exciting, unify-analysis, annual-spend, zoominfo-vs-apollo, tool-wishlist)
  - BUILT_TOOL_SLUGS expanded to 11 pages
  - Tools index updated with 11 live page cards
affects: [07-quality-sweep, tools section completeness]

tech-stack:
  added: []
  patterns: [same build_tool_*() pattern with BreadcrumbList + FAQPage schema]

key-files:
  created:
    - output/tools/frustrations/index.html
    - output/tools/most-exciting/index.html
    - output/tools/unify-analysis/index.html
    - output/tools/annual-spend/index.html
    - output/tools/zoominfo-vs-apollo/index.html
    - output/tools/tool-wishlist/index.html
  modified:
    - scripts/build.py

key-decisions:
  - "TOOL_PAGES expanded from 16 to 22 entries to accommodate 6 new analysis pages"
  - "Unify analysis written as honest criticism page per CLAUDE.md: 8.8% vs Clay 84%"
  - "Tool index card_data includes all 11 built pages with stat badges"

patterns-established:
  - "Opinion and spending pages follow same builder pattern as adoption pages"
  - "Cross-linking between frustrations, wishlist, and most-exciting pages creates content cluster"

requirements-completed: [TOOL-06, TOOL-07, TOOL-08, TOOL-09, TOOL-10, TOOL-11]

duration: 8min
completed: 2026-03-13
---

# Phase 6 Plan 2: Tool Opinion and Spending Pages Summary

**6 tool pages covering frustrations, most exciting tools (Claude 39 mentions), Unify 8.8% honest critique, annual spend ($5K-$25K agencies), ZoomInfo vs Apollo head-to-head, and tool wishlist (all-in-one outbound #1 request)**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-13T22:29:37Z
- **Completed:** 2026-03-13T22:37:40Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Tool frustrations page with integration issues, UX, documentation, and pricing complaint categories (1,927 words)
- Most exciting tools page with Claude (39), Cursor (11), n8n (8) as top 3 plus emerging tool analysis (1,666 words)
- Unify honest critique page showing 8.8% adoption vs Clay's 84%, with marketing-vs-reality analysis (1,539 words)
- Annual tool spend page covering $5K-$25K agency sweet spot, US vs non-US, cost optimization strategies (1,685 words)
- ZoomInfo vs Apollo comparison with data quality, pricing, and Clay waterfall enrichment patterns (1,719 words)
- Tool wishlist page revealing all-in-one outbound as #1 request, AI SDR demand, attribution gaps (1,686 words)
- Build total increased from 90 to 96 pages, zero validation warnings

## Task Commits

Each task was committed atomically:

1. **Task 1: Frustrations, most exciting tools, Unify analysis** - `07e7cb3` (feat)
2. **Task 2: Annual spend, ZoomInfo vs Apollo, tool wishlist** - `127772b` (feat)

**Plan metadata:** [pending]

## Files Created/Modified
- `scripts/build.py` - Added build_tool_frustrations(), build_tool_most_exciting(), build_tool_unify(), build_tool_annual_spend(), build_tool_zoominfo_vs_apollo(), build_tool_wishlist(), expanded TOOL_PAGES to 22 entries, BUILT_TOOL_SLUGS to 11 pages, updated tools index card_data
- `output/tools/frustrations/index.html` - Tool frustrations analysis (1,927 words)
- `output/tools/most-exciting/index.html` - Most exciting tools survey results (1,666 words)
- `output/tools/unify-analysis/index.html` - Unify 8.8% adoption honest critique (1,539 words)
- `output/tools/annual-spend/index.html` - Annual tool spend data (1,685 words)
- `output/tools/zoominfo-vs-apollo/index.html` - ZoomInfo vs Apollo comparison (1,719 words)
- `output/tools/tool-wishlist/index.html` - Tool wishlist analysis (1,686 words)

## Decisions Made
- Expanded TOOL_PAGES from 16 to 22 entries to fit 6 new analysis-style pages alongside adoption deep-dives
- Unify page written as honest criticism: 8.8% vs Clay 84%, marketing disconnect analysis, no softening of the adoption gap
- Cross-linked frustrations, wishlist, and most-exciting pages as a content cluster (each references the other two)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed banned words across 3 pages**
- **Found during:** Task 1 (initial build validation)
- **Issue:** "actually" in frustrations and most-exciting pages, "resonates" in most-exciting, "landscape" and "positioning" in Unify page, title too long for frustrations page (62 chars)
- **Fix:** Replaced banned words with compliant alternatives, shortened frustrations title by removing "(2026)"
- **Files modified:** scripts/build.py
- **Verification:** Build validation passes with zero warnings
- **Committed in:** 07e7cb3 (part of Task 1 commit)

**2. [Rule 1 - Bug] Fixed banned word "unlock" in wishlist page**
- **Found during:** Task 2 (build validation)
- **Issue:** "unlock" used in pricing frustrations paragraph
- **Fix:** Replaced "features that those seats unlock" with "features that come with those seats"
- **Files modified:** scripts/build.py
- **Verification:** Build validation passes with zero warnings
- **Committed in:** 127772b (part of Task 2 commit)

---

**Total deviations:** 2 auto-fixed (2 bugs - banned word violations)
**Impact on plan:** Minor word replacements. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Tools section now has 11 live pages plus 11 coming soon
- Cross-linking cluster (frustrations, wishlist, most-exciting) creates strong internal link structure
- Tool infrastructure ready for remaining tool pages in future plans

---
*Phase: 06-tools-and-benchmarks*
*Completed: 2026-03-13*
