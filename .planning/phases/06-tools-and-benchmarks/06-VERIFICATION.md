---
phase: 06-tools-and-benchmarks
verified: 2026-03-13T23:15:00Z
status: passed
score: 4/4 must-haves verified
gaps: []
human_verification:
  - test: "Browse /tools/ and /benchmarks/ sections end-to-end"
    expected: "All pages load, cards link correctly, nav dropdown works, no layout issues"
    why_human: "Visual layout and card rendering can't be verified programmatically"
  - test: "Read Clay page for honest criticism quality"
    expected: "Both praise and criticism feel genuine, not templated pro/con filler"
    why_human: "Writing quality and tone require subjective evaluation"
  - test: "Verify 50 Key Stats page scannability"
    expected: "Stats are visually organized by category, each links to its detail page"
    why_human: "Visual hierarchy and UX scannability require human review"
---

# Phase 6: Tools and Benchmarks Verification Report

**Phase Goal:** Visitors can explore the full GTM Engineer tech stack (adoption rates, frustrations, spend) and industry benchmarks (demographics, bottlenecks, predictions) through 25 data-reference pages
**Verified:** 2026-03-13T23:15:00Z
**Status:** passed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Tech stack benchmark page shows adoption rates for every major tool category (Clay 84%, CRM 92%, AI coding 71%, n8n 54%) with agency vs in-house splits | VERIFIED | `output/tools/tech-stack-benchmark/index.html` exists (1,791 words), contains all four adoption percentages, 17 mentions of "agency" for agency/in-house splits |
| 2 | Individual tool pages (Clay, Python, SQL, Zapier vs n8n, HubSpot vs Salesforce) provide adoption data, salary impact, and honest criticism | VERIFIED | All 5 pages exist with 1,400-1,927 words each. Clay has 84%/96% data with "most frustrating" criticism. Python ties to $45K premium. Zapier vs n8n shows 54% n8n adoption. HubSpot vs Salesforce covers 92% CRM by company size. |
| 3 | Benchmark pages cover the full "state of" picture: 50 key stats, demographics, bottlenecks, headcount trends, and future predictions | VERIFIED | All 9 benchmark pages exist (1,591-1,884 words). 50 stats page has category-organized data. Demographics shows 228/32 countries. Bottlenecks has 25%/17%/8%. Future predictions has 9.6% RevOps convergence. |
| 4 | Every page meets content depth (1,200-2,000 words) and has working internal links to related salary, career, and tool pages | VERIFIED | All 25 content pages exceed 1,200 words. Every tool page has 18-20 salary cross-links. Every benchmark page has 9-33 salary links and 9-23 tool links. All pages have BreadcrumbList + FAQPage schema and source citations. |

**Score:** 4/4 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `output/tools/index.html` | Tools index with category cards | VERIFIED | 1,512 words, 24 tool links, card grid |
| `output/tools/tech-stack-benchmark/index.html` | Full tech stack benchmark | VERIFIED | 1,791 words, all adoption rates, agency splits |
| `output/tools/clay/index.html` | Clay adoption deep-dive | VERIFIED | 1,816 words, 84%/96% data, frustration analysis |
| `output/tools/crm-adoption/index.html` | CRM adoption analysis | VERIFIED | 1,440 words, 92% adoption, SF/HS split |
| `output/tools/ai-coding-tools/index.html` | AI coding tools | VERIFIED | 1,633 words, 71% adoption, Cursor/Claude Code |
| `output/tools/n8n-adoption/index.html` | n8n adoption analysis | VERIFIED | 1,526 words, 54% adoption, agency economics |
| `output/tools/frustrations/index.html` | Tool frustrations | VERIFIED | 1,948 words, integration/UX/docs complaints |
| `output/tools/most-exciting/index.html` | Most exciting tools | VERIFIED | 1,687 words, Claude 39/Cursor 11/n8n 8 |
| `output/tools/unify-analysis/index.html` | Unify honest critique | VERIFIED | 1,560 words, 8.8% adoption data |
| `output/tools/annual-spend/index.html` | Annual tool spend | VERIFIED | 1,706 words, $5-25K agency data |
| `output/tools/zoominfo-vs-apollo/index.html` | ZoomInfo vs Apollo | VERIFIED | 1,740 words, 65% enrichment adoption |
| `output/tools/tool-wishlist/index.html` | Tool wishlist | VERIFIED | 1,707 words, all-in-one outbound data |
| `output/tools/python/index.html` | Python for GTMEs | VERIFIED | 1,927 words, $45K premium, learning path |
| `output/tools/sql/index.html` | SQL for GTMEs | VERIFIED | 1,787 words, ~25% posting frequency |
| `output/tools/javascript/index.html` | JavaScript for GTMEs | VERIFIED | 1,820 words, JS vs Python comparison |
| `output/tools/zapier-vs-n8n/index.html` | Zapier vs n8n comparison | VERIFIED | 1,765 words, 54% n8n, pricing model comparison |
| `output/tools/hubspot-vs-salesforce/index.html` | HubSpot vs Salesforce | VERIFIED | 1,808 words, 92% CRM by company size |
| `output/benchmarks/index.html` | Benchmarks index | VERIFIED | 1,102 words, 15 benchmark links, card grid |
| `output/benchmarks/50-stats/index.html` | 50 key stats roundup | VERIFIED | 1,720 words, 5 categories, detail page links |
| `output/benchmarks/demographics/index.html` | Demographics deep-dive | VERIFIED | 1,679 words, 228 respondents, 32 countries |
| `output/benchmarks/report-summary/index.html` | Report analysis | VERIFIED | 1,591 words, editorial commentary |
| `output/benchmarks/operator-vs-engineer/index.html` | Operator vs engineer | VERIFIED | 1,840 words, $45K gap, bimodal data |
| `output/benchmarks/bottlenecks/index.html` | GTM bottlenecks | VERIFIED | 1,803 words, 25%/17%/8% data |
| `output/benchmarks/company-understanding/index.html` | Company understanding | VERIFIED | 1,820 words, 45%/9% findings |
| `output/benchmarks/learning-resources/index.html` | Learning resources | VERIFIED | 1,838 words, LinkedIn 174 mentions |
| `output/benchmarks/headcount-trends/index.html` | Headcount trends | VERIFIED | 1,775 words, growth intent data |
| `output/benchmarks/future-predictions/index.html` | Future predictions | VERIFIED | 1,884 words, 9.6% RevOps convergence |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| Tools index | All 16 tool pages | Card grid links | WIRED | 24 /tools/ links in index (16 pages + nav/footer repeats) |
| Benchmarks index | All 9 benchmark pages | Card grid links | WIRED | 15 /benchmarks/ links in index |
| Tool pages | /salary/ pages | tool_related_links() | WIRED | 18-20 salary links per tool page |
| Benchmark pages | /salary/ and /tools/ | bench_related_links() | WIRED | 9-33 salary + 9-23 tools links per page |
| Nav | /tools/ | Tools dropdown (4 children) | WIRED | Dropdown with Index, Tech Stack, Clay, Frustrations |
| Nav | /benchmarks/ | Simple link | WIRED | "Benchmarks" entry in nav after Tools |
| Footer | Tools + Benchmarks | Resources column | WIRED | 5 links: GTM Tools, Tech Stack, Frustrations, Benchmarks, 50 Stats |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-----------|-------------|--------|----------|
| TOOL-01 | 06-01 | Tech stack benchmark page | SATISFIED | `output/tools/tech-stack-benchmark/index.html` (1,791 words) |
| TOOL-02 | 06-01 | Clay deep-dive (84%, 96%, most loved/frustrating) | SATISFIED | `output/tools/clay/index.html` (1,816 words) |
| TOOL-03 | 06-01 | CRM adoption (92%) | SATISFIED | `output/tools/crm-adoption/index.html` (1,440 words) |
| TOOL-04 | 06-01 | AI coding tools (71%) | SATISFIED | `output/tools/ai-coding-tools/index.html` (1,633 words) |
| TOOL-05 | 06-01 | n8n adoption (54%) | SATISFIED | `output/tools/n8n-adoption/index.html` (1,526 words) |
| TOOL-06 | 06-02 | Tool frustrations page | SATISFIED | `output/tools/frustrations/index.html` (1,948 words) |
| TOOL-07 | 06-02 | Most exciting tools (Claude 39, Cursor 11, n8n 8) | SATISFIED | `output/tools/most-exciting/index.html` (1,687 words) |
| TOOL-08 | 06-02 | Unify analysis (8.8%) | SATISFIED | `output/tools/unify-analysis/index.html` (1,560 words) |
| TOOL-09 | 06-02 | Annual tool spend | SATISFIED | `output/tools/annual-spend/index.html` (1,706 words) |
| TOOL-10 | 06-02 | ZoomInfo vs Apollo (65%) | SATISFIED | `output/tools/zoominfo-vs-apollo/index.html` (1,740 words) |
| TOOL-11 | 06-02 | Tool wishlist | SATISFIED | `output/tools/tool-wishlist/index.html` (1,707 words) |
| TOOL-12 | 06-03 | Python for GTMEs | SATISFIED | `output/tools/python/index.html` (1,927 words) |
| TOOL-13 | 06-03 | SQL for GTMEs | SATISFIED | `output/tools/sql/index.html` (1,787 words) |
| TOOL-14 | 06-03 | Zapier vs n8n | SATISFIED | `output/tools/zapier-vs-n8n/index.html` (1,765 words) |
| TOOL-15 | 06-03 | HubSpot vs Salesforce | SATISFIED | `output/tools/hubspot-vs-salesforce/index.html` (1,808 words) |
| TOOL-16 | 06-03 | JavaScript for GTMEs | SATISFIED | `output/tools/javascript/index.html` (1,820 words) |
| BENCH-01 | 06-04 | 50 key stats roundup | SATISFIED | `output/benchmarks/50-stats/index.html` (1,720 words) |
| BENCH-02 | 06-04 | Demographics (228 respondents, 32 countries) | SATISFIED | `output/benchmarks/demographics/index.html` (1,679 words) |
| BENCH-03 | 06-04 | Report summary/analysis | SATISFIED | `output/benchmarks/report-summary/index.html` (1,591 words) |
| BENCH-04 | 06-04 | Operator vs engineer divide | SATISFIED | `output/benchmarks/operator-vs-engineer/index.html` (1,840 words) |
| BENCH-05 | 06-04 | Bottlenecks (25%, 17%, 8%) | SATISFIED | `output/benchmarks/bottlenecks/index.html` (1,803 words) |
| BENCH-06 | 06-04 | Company understanding (45%, 9%) | SATISFIED | `output/benchmarks/company-understanding/index.html` (1,820 words) |
| BENCH-07 | 06-04 | Learning resources (LinkedIn 174) | SATISFIED | `output/benchmarks/learning-resources/index.html` (1,838 words) |
| BENCH-08 | 06-04 | Headcount trends | SATISFIED | `output/benchmarks/headcount-trends/index.html` (1,775 words) |
| BENCH-09 | 06-04 | Future predictions (AI, RevOps 9.6%) | SATISFIED | `output/benchmarks/future-predictions/index.html` (1,884 words) |

All 25 requirements (TOOL-01 through TOOL-16, BENCH-01 through BENCH-09) are SATISFIED. No orphaned requirements.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `output/tools/ai-coding-tools/index.html` | 166 | "robustness" (derivative of banned word "robust") | Info | Technical usage in error-handling context, not AI buzzword fluff. Borderline. |

No TODOs, FIXMEs, placeholders, empty implementations, or stub content found in any tool or benchmark page.

### Human Verification Required

### 1. Visual Layout Check
**Test:** Browse /tools/ and /benchmarks/ index pages and 3-4 content pages
**Expected:** Card grids render correctly, stat badges display, no layout overflow on mobile
**Why human:** CSS rendering and responsive behavior need visual inspection

### 2. Content Quality Spot Check
**Test:** Read Clay page and Unify page for writing quality
**Expected:** Clay has genuine criticism (not templated pro/con). Unify honestly assesses 8.8% without softening.
**Why human:** Tone quality and honest criticism assessment requires subjective reading

### 3. 50 Key Stats Scannability
**Test:** Scan the 50 stats page on desktop and mobile
**Expected:** Stats organized by category headers, each stat links to its detail page, visually scannable
**Why human:** Information hierarchy and scan pattern need human UX evaluation

### Gaps Summary

No gaps found. All 25 data-reference pages (16 tool + 9 benchmark) exist with substantive content (1,440-1,948 words), proper JSON-LD schema (BreadcrumbList + FAQPage), source citations, and extensive cross-linking to salary/career sections. Navigation has Tools dropdown and Benchmarks entry. Build produces 111 pages with zero validation warnings.

One minor note: "robustness" appears in the AI coding tools page. It is used in a technical context (error handling) rather than as AI buzzword filler, so it does not constitute a content quality violation.

---

_Verified: 2026-03-13T23:15:00Z_
_Verifier: Claude (gsd-verifier)_
