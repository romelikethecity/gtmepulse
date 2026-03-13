---
phase: 05-career-agency-and-job-market
verified: 2026-03-13T19:30:00Z
status: passed
score: 4/4 success criteria verified
---

# Phase 5: Career, Agency, and Job Market Verification Report

**Phase Goal:** Visitors can explore 28 pages of career intelligence, agency business data, and job market analysis, each backed by real survey and job posting data
**Verified:** 2026-03-13T19:30:00Z
**Status:** passed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths (from Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Visitor searching "how to become a GTM engineer" finds page with self-taught data (121/228), career path breakdown, actionable steps | VERIFIED | output/careers/how-to-become-gtm-engineer/index.html contains "121" (3 occurrences), "self-taught" (6 occurrences), "228" (8 occurrences), 1,943 words |
| 2 | Agency pages show real pricing ($5K-$8K/mo median, regional breakdowns) and business metrics (client retention, pricing models) a freelancer can benchmark against | VERIFIED | agency-pricing has $5K (15x), $8K (10x); client-retention has 44% (8x); deliverability-practices has 89.7% (8x); 8 agency pages with pricing-models, client-count, regional fees |
| 3 | Job market pages display 5,205% growth with monthly trends, country breakdowns, salary band data from 3,342 postings | VERIFIED | job-growth has 5,205% (12x), 3,342 (10x); monthly-hiring-trends has 624 (8x); jobs-by-country has 25.7% (7x); 8 job market pages cover all angles |
| 4 | Every page has 1,200-2,000 words, BreadcrumbList schema, 3+ internal links, visible source citations | VERIFIED | All 28 pages: word counts 1,423-1,943 (all within 1,200-2,000), BreadcrumbList present on all 28, internal links 44-49 per page, source citation on all 28, FAQPage schema on all 28 |

**Score:** 4/4 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `output/careers/index.html` | Career landing page with 28 cards | VERIFIED | 18,524 bytes, 3 subsections (Career Guides 12, Agency & Freelance 8, Job Market 8), 28 unique page links |
| `output/careers/how-to-become-gtm-engineer/index.html` | CAREER-01 | VERIFIED | 1,943 words, self-taught data, BreadcrumbList + FAQPage |
| `output/careers/operator-vs-engineer/index.html` | CAREER-02 | VERIFIED | 1,793 words, $45K gap data |
| `output/careers/is-gtm-engineering-real-career/index.html` | CAREER-03 | VERIFIED | 1,616 words, 5,205% growth |
| `output/careers/job-market-analysis/index.html` | CAREER-04 | VERIFIED | 1,712 words, posting trends |
| `output/careers/how-gtm-engineers-got-jobs/index.html` | CAREER-05 | VERIFIED | 1,838 words, entry paths |
| `output/careers/work-life-balance/index.html` | CAREER-06 | VERIFIED | 1,745 words, 60%/23% data |
| `output/careers/demographics/index.html` | CAREER-07 | VERIFIED | 1,645 words, median age 25 |
| `output/careers/gtm-engineer-vs-revops/index.html` | CAREER-08 | VERIFIED | 1,551 words, 9.6% convergence |
| `output/careers/do-you-need-to-code/index.html` | CAREER-09 | VERIFIED | 1,862 words, bimodal distribution |
| `output/careers/reporting-structure/index.html` | CAREER-10 | VERIFIED | 1,515 words, reporting data |
| `output/careers/impact-measurement/index.html` | CAREER-11 | VERIFIED | 1,650 words, pipeline KPIs |
| `output/careers/skills-gap/index.html` | CAREER-12 | VERIFIED | 1,642 words, Clay 84% |
| `output/careers/agency-pricing/index.html` | AGENCY-01 | VERIFIED | 1,595 words, $5K-$8K median |
| `output/careers/start-gtm-engineering-agency/index.html` | AGENCY-02 | VERIFIED | 1,723 words, 30% agency data |
| `output/careers/agency-vs-freelance/index.html` | AGENCY-03 | VERIFIED | 1,496 words, revenue comparison |
| `output/careers/client-retention/index.html` | AGENCY-04 | VERIFIED | 1,547 words, 44% retention |
| `output/careers/client-count/index.html` | AGENCY-05 | VERIFIED | 1,508 words, client analysis |
| `output/careers/pricing-models/index.html` | AGENCY-06 | VERIFIED | 1,628 words, model breakdown |
| `output/careers/agency-fees-by-region-guide/index.html` | AGENCY-07 | VERIFIED | 1,667 words, regional fees |
| `output/careers/deliverability-practices/index.html` | AGENCY-08 | VERIFIED | 1,788 words, 89.7% domain rotation |
| `output/careers/job-growth/index.html` | JOBMKT-01 | VERIFIED | 1,588 words, 5,205% surge |
| `output/careers/jobs-by-country/index.html` | JOBMKT-02 | VERIFIED | 1,423 words, US 25.7% |
| `output/careers/posted-vs-actual-salary/index.html` | JOBMKT-03 | VERIFIED | 1,473 words, salary gap |
| `output/careers/top-skills-in-postings/index.html` | JOBMKT-04 | VERIFIED | 1,500 words, skills demand |
| `output/careers/monthly-hiring-trends/index.html` | JOBMKT-05 | VERIFIED | 1,578 words, Dec 624 peak |
| `output/careers/salary-bands-by-location/index.html` | JOBMKT-06 | VERIFIED | 1,472 words, salary bands |
| `output/careers/india-gtm-engineering/index.html` | JOBMKT-07 | VERIFIED | 1,472 words, 17.4% market |
| `output/careers/spain-europe-gtm-engineering/index.html` | JOBMKT-08 | VERIFIED | 1,628 words, 15.3% market |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| scripts/build.py | output/careers/*/index.html | build_career_*, build_agency_*, build_jobmkt_* | WIRED | 13 career, 8 agency, 8 jobmkt generator functions in build.py |
| career pages | /salary/ pages | inline href links | WIRED | All career pages contain href="/salary/" links |
| agency pages | /salary/agency-fees* | inline links | WIRED | Agency pages link to salary agency fee pages |
| career_related_links() | 12 career pages | cross-link helper | WIRED | Function exists, links all 12 career slugs |
| agency_related_links() | 8 agency pages | cross-link helper | WIRED | Function exists, links all 8 agency slugs |
| jobmkt_related_links() | 8 job market pages | cross-link helper | WIRED | Function exists, links all 8 job market slugs |
| nav_config.py | career pages | Careers dropdown | WIRED | Dropdown with 4 children: Career Guides, How to Become, Job Market Growth, Agency Pricing |
| career index | all 28 content pages | card grid links | WIRED | 28 unique href links in index, 3 subsections |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| CAREER-01 | 05-01 | How to become a GTM Engineer guide | SATISFIED | Page exists with 1,943 words, self-taught 121/228 data |
| CAREER-02 | 05-01 | Operator vs engineer bifurcation | SATISFIED | Page exists with $45K gap data |
| CAREER-03 | 05-01 | Is GTM Engineering a real career | SATISFIED | Page exists with 5,205% growth data |
| CAREER-04 | 05-01 | Job market analysis | SATISFIED | Page exists with 63-to-3,342 posting data |
| CAREER-05 | 05-01 | How GTMEs got their jobs | SATISFIED | Page exists with entry path data |
| CAREER-06 | 05-01 | Work-life balance | SATISFIED | Page exists with 60%/23% hours data |
| CAREER-07 | 05-02 | Demographics deep-dive | SATISFIED | Page exists with median age 25, 32 countries |
| CAREER-08 | 05-02 | GTM Engineer vs RevOps convergence | SATISFIED | Page exists with 9.6% convergence data |
| CAREER-09 | 05-02 | Do you need to code | SATISFIED | Page exists with bimodal distribution, $45K premium |
| CAREER-10 | 05-02 | Reporting structure | SATISFIED | Page exists with reporting line data |
| CAREER-11 | 05-02 | Impact measurement | SATISFIED | Page exists with pipeline KPI data |
| CAREER-12 | 05-02 | Skills gap analysis | SATISFIED | Page exists with Clay 84%, CRM 92% |
| AGENCY-01 | 05-03 | Agency pricing guide | SATISFIED | Page exists with $5K-$8K/mo median |
| AGENCY-02 | 05-03 | How to start an agency | SATISFIED | Page exists with 30% agency data |
| AGENCY-03 | 05-03 | Agency vs freelance revenue | SATISFIED | Page exists with revenue comparison |
| AGENCY-04 | 05-03 | Client retention data | SATISFIED | Page exists with 44% at 3-6mo data |
| AGENCY-05 | 05-03 | Client count analysis | SATISFIED | Page exists with 47% under 5 clients |
| AGENCY-06 | 05-03 | Pricing models breakdown | SATISFIED | Page exists with model comparison |
| AGENCY-07 | 05-03 | Agency fees by region guide | SATISFIED | Page exists with regional fee data |
| AGENCY-08 | 05-03 | Deliverability practices | SATISFIED | Page exists with 89.7% domain rotation |
| JOBMKT-01 | 05-04 | Job growth 5,205% | SATISFIED | Page exists with 63-to-3,342 data |
| JOBMKT-02 | 05-04 | Jobs by country | SATISFIED | Page exists with US 25.7%, India 17.4%, Spain 15.3% |
| JOBMKT-03 | 05-04 | Posted vs actual salary | SATISFIED | Page exists with $150K vs $135K gap |
| JOBMKT-04 | 05-04 | Top skills in postings | SATISFIED | Page exists with Clay, HubSpot, Python, SQL |
| JOBMKT-05 | 05-04 | Monthly hiring trends | SATISFIED | Page exists with Dec 624 peak |
| JOBMKT-06 | 05-04 | Salary bands by location | SATISFIED | Page exists with US $128K-$175K band |
| JOBMKT-07 | 05-04 | India market analysis | SATISFIED | Page exists with 17.4% data |
| JOBMKT-08 | 05-04 | Spain/Europe market analysis | SATISFIED | Page exists with 15.3% data |

**28/28 requirements SATISFIED. 0 orphaned.**

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (none) | - | - | - | No TODO, FIXME, PLACEHOLDER, or stub patterns found in build.py or output files |

### Human Verification Required

### 1. Visual Appearance of Career Index

**Test:** Open http://localhost:8090/careers/ and verify the 3-section card grid (Career Guides, Agency & Freelance, Job Market) renders correctly with consistent card sizing
**Expected:** 28 cards organized in 3 labeled sections, consistent with salary index styling
**Why human:** Visual layout, card alignment, responsive behavior cannot be verified programmatically

### 2. Careers Nav Dropdown

**Test:** Click the "Careers" nav item and verify the dropdown shows 4 children links
**Expected:** Dropdown appears with Career Guides, How to Become a GTME, Job Market Growth, Agency Pricing
**Why human:** Dropdown interaction behavior requires browser testing

### 3. Content Quality Spot Check

**Test:** Read through 2-3 pages (how-to-become, agency-pricing, job-growth) and verify writing quality matches the practitioner voice described in CLAUDE.md
**Expected:** Direct, data-backed writing with no AI tells, no banned words, varied sentence length, specific numbers
**Why human:** Writing quality and tone cannot be verified programmatically beyond word counting and banned-word scanning

---

_Verified: 2026-03-13T19:30:00Z_
_Verifier: Claude (gsd-verifier)_
