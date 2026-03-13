---
phase: 04-salary-data-overhaul
plan: 03
subsystem: content
tags: [salary, equity, agency-fees, geographic, posted-vs-actual, seed-vs-enterprise, navigation]

# Dependency graph
requires:
  - phase: 04-salary-data-overhaul
    provides: salary data dicts, source_citation_html(), salary page generator pattern, analysis page type
provides:
  - 6 new salary pages (equity, US vs global, posted vs actual, agency fees, agency fees by region, seed vs enterprise)
  - Updated navigation dropdown with Coding Premium, Equity Data, Agency Fees entries
  - Updated footer with Coding Premium and Equity Data links
  - Updated salary index with "More Salary Data" section linking all 12 new pages
  - Updated salary_related_links() with equity, agency-fees, us-vs-global cross-links
affects: [salary pages, homepage, sitemap, navigation]

# Tech tracking
tech-stack:
  added: []
  patterns: [custom stats block for non-salary metrics (equity percentages, agency fees), geographic comparison stats layout]

key-files:
  created:
    - output/salary/equity/index.html
    - output/salary/us-vs-global/index.html
    - output/salary/posted-vs-actual/index.html
    - output/salary/agency-fees/index.html
    - output/salary/agency-fees-by-region/index.html
    - output/salary/seed-vs-enterprise/index.html
  modified:
    - scripts/build.py
    - scripts/nav_config.py

key-decisions:
  - "Custom stats blocks for equity (percentages), agency fees ($K/mo ranges), and geographic data (side-by-side medians) reusing salary-stat-card CSS"
  - "Salary index gains 'More Salary Data' section with cards for all 12 analysis pages"
  - "Nav dropdown limited to 3 new entries (Coding Premium, Equity, Agency Fees) to avoid overcrowding"

patterns-established:
  - "Agency/non-employee compensation pages use same analysis page pattern as salary pages"
  - "Salary index card grid pattern for linking to analysis sub-pages"

requirements-completed: [SALN-07, SALN-08, SALN-09, SALN-10, SALN-11, SALN-12]

# Metrics
duration: 7min
completed: 2026-03-13
---

# Phase 4 Plan 3: Final Salary Pages Summary

**6 salary pages covering equity (68% have nothing), US vs global ($60K gap), posted vs actual ($15K inflation), agency fees ($5K-$8K/mo), regional agency rates, and seed vs enterprise trade-offs, plus nav and index updates**

## Performance

- **Duration:** 7 min
- **Started:** 2026-03-13T17:25:17Z
- **Completed:** 2026-03-13T17:32:30Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Built 6 final salary analysis pages completing the salary data overhaul
- Equity page documents that 68% of GTM Engineers hold no meaningful equity, with a U-curve across funding stages (Pre-Seed 29%, Series A 9%, Public 33%)
- US vs Global page shows the $60K gap ($135K US vs $75K non-US) with distribution across 6 regions and 32 countries
- Posted vs Actual page reveals $150K posted median vs $135K reported, with US posted salary band detail (P25-P90)
- Agency fees page: first real data on GTM Engineering agency economics ($5K-$8K/mo median, 47% with <5 clients)
- Agency fees by region: US premium, APAC $3K, MEA $4K, with arbitrage analysis for non-US agencies
- Seed vs Enterprise page: comprehensive compensation trade-off guide across all funding stages
- Updated nav dropdown with 3 new salary subcategories (Coding Premium, Equity Data, Agency Fees)
- Updated salary index with "More Salary Data" card grid linking all 12 new analysis pages
- Updated salary_related_links() to cross-reference new pages
- Build produces 55 total pages with zero content validation warnings

## Task Commits

Each task was committed atomically:

1. **Task 1: Build equity, US vs global, and posted vs actual pages** - `6f648e8` (feat)
2. **Task 2: Build agency fees, regional fees, seed vs enterprise pages, update nav** - `48b9c43` (feat)

## Files Created/Modified
- `scripts/build.py` - Added 6 new page generator functions, updated salary_related_links() with new page cross-links, added "More Salary Data" section to salary index, added calls in main()
- `scripts/nav_config.py` - Added 3 entries to nav dropdown (Coding Premium, Equity Data, Agency Fees), 2 entries to footer Salary Data column

## Decisions Made
- Used custom stats blocks (reusing salary-stat-card CSS classes) for equity percentages, agency fee ranges, and geographic comparison medians for visual consistency across all salary pages
- Limited nav dropdown additions to 3 entries (Coding Premium, Equity, Agency Fees) to keep the dropdown manageable. All 12 pages are accessible via the salary index "More Salary Data" section.
- Updated salary_related_links() to show equity, agency fees, and US vs global instead of bonus/experience links for non-analysis pages, maximizing cross-linking to new content.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed banned word "exceed" in equity and posted-vs-actual pages**
- **Found during:** Task 1 (build validation)
- **Issue:** "exceed" appeared 3 times across equity FAQ, us-vs-global content, and posted-vs-actual content
- **Fix:** Replaced with "cover", "outpaces", and "is above" respectively
- **Files modified:** scripts/build.py
- **Verification:** Build passes content validation with zero warnings
- **Committed in:** 6f648e8 (Task 1 commit)

**2. [Rule 1 - Bug] Fixed banned word "landscape" in agency-fees-by-region page**
- **Found during:** Task 2 (build validation)
- **Issue:** "landscape" appeared in regional pricing description
- **Fix:** Removed "landscape" from sentence
- **Files modified:** scripts/build.py
- **Verification:** Build passes content validation with zero warnings
- **Committed in:** 48b9c43 (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (2 bug fixes)
**Impact on plan:** Minor text corrections for writing standards compliance. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All 12 new salary analysis pages complete (6 from 04-02, 6 from 04-03)
- Total salary section covers 49 pages across seniority, location, stage, comparisons, analysis, and tools
- Navigation and footer updated to surface new content
- Salary index provides comprehensive hub with cards linking to every sub-page
- Phase 04 (Salary Data Overhaul) is complete
- Ready for Phase 05

---
*Phase: 04-salary-data-overhaul*
*Completed: 2026-03-13*
