---
gsd_state_version: 1.0
milestone: v3.0
milestone_name: Tool Reviews, Glossary, and Infrastructure
status: defining_requirements
stopped_at: Defining requirements
last_updated: "2026-03-14T06:30:00.000Z"
last_activity: 2026-03-14 — Milestone v3.0 started
progress:
  total_phases: 0
  completed_phases: 0
  total_plans: 0
  completed_plans: 0
  percent: 0
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-13)

**Core value:** GTM Engineers can find accurate, vendor-neutral salary benchmarks and career intelligence in one place, with data no competitor provides.
**Current focus:** v3.0 Tool Reviews, Glossary, and Infrastructure. Defining requirements.

## Current Position

Phase: Not started (defining requirements)
Plan: —
Status: Defining requirements
Last activity: 2026-03-14 — Milestone v3.0 started

Progress: [░░░░░░░░░░] 0%

## Performance Metrics

**Velocity:**
- Total plans completed: 15
- Average duration: 7min
- Total execution time: 111min

*Updated after each plan completion*

## Accumulated Context

### Decisions

- [v1.0]: 3-phase Wave 1 structure (build system -> core pages + newsletter -> salary engine)
- [v1.0 01-01]: 3-file split pattern: nav_config.py -> templates.py -> build.py
- [v1.0 01-01]: CSS cascade: tokens.css -> components.css -> styles.css
- [v2.0]: Real State of GTME Report 2026 data (n=228) replaces hardcoded estimates
- [v2.0]: Every data page cites "Source: State of GTM Engineering Report 2026 (n=228)"
- [v2.0 Roadmap]: SALUP first (data layer), then content phases, QUAL2 validated in final sweep
- [v2.0 04-01]: US respondents (132) used for location pages, full 228 for aggregate/remote/stage
- [v2.0 04-01]: source_citation_html() pattern established for all data pages
- [v2.0 04-02]: Custom stats block for bonus page (percentages, not salary ranges) using same CSS classes
- [v2.0 04-02]: Analysis pages use 'analysis' type in salary_related_links for cross-linking
- [v2.0 04-03]: Custom stats blocks for equity percentages, agency fees, and geographic comparisons reuse salary-stat-card CSS
- [v2.0 04-03]: Salary index "More Salary Data" section with cards for all 12 analysis pages
- [v2.0 04-03]: Nav dropdown limited to 3 new entries to avoid overcrowding; all pages accessible via index
- [v2.0 05-01]: Career pages reuse salary-header, salary-stats, salary-content CSS classes for visual consistency
- [v2.0 05-01]: career_related_links() cross-links all career pages plus salary index and coding premium
- [v2.0 05-01]: Career index uses salary-index-card grid pattern for consistency with salary index
- [v2.0 05-02]: career_related_links() limit increased from 8 to 12 for all career pages
- [v2.0 05-02]: CAREER_PAGES array expanded to 12 entries as single source of truth for index and cross-links
- [v2.0 05-03]: AGENCY_PAGES array pattern mirrors CAREER_PAGES for consistency
- [v2.0 05-03]: Agency pages live under /careers/ path (not a separate section)
- [v2.0 05-03]: agency_related_links() cross-links all 8 agency pages plus salary agency fee pages
- [v2.0 05-04]: JOBMKT_PAGES array and jobmkt_related_links() follow same pattern as CAREER_PAGES and AGENCY_PAGES
- [v2.0 05-04]: Careers nav converted to dropdown with 4 children entries
- [v2.0 05-04]: Career index three-section layout: Career Guides (12) + Agency (8) + Job Market (8)
- [v2.0 05-04]: CSS_VERSION bumped to 10 for nav/footer structural changes
- [v2.0 06-01]: TOOL_PAGES array (16 entries) + BUILT_TOOL_SLUGS set for incremental tool page publishing
- [v2.0 06-01]: Tool pages under /tools/ path as own section, tool_related_links() cross-links built pages + salary
- [v2.0 06-02]: TOOL_PAGES expanded to 22 entries, BUILT_TOOL_SLUGS to 11 pages
- [v2.0 06-02]: Unify analysis written as honest criticism: 8.8% vs Clay 84%
- [v2.0 06-02]: Frustrations/wishlist/most-exciting cross-linked as content cluster
- [v2.0 06-03]: TOOL_PAGES expanded to 27 entries, BUILT_TOOL_SLUGS to 16 pages
- [v2.0 06-03]: Tools nav converted to dropdown with 4 children (Index, Tech Stack, Clay, Frustrations)
- [v2.0 06-03]: Footer Resources expanded with Tech Stack Benchmark and Tool Frustrations links
- [v2.0 06-03]: CSS_VERSION bumped to 11 for nav/footer structural changes
- [v2.0 06-04]: BENCH_PAGES array (9 entries) as single source of truth for index and cross-links
- [v2.0 06-04]: Benchmarks nav entry as simple link (not dropdown) since 9 pages don't need subcategory navigation
- [v2.0 06-04]: bench_related_links() cross-links all benchmark pages plus salary/tools/career indexes (limit 12)
- [v2.0 06-04]: CSS_VERSION bumped to 12 for nav/footer structural changes
- [v2.0 07-01]: COMP_PAGES array (6 entries) as single source of truth for index and cross-links
- [v2.0 07-01]: Comparisons nav entry as simple link (not dropdown) since 6 pages don't need subcategory navigation
- [v2.0 07-01]: comparison_related_links() cross-links all comparison pages plus salary/tools/careers/benchmarks indexes (limit 12)
- [v2.0 07-01]: CSS_VERSION bumped to 13 for nav/footer structural changes
- [v2.0 07-02]: BLOG_PAGES array (14 entries) with BUILT_BLOG_SLUGS gating, same incremental publishing pattern as tools
- [v2.0 07-02]: Blog articles use salary-header/salary-content CSS classes for visual consistency (no new CSS)
- [v2.0 07-02]: Each blog article includes author byline (By Rome Thorndike) for editorial credibility
- [v2.0 07-03]: BUILT_BLOG_SLUGS expanded to 14 entries, completing all blog articles
- [v2.0 07-03]: Blog nav entry as simple link after Comparisons, before Careers
- [v2.0 07-03]: CSS_VERSION bumped to 14 for nav/footer structural changes
- [v2.0 07-04]: Word count thresholds set per page type: data pages 1000+, blog 1300+, calculator 500+
- [v2.0 07-04]: validate_pages() enhanced with 9 QUAL2 check categories (SEO, breadcrumbs, links, FAQ, duplicates, citations, writing, word counts)
- [v2.0 07-04]: Salary template pages expanded with job market, negotiation, cost-of-living, and tool stack sections

### Pending Todos

None yet.

### Blockers/Concerns

- Wave 1 Phase 1 is 50% complete. v2.0 phases depend on Wave 1 build system and salary pages existing.
- Content volume (~85 pages) needs efficient page generator patterns. Build on existing salary page generators.
- QUAL2 standards enforced per-page during build but formally validated in Phase 7 sweep.

## Session Continuity

Last session: 2026-03-14T05:18:24Z
Stopped at: Completed 07-04-PLAN.md
Resume file: None
