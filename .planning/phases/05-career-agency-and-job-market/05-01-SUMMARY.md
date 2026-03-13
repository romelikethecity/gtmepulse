---
phase: 05-career-agency-and-job-market
plan: 01
subsystem: content
tags: [career-guides, survey-data, seo, faq-schema, breadcrumbs]

requires:
  - phase: 04-salary-data-overhaul
    provides: salary page patterns (stats blocks, related links, source citations, FAQ schema)
provides:
  - Career index page at /careers/ with card grid linking to 6 guides
  - 6 career guide pages (how-to-become, operator-vs-engineer, is-real-career, job-market, how-got-jobs, work-life)
  - career_related_links() helper for cross-linking career pages
affects: [06-tool-reviews, 07-quality-sweep]

tech-stack:
  added: []
  patterns: [career page generator pattern matching salary analysis pages]

key-files:
  created:
    - output/careers/index.html
    - output/careers/how-to-become-gtm-engineer/index.html
    - output/careers/operator-vs-engineer/index.html
    - output/careers/is-gtm-engineering-real-career/index.html
    - output/careers/job-market-analysis/index.html
    - output/careers/how-gtm-engineers-got-jobs/index.html
    - output/careers/work-life-balance/index.html
  modified:
    - scripts/build.py

key-decisions:
  - "Career pages reuse salary-header, salary-stats, salary-content CSS classes for visual consistency"
  - "career_related_links() cross-links all 6 career pages plus salary index and coding premium"
  - "Career index uses salary-index-card grid pattern for consistency with salary index"

patterns-established:
  - "Career page pattern: eyebrow + H1 + stats grid + long-form content + FAQ + related links + citation + CTA"
  - "career_related_links(current_slug) for career page cross-linking"

requirements-completed: [CAREER-01, CAREER-02, CAREER-03, CAREER-04, CAREER-05, CAREER-06]

duration: 8min
completed: 2026-03-13
---

# Phase 5 Plan 1: Career Pages Summary

**6 career guides with survey-backed data (n=228): entry paths, operator/engineer bifurcation, job market growth, hiring patterns, and work-life balance**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-13T18:28:19Z
- **Completed:** 2026-03-13T18:36:28Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Career index page with card grid linking to all 6 guides, stats banner (228 surveyed, 5,205% growth, $135K median)
- 6 long-form career guides (2,000-2,400 words each), all with BreadcrumbList + FAQPage schema, source citations, 3+ internal links
- career_related_links() helper cross-linking all career pages plus salary data
- Site now at 62 pages total (55 prior + 7 career pages)

## Task Commits

Each task was committed atomically:

1. **Task 1: Career index + first 3 career pages** - `5635601` (feat)
2. **Task 2: Career pages 4-6** - `b11501f` (feat)

## Files Created/Modified
- `scripts/build.py` - Added CAREER_PAGES data, career_related_links(), build_career_index(), and 6 build_career_* functions
- `output/careers/index.html` - Career landing page with card grid
- `output/careers/how-to-become-gtm-engineer/index.html` - CAREER-01: self-taught paths, skills, timelines
- `output/careers/operator-vs-engineer/index.html` - CAREER-02: $45K gap, bimodal distribution
- `output/careers/is-gtm-engineering-real-career/index.html` - CAREER-03: 5,205% growth, longevity argument
- `output/careers/job-market-analysis/index.html` - CAREER-04: posting trends, top countries, salary bands
- `output/careers/how-gtm-engineers-got-jobs/index.html` - CAREER-05: entry paths, hiring patterns
- `output/careers/work-life-balance/index.html` - CAREER-06: hours, agency vs in-house, burnout

## Decisions Made
- Career pages reuse salary-header, salary-stats, and salary-content CSS classes for visual consistency across the site
- career_related_links() includes salary cross-links (salary index + coding premium) to strengthen internal linking between content verticals
- Career index uses the same salary-index-card grid pattern established in 04-03

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed banned word "actually" in how-to-become page**
- **Found during:** Task 1
- **Issue:** Two instances of "actually" (banned word per CLAUDE.md) in body content
- **Fix:** Removed both instances, rephrased sentences
- **Committed in:** 5635601

**2. [Rule 1 - Bug] Fixed title length for how-to-become page**
- **Found during:** Task 1
- **Issue:** Title was 49 chars, validator requires 50-60
- **Fix:** Changed from "How to Become a GTM Engineer in 2026" to "How to Become a GTM Engineer: 2026 Guide"
- **Committed in:** 5635601

**3. [Rule 1 - Bug] Fixed banned word "leverage" in job-market page**
- **Found during:** Task 2
- **Issue:** Two instances of "leverage" in body content
- **Fix:** Replaced with "negotiating power" and "advantage"
- **Committed in:** b11501f

---

**Total deviations:** 3 auto-fixed (3 Rule 1 bugs - banned words and title length)
**Impact on plan:** All fixes required for content validation to pass. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Career pages live and cross-linked to salary data
- Nav already has /careers/ link (configured in 04-03)
- Ready for Phase 05 Plan 02 (additional career content) or Phase 06 (tool reviews)

---
*Phase: 05-career-agency-and-job-market*
*Completed: 2026-03-13*
