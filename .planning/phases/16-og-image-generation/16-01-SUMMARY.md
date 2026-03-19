---
phase: 16-og-image-generation
plan: 01
subsystem: build-pipeline
tags: [playwright, og-images, social-preview, meta-tags, screenshot]

requires:
  - phase: 15-insight-articles-batch-2
    provides: all 284 pages built and registered in ALL_PAGES
provides:
  - OG image generation pipeline (Playwright-based, 5 templates)
  - og:image and twitter:image meta tags on all 284 pages
  - --skip-og flag for fast dev builds
  - OG-04 validation rule in validate_pages()
affects: [deployment, social-sharing, seo]

tech-stack:
  added: [playwright]
  patterns: [bulk-screenshot-generation, auto-computed-og-paths]

key-files:
  created:
    - og-templates/og-default.html
    - og-templates/og-salary.html
    - og-templates/og-tool.html
    - og-templates/og-glossary.html
    - scripts/generate_og_images.py
  modified:
    - scripts/templates.py
    - scripts/build.py

key-decisions:
  - "Auto-compute og_image path from canonical_path in get_page_wrapper (zero changes to 100+ call sites)"
  - "Bulk OG registration by scanning ALL_PAGES after build, extracting title from generated HTML"
  - "Single Playwright browser instance with page reuse for 284 screenshots (~166s total)"

patterns-established:
  - "OG path convention: /assets/og/{canonical-path-with-hyphens}.png"
  - "Template selection by path prefix: salary/ -> og-salary, tools/ -> og-tool, etc."

requirements-completed: [OG-01, OG-02, OG-03, OG-04]

duration: 14min
completed: 2026-03-19
---

# Phase 16 Plan 01: OG Image Generation Summary

**Playwright-based OG pipeline generating branded 1200x630 PNG social previews for all 284 pages with 5 template variants**

## Performance

- **Duration:** 14 min
- **Started:** 2026-03-19T05:47:46Z
- **Completed:** 2026-03-19T06:01:46Z
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments
- 5 OG HTML templates with distinct visual treatments per page type (default, salary with stat callout, tool with category label, glossary with quote decoration, article)
- Playwright generator script renders all 284 pages in ~166 seconds using single browser instance
- og:image and twitter:image meta tags auto-injected on every page via get_page_wrapper
- OG-04 validation rule catches missing tags and missing PNG files
- --skip-og flag for fast dev builds (skips generation + validation)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create OG templates and generator script** - `de484f0` (feat)
2. **Task 2: Wire OG pipeline into build system** - `6437b5a` (feat)

## Files Created/Modified
- `og-templates/og-default.html` - General-purpose fallback template with prominent domain text
- `og-templates/og-salary.html` - Salary template with Source Code Pro stat callout and SALARY DATA label
- `og-templates/og-tool.html` - Tool template with category label and decorative grid squares
- `og-templates/og-glossary.html` - Glossary template with smaller title font and decorative quotation mark
- `scripts/generate_og_images.py` - Playwright batch renderer with template caching and progress reporting
- `scripts/templates.py` - Added og_image param to get_html_head(), auto-compute in get_page_wrapper()
- `scripts/build.py` - OG registration loop, generation call, OG-04 validation, --skip-og flag

## Decisions Made
- Auto-compute og_image path from canonical_path in get_page_wrapper so zero changes needed across 100+ write_page call sites
- Bulk register OG pages by scanning ALL_PAGES post-build and extracting title/description from generated HTML
- Single Playwright Chromium instance reused across all 284 screenshots for performance

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed 404.html generating invalid OG filename**
- **Found during:** Task 2 (build verification)
- **Issue:** 404.html produced og_filename "404.html.png" instead of "404.png" because the .html stripping only handled index.html
- **Fix:** Added .html suffix stripping to both og_filename_from_path() and get_page_wrapper() og_stem computation
- **Files modified:** scripts/generate_og_images.py, scripts/templates.py
- **Verification:** Full build passes with zero OG-04 warnings
- **Committed in:** 6437b5a (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Minor edge case fix for 404.html. No scope creep.

## Issues Encountered
None

## User Setup Required
None - Playwright must be installed on build machine (already noted in STATE.md blockers).

## Next Phase Readiness
- All 284 pages have branded OG images ready for social sharing
- Build pipeline fully integrated, ready for deployment

---
*Phase: 16-og-image-generation*
*Completed: 2026-03-19*
