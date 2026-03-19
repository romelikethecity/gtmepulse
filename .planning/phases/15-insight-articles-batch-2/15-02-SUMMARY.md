---
phase: 15-insight-articles-batch-2
plan: 02
subsystem: content
tags: [insight-articles, intent-data, crm-hygiene, pulse-report, live-data, build-py]

# Dependency graph
requires:
  - phase: 15-insight-articles-batch-2
    plan: 01
    provides: "INSIGHT_PAGES with all 20 entries, BUILT_INSIGHT_SLUGS with 14 slugs, commented dispatch calls"
provides:
  - "3 new insight articles (ART-15 through ART-17)"
  - "17 total insight articles on insights index"
  - "ART-17 loads jobs.json at build time and renders live stats"
affects: [15-insight-articles-batch-2]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Build-time data injection: load JSON, compute stats, render into HTML template"]

key-files:
  created: []
  modified: ["scripts/build.py"]

key-decisions:
  - "ART-17 loads jobs.json via os.path.exists with empty-list fallback for missing data"
  - "Computed stats include total roles, remote %, median salary, salary range, top company, seniority distribution"

patterns-established:
  - "Data-driven article pattern: load JSON at build time, compute aggregates, render stat cards and tables with live values"

requirements-completed: [ART-15, ART-16, ART-17]

# Metrics
duration: 7min
completed: 2026-03-18
---

# Phase 15 Plan 02: Insight Articles Batch 2 (Intent, CRM, Pulse) Summary

**Intent data buying guide, CRM hygiene playbook, and data-driven pulse report template rendering live job market stats from jobs.json at build time**

## Performance

- **Duration:** 7 min
- **Started:** 2026-03-19T04:52:29Z
- **Completed:** 2026-03-19T04:59:22Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Wrote ART-15 (intent data guide): vendor comparison across 6sense, Bombora, G2, TrustRadius with pricing tiers, integration patterns, and ROI calculation
- Wrote ART-16 (CRM hygiene): automated dedup with fuzzy matching, lifecycle stage automation, lead routing via code, enrichment triggers, dead lead detection
- Wrote ART-17 (pulse report template): loads data/jobs.json at build time, computes 13 tracked roles, 62% remote, $170K median salary, seniority distribution table
- Insights index now shows 17 articles (10 Phase 14 + 4 Plan 01 + 3 Plan 02)
- Zero new build warnings

## Task Commits

Each task was committed atomically:

1. **Task 1: ART-15 intent data guide and ART-16 CRM hygiene playbook** - `4f7ffe3` (feat)
2. **Task 2: ART-17 pulse report template with live data** - `3a824f2` (feat)

## Files Created/Modified
- `scripts/build.py` - Added 3 build_insight_*() functions, updated BUILT_INSIGHT_SLUGS to 17 slugs, uncommented 3 dispatch calls

## Decisions Made
- ART-17 uses os.path.exists() with empty list fallback so the build doesn't fail if jobs.json is missing
- Stat cards render computed values (total roles, remote %, median salary, salary range) that update automatically on each build
- Seniority distribution rendered as a sorted table showing counts and percentages

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed title length violations**
- **Found during:** Task 1 and Task 2
- **Issue:** CRM hygiene title was 44 chars (under 50 min), pulse report title was 46 then 61 chars
- **Fix:** Extended CRM title to "CRM Hygiene Automation Playbook for GTM Teams", adjusted pulse report to "Monthly GTM Pulse Report: Template With Data"
- **Files modified:** scripts/build.py
- **Verification:** Build passes with 0 new warnings

**2. [Rule 1 - Bug] Fixed banned word violations**
- **Found during:** Task 1
- **Issue:** "leverage" and "actually" in intent data article
- **Fix:** Replaced "highest-leverage" with "highest-impact", removed "actually"
- **Files modified:** scripts/build.py
- **Verification:** Build passes with 0 new warnings

---

**Total deviations:** 2 auto-fixed (2 bugs)
**Impact on plan:** Minor text corrections required by build validator. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- 3 remaining articles (ART-18 through ART-20) ready for Phase 15 Plan 03
- 3 commented dispatch calls remain for Plan 03 articles
- BUILT_INSIGHT_SLUGS at 17, needs 3 more for completion

---
*Phase: 15-insight-articles-batch-2*
*Completed: 2026-03-18*
