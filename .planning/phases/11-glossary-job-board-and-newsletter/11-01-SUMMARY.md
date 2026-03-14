---
phase: 11-glossary-job-board-and-newsletter
plan: 01
subsystem: content
tags: [glossary, seo, python, static-site, importlib]

requires:
  - phase: 10-alternatives-and-roundups
    provides: build.py generator patterns, salary-header/salary-content CSS, content module loading via importlib
provides:
  - 50-term glossary content module (content/glossary.py) with definitions, bodies, and cross-links
  - Glossary index page at /glossary/ with category grouping
  - 50 individual term pages at /glossary/[slug]/ with BreadcrumbList schema
  - Navigation and footer links to glossary
affects: [12-final-quality, glossary-expansion]

tech-stack:
  added: []
  patterns: [glossary content module with GLOSSARY_TERMS dict keyed by slug, _load_glossary_content() pattern]

key-files:
  created:
    - content/glossary.py
  modified:
    - scripts/build.py
    - scripts/nav_config.py

key-decisions:
  - "Glossary terms use salary-header/salary-content CSS classes for visual consistency"
  - "Definition block styled with amber left border and tinted background"
  - "Title formula targets 50-60 char range with 3-tier fallback (long/mid/short variants)"

patterns-established:
  - "Glossary content module: GLOSSARY_TERMS dict keyed by slug with term, category, definition, body, related_links"
  - "Glossary generator: _load_glossary_content() loads from content module, build_glossary_index() and build_glossary_terms() generate pages"

requirements-completed: [GLOS-01, GLOS-02]

duration: 13min
completed: 2026-03-14
---

# Phase 11 Plan 01: Glossary Summary

**50-term GTM Engineering glossary with category-grouped index page, individual definition pages with BreadcrumbList schema, and cross-links to tool reviews, salary data, and career guides**

## Performance

- **Duration:** 13 min
- **Started:** 2026-03-14T17:50:42Z
- **Completed:** 2026-03-14T18:03:57Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Created content module with 50 glossary terms across 7 categories (Data & Enrichment, Outbound & Sequencing, Automation & Workflows, Analytics & Signals, Career & Industry, CRM & Pipeline, AI & LLM)
- Each term has practitioner-voice body text (200-500 words), definition, and related links to existing tool reviews, comparisons, salary pages, and career guides
- Glossary index at /glossary/ groups terms by category with definition preview cards
- Individual term pages have styled definition callout, body content, related links grid, and cross-category navigation
- Build produces 262 total pages (211 existing + 51 glossary)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create glossary content module with 50 GTM Engineering terms** - `10be9ac` (feat)
2. **Task 2: Add glossary generator infrastructure to build.py and nav** - `1b62ce8` (feat)

## Files Created/Modified
- `content/glossary.py` - 50 glossary term definitions with body text and related links
- `scripts/build.py` - GLOSSARY_TERMS list, _load_glossary_content(), build_glossary_index(), generate_glossary_term(), build_glossary_terms()
- `scripts/nav_config.py` - Added /glossary/ to NAV_ITEMS and FOOTER_COLUMNS Resources

## Decisions Made
- Glossary terms reuse salary-header/salary-content CSS classes for visual consistency with other verticals
- Definition block uses amber left-border callout style (tinted background, accent border)
- Title formula uses 3-tier fallback to stay within 50-60 char SEO range
- Related links combine content-module links (to specific tool reviews) with auto-generated same-category glossary links

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed banned words in glossary content**
- **Found during:** Task 2 (build verification)
- **Issue:** QUAL2-09 validator flagged "actually" (4 instances), "landscape" (2 instances), "positioning" (1 instance), and one false reframe pattern
- **Fix:** Replaced all banned words with alternatives and restructured the false reframe sentence
- **Files modified:** content/glossary.py
- **Verification:** Rebuild shows zero QUAL2-09 glossary warnings
- **Committed in:** 1b62ce8 (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 bug - banned words)
**Impact on plan:** Content quality fix required by CLAUDE.md writing standards. No scope creep.

## Issues Encountered
- Title length optimization required iterating through 3 title format variants to balance SEO requirements (50-60 chars) across terms of different name lengths. A few edge cases (48-49 chars) remain within acceptable tolerance.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Glossary vertical complete, ready for Phase 11 Plan 02 (Job Board) or Phase 12 (Final Quality)
- 262 total pages across all verticals
- All glossary pages have BreadcrumbList schema and cross-links to existing content

---
*Phase: 11-glossary-job-board-and-newsletter*
*Completed: 2026-03-14*
