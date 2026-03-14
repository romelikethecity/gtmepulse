---
phase: 10-alternatives-and-roundups
verified: 2026-03-14T17:30:00Z
status: passed
score: 8/8 must-haves verified
re_verification: false
---

# Phase 10: Alternatives and Roundups Verification Report

**Phase Goal:** Users searching for "[Tool] alternatives" or "best [category] tools" find comprehensive, opinionated pages with clear recommendations
**Verified:** 2026-03-14T17:30:00Z
**Status:** passed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | User can find 10 alternatives pages listing 5-8 alternatives each with pros, cons, and pricing | VERIFIED | 10 pages in output/tools/*-alternatives/, each with 5-7 alternatives, pros/cons grids, pricing, verdict |
| 2 | User can find 10 best-for roundup pages with ranked recommendations and use-case guidance | VERIFIED | 10 pages in output/tools/best-*/, each with 3-8 ranked tools, best-for tags, why-picked, pricing |
| 3 | Every alternatives page has FAQ section with 3+ Q&A and FAQPage JSON-LD schema | VERIFIED | All 10 alternatives pages have FAQPage schema (grep confirmed), 4 FAQ pairs each |
| 4 | Every roundup page has FAQ section with 3+ Q&A and FAQPage JSON-LD schema | VERIFIED | All 10 roundup pages have FAQPage schema (grep confirmed), 3-4 FAQ pairs each |
| 5 | Alternatives pages cross-link to tool reviews and comparison pages | VERIFIED | Clay alternatives page has 9 review links; related links grid includes comparisons |
| 6 | Roundup pages cross-link to reviews, comparisons, and alternatives | VERIFIED | roundup_related_links() references TOOL_ALTERNATIVES, TOOL_ROUNDUPS, TOOL_CATEGORIES; startups roundup has 7 review links |
| 7 | Build completes with all 20 pages in output | VERIFIED | Build produces 211 total pages, all 10 alternatives + 10 roundups present |
| 8 | Every page has BreadcrumbList JSON-LD | VERIFIED | All 20 pages confirmed via grep |

**Score:** 8/8 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `scripts/build.py` | TOOL_ALTERNATIVES, TOOL_ROUNDUPS, generators | VERIFIED | TOOL_ALTERNATIVES (line 6320), TOOL_ROUNDUPS (line 6544), all 4 generator functions present, wired in main() at lines 12226-12227 |
| `content/alternatives_enrichment.py` | Clay, Apollo, ZoomInfo alternatives | VERIFIED | 32KB, ALTERNATIVES dict with 3 entries, each 5-7 alternatives, 4 FAQs |
| `content/alternatives_outbound.py` | Instantly, Outreach alternatives | VERIFIED | 19KB, ALTERNATIVES dict with 2 entries |
| `content/alternatives_crm.py` | HubSpot, Salesforce alternatives | VERIFIED | 20KB, ALTERNATIVES dict with 2 entries |
| `content/alternatives_automation.py` | Zapier alternatives | VERIFIED | 9.7KB, ALTERNATIVES dict with 1 entry, 5 alternatives |
| `content/alternatives_intent.py` | 6sense alternatives | VERIFIED | 11KB, ALTERNATIVES dict with 1 entry, 6 alternatives |
| `content/alternatives_linkedin.py` | Sales Navigator alternatives | VERIFIED | 11KB, ALTERNATIVES dict with 1 entry, 6 alternatives |
| `content/roundups_startup.py` | Startup + enterprise roundups | VERIFIED | 18KB, ROUNDUPS dict with 2 entries (6 and 5 tools) |
| `content/roundups_free.py` | Free + AI tools roundups | VERIFIED | 16KB, ROUNDUPS dict with 2 entries (5 and 4 tools) |
| `content/roundups_category.py` | 6 category roundups | VERIFIED | 50KB, ROUNDUPS dict with 6 entries (3-8 tools each) |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `scripts/build.py` | `content/alternatives_*.py` | `_load_alternative_content()` importlib | WIRED | Called at line 6430 inside generate_tool_alternative() |
| `scripts/build.py` | `content/roundups_*.py` | `_load_roundup_content()` importlib | WIRED | Called at line 6649 inside generate_tool_roundup() |
| `generate_tool_alternative()` | `faq_html, get_faq_schema, get_breadcrumb_schema` | function calls | WIRED | Lines 6441-6449, schema in extra_head at lines 6519-6521 |
| `generate_tool_roundup()` | `faq_html, get_faq_schema, get_breadcrumb_schema` | function calls | WIRED | Confirmed in generate_tool_roundup function body |
| `roundup_related_links()` | `TOOL_ALTERNATIVES, TOOL_ROUNDUPS` | cross-links | WIRED | Lines 6620-6625 iterate both data lists |
| `main()` | `build_tool_alternatives(), build_tool_roundups()` | function calls | WIRED | Lines 12226-12227 |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| TALT-01 | 10-01 | Clay alternatives | SATISFIED | content/alternatives_enrichment.py key "clay", 7 alternatives, output page exists |
| TALT-02 | 10-01 | Apollo alternatives | SATISFIED | content/alternatives_enrichment.py key "apollo", 6 alternatives |
| TALT-03 | 10-01 | ZoomInfo alternatives | SATISFIED | content/alternatives_enrichment.py key "zoominfo", 6 alternatives |
| TALT-04 | 10-01 | Instantly alternatives | SATISFIED | content/alternatives_outbound.py key "instantly", 6 alternatives |
| TALT-05 | 10-01 | Outreach alternatives | SATISFIED | content/alternatives_outbound.py key "outreach", 5 alternatives |
| TALT-06 | 10-01 | HubSpot alternatives | SATISFIED | content/alternatives_crm.py key "hubspot", 5 alternatives |
| TALT-07 | 10-01 | Salesforce alternatives | SATISFIED | content/alternatives_crm.py key "salesforce", 6 alternatives |
| TALT-08 | 10-01 | Zapier alternatives | SATISFIED | content/alternatives_automation.py key "zapier", 5 alternatives |
| TALT-09 | 10-01 | 6sense alternatives | SATISFIED | content/alternatives_intent.py key "6sense", 6 alternatives |
| TALT-10 | 10-01 | Sales Navigator alternatives | SATISFIED | content/alternatives_linkedin.py key "linkedin-sales-navigator", 6 alternatives |
| TBST-01 | 10-02 | Best GTM tools for startups | SATISFIED | content/roundups_startup.py, 6 ranked tools |
| TBST-02 | 10-02 | Best GTM tools for enterprise | SATISFIED | content/roundups_startup.py, 5 ranked tools |
| TBST-03 | 10-02 | Best free GTM tools | SATISFIED | content/roundups_free.py, 5 ranked tools |
| TBST-04 | 10-02 | Best data enrichment tools | SATISFIED | content/roundups_category.py, 8 ranked tools |
| TBST-05 | 10-02 | Best outbound sequencing tools | SATISFIED | content/roundups_category.py, 6 ranked tools |
| TBST-06 | 10-02 | Best CRM for GTM Engineers | SATISFIED | content/roundups_category.py, 5 ranked tools |
| TBST-07 | 10-02 | Best workflow automation tools | SATISFIED | content/roundups_category.py, 3 ranked tools |
| TBST-08 | 10-02 | Best AI tools for GTM | SATISFIED | content/roundups_free.py, 4 ranked tools |
| TBST-09 | 10-02 | Best LinkedIn prospecting tools | SATISFIED | content/roundups_category.py, 3 ranked tools |
| TBST-10 | 10-02 | Best intent data platforms | SATISFIED | content/roundups_category.py, 3 ranked tools |

All 20 requirements satisfied. No orphaned requirements found.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (none) | - | - | - | Zero TODOs, FIXMEs, PLACEHOLDERs, or stubs found across all 9 content modules |

### Build Warnings (Phase 10 pages)

16 QUAL2-01 (title length) warnings and 2 QUAL2-04 (word count) warnings on Phase 10 pages. These are minor quality items:
- Title length warnings: most titles are 2-5 chars outside the 50-60 target range (either too short or too long)
- Word count warnings: best-workflow-automation-tools (903 words) and best-linkedin-prospecting-tools (935 words) are slightly under the 1000-word threshold

These are cosmetic SEO optimization items, not goal blockers. Zero QUAL2-09 (banned words) warnings on Phase 10 pages.

### Human Verification Required

### 1. Visual Layout of Alternatives Pages

**Test:** Open http://localhost:8090/tools/clay-alternatives/ and review the pros/cons grid, pricing sections, and related links
**Expected:** Two-column pros (green) / cons (red) grid renders cleanly, pricing is visible, related links show reviews and comparisons
**Why human:** Visual layout and color rendering cannot be verified programmatically

### 2. Roundup Ranking Presentation

**Test:** Open http://localhost:8090/tools/best-data-enrichment-tools/ and check that tools are numbered #1-#8 with clear ranking
**Expected:** Tools appear in ranked order with category badges, best-for summaries, and review links
**Why human:** Visual hierarchy and scannability of ranked list requires human assessment

### 3. Cross-Link Navigation Flow

**Test:** From a roundup page, click through to a tool review, then to a comparison, then to an alternatives page
**Expected:** All cross-links resolve to real pages, navigation flow feels natural
**Why human:** Navigation flow quality is subjective and requires clicking through

---

_Verified: 2026-03-14T17:30:00Z_
_Verifier: Claude (gsd-verifier)_
