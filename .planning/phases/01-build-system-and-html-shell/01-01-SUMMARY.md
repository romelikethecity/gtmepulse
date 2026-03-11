---
phase: 01-build-system-and-html-shell
plan: 01
subsystem: ui
tags: [python, css, html-shell, static-site-generator, json-ld, responsive]

requires:
  - phase: none
    provides: tokens.css design tokens and brand assets (pre-existing)
provides:
  - nav_config.py with site constants, NAV_ITEMS, FOOTER_COLUMNS
  - templates.py with 10 HTML/schema helper functions and write_page() + ALL_PAGES tracking
  - components.css with reusable component classes (cards, buttons, tables, breadcrumbs, stats, FAQ)
  - styles.css with nav, footer, responsive breakpoints at 768px and 480px
affects: [01-02, 01-03, 02-salary-pages, 02-tool-pages]

tech-stack:
  added: []
  patterns: [3-file-split, css-3-layer-cascade, json-dumps-schema, write-page-tracking]

key-files:
  created:
    - scripts/nav_config.py
    - scripts/templates.py
    - assets/css/components.css
    - assets/css/styles.css
  modified: []

key-decisions:
  - "Footer newsletter form included as non-functional HTML placeholder for Phase 1, JS handler deferred to Phase 2"
  - "Dropdown toggle uses separate button element with SVG chevron for accessibility (aria-expanded)"
  - "Newsletter CTA helper included as reusable component for embedding on any page"

patterns-established:
  - "3-file split: nav_config.py (pure data) -> templates.py (HTML shell) -> build.py (data + generators)"
  - "CSS cascade: tokens.css (variables) -> components.css (reusable) -> styles.css (page-scoped)"
  - "All schema uses json.dumps() for safe JSON-LD serialization"
  - "write_page() appends to ALL_PAGES for auto-sitemap generation"
  - "CSS cache busting via ?v={CSS_VERSION} on components.css and styles.css"

requirements-completed: [BUILD-02, BUILD-03, HTML-01, HTML-02, HTML-03, HTML-04, HTML-05, SEO-01, SEO-02, SEO-03, SEO-04]

duration: 3min
completed: 2026-03-10
---

# Phase 1 Plan 01: Config, Templates, and CSS Summary

**4-file foundation (nav_config.py, templates.py, components.css, styles.css) producing complete responsive HTML pages with JSON-LD schema from any body content string**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-11T06:19:45Z
- **Completed:** 2026-03-11T06:23:09Z
- **Tasks:** 2
- **Files created:** 4

## Accomplishments
- nav_config.py exports all site constants, NAV_ITEMS with Salary Data dropdown (6 children), and FOOTER_COLUMNS (3 columns)
- templates.py exports 10 functions: get_html_head, get_nav_html, get_footer_html, get_page_wrapper, write_page, get_homepage_schema, get_breadcrumb_schema, get_faq_schema, breadcrumb_html, newsletter_cta_html
- components.css provides 13 component groups (reset, links, headings, container, buttons, cards, stat blocks, breadcrumb, tables, FAQ, newsletter CTA, page header, related links) with zero hardcoded colors
- styles.css provides sticky nav with dropdown support, dark footer with newsletter form, main content area, and responsive breakpoints at 768px and 480px

## Task Commits

Each task was committed atomically:

1. **Task 1: Create nav_config.py and templates.py** - `fb1d172` (feat)
2. **Task 2: Create components.css and styles.css** - `70fd34f` (feat)

## Files Created/Modified
- `scripts/nav_config.py` - Site constants, NAV_ITEMS, FOOTER_COLUMNS (pure data, zero logic)
- `scripts/templates.py` - HTML shell components, schema helpers, write_page + ALL_PAGES tracking
- `assets/css/components.css` - Reusable component classes referencing --gtme-* tokens
- `assets/css/styles.css` - Nav, footer, main content, responsive breakpoints

## Decisions Made
- Footer newsletter form included as non-functional HTML placeholder (onsubmit="return false;"). JS handler wired in Phase 2 when Cloudflare Worker exists.
- Dropdown toggle uses separate button element with SVG chevron and aria-expanded for accessibility, rather than making the entire nav link a toggle.
- Newsletter CTA helper included as standalone reusable component for embedding across pages.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed CSS comment containing "!important" triggering false positive in verification**
- **Found during:** Task 2 (CSS verification)
- **Issue:** File header comment "Zero !important" contained the literal string, causing the no-!important assertion to fail
- **Fix:** Changed comment wording to "No forced specificity"
- **Files modified:** assets/css/components.css, assets/css/styles.css
- **Verification:** CSS checks pass with zero !important in any context
- **Committed in:** 70fd34f (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Trivial comment wording fix. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All 4 foundation files ready for build.py (Plan 02) to import and use
- templates.py can produce complete HTML pages from any body content string
- CSS cascade fully operational: tokens.css -> components.css -> styles.css
- Schema helpers ready for homepage (@graph), inner pages (BreadcrumbList), and FAQ pages (FAQPage)

---
*Phase: 01-build-system-and-html-shell*
*Completed: 2026-03-10*
