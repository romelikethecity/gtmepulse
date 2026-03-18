---
phase: 14-insight-articles-batch-1
plan: 01
subsystem: content
tags: [article, json-ld, insights, seo, schema-markup]

requires:
  - phase: 13-analytics-and-newsletter-go-live
    provides: GA4 analytics, newsletter infrastructure, deploy pipeline
provides:
  - get_article_schema() helper in templates.py for Article JSON-LD
  - INSIGHT_PAGES registry (10 entries) and BUILT_INSIGHT_SLUGS set (4)
  - insight_related_links() and build_insights_index() functions
  - 4 data analysis articles (job market, salary trends, tool adoption, state of GTME)
  - insights/ validator integration (DATA_DIRS, word count 1300+ floor)
  - Insights nav and footer entries
affects: [14-02-PLAN, 14-03-PLAN, content-expansion]

tech-stack:
  added: []
  patterns: [Article JSON-LD schema with Person author, insight article build pattern cloned from blog]

key-files:
  created:
    - output/insights/index.html
    - output/insights/job-market-2026/index.html
    - output/insights/salary-trends/index.html
    - output/insights/tool-adoption/index.html
    - output/insights/state-of-gtme-2026/index.html
  modified:
    - scripts/templates.py
    - scripts/build.py
    - scripts/nav_config.py

key-decisions:
  - "Cloned blog pattern for insight articles (salary-header + salary-stats + salary-content layout)"
  - "Category badges on insight index cards (Market Analysis vs Playbook)"
  - "Insight article word count floor set to 1300 to match blog"

patterns-established:
  - "Insight article pattern: get_article_schema() + breadcrumb + salary-header + salary-stats + salary-content + source_citation + newsletter_cta + insight_related_links"

requirements-completed: [ART-01, ART-02, ART-03, ART-04]

duration: 9min
completed: 2026-03-18
---

# Phase 14 Plan 01: Insight Articles Infrastructure + Data Analysis Articles Summary

**Article JSON-LD schema helper, insights index page, and 4 data-analysis articles (job market, salary trends, tool adoption, state of GTME 2026) with full validator integration**

## Performance

- **Duration:** 9 min
- **Started:** 2026-03-18T07:12:23Z
- **Completed:** 2026-03-18T07:21:23Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Built get_article_schema() helper generating Article JSON-LD with Person author markup
- Created INSIGHT_PAGES registry (10 entries) with BUILT_INSIGHT_SLUGS (4 built)
- Built insights index page with category badges and card grid
- Delivered 4 data-analysis articles: job market 2026, salary trends, tool adoption, state of GTME 2026
- Each article has 1,500-2,300 words, 3+ internal links, 2+ outbound citations
- Added insights/ to DATA_DIRS with 1300+ word count floor in validator
- Added Insights to nav Resources dropdown and footer

## Task Commits

Each task was committed atomically:

1. **Task 1: Article infrastructure** - `320087a` (feat)
2. **Task 2: Data analysis articles ART-01 through ART-04** - `926c4b2` (feat)

## Files Created/Modified
- `scripts/templates.py` - Added get_article_schema() for Article JSON-LD
- `scripts/build.py` - Added INSIGHT_PAGES, index, 4 article functions, validator updates
- `scripts/nav_config.py` - Added Insights to Resources dropdown + footer, bumped CSS_VERSION to 17

## Decisions Made
- Cloned blog article pattern for consistency (salary-header + salary-stats + salary-content)
- Added category badges to insight index cards to differentiate Market Analysis from Playbook
- Set insights word count floor to 1300 (matching blog articles)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed banned words and false reframe patterns in article content**
- **Found during:** Task 2 (article content)
- **Issue:** Validator flagged "leverage", "actually", "landscape", "resonates" and false reframe patterns
- **Fix:** Replaced all banned words and restructured flagged sentences
- **Files modified:** scripts/build.py
- **Verification:** Build produces zero new warnings
- **Committed in:** 926c4b2 (Task 2 commit)

**2. [Rule 1 - Bug] Fixed word count below 1300 floor for job-market and salary-trends articles**
- **Found during:** Task 2 (article content)
- **Issue:** job-market-2026 had 1250 words, salary-trends had 1297 words
- **Fix:** Added additional content sections to both articles
- **Files modified:** scripts/build.py
- **Verification:** Both articles now pass 1300+ word count check
- **Committed in:** 926c4b2 (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (2 bugs)
**Impact on plan:** Both fixes necessary for build validation. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Insight article infrastructure ready for Plans 02 and 03 (6 remaining playbook articles)
- BUILT_INSIGHT_SLUGS set ready to be expanded as new articles are added
- build_insights_index() automatically shows only articles in BUILT_INSIGHT_SLUGS

---
*Phase: 14-insight-articles-batch-1*
*Completed: 2026-03-18*
