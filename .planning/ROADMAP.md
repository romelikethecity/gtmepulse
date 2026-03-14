# Roadmap: GTME Pulse

## Milestones

- ✅ **v1.0 Wave 1: Foundation + Salary Engine** - Phases 1-3 (in progress)
- 📋 **v2.0 Wave 2: State of GTME Content Wave** - Phases 4-7 (planned)

## Phases

<details>
<summary>✅ v1.0 Wave 1: Foundation + Salary Engine (Phases 1-3)</summary>

### Phase 1: Build System and HTML Shell
**Goal**: A working build pipeline that generates valid, responsive HTML pages with correct schema markup, CSS architecture, and sitemap from a single `python3 scripts/build.py` command
**Depends on**: Nothing (first phase)
**Requirements**: BUILD-01 through BUILD-08, HTML-01 through HTML-05, SEO-01 through SEO-04, CONTENT-01 through CONTENT-06
**Plans**: 1/2 plans executed

Plans:
- [ ] 01-01-PLAN.md — Config layer, HTML shell, CSS architecture
- [ ] 01-02-PLAN.md — Build pipeline, placeholder pages, sitemap/robots/CNAME

### Phase 2: Core Pages and Newsletter Infrastructure
**Goal**: Six core pages live and functional, with a working newsletter signup flow
**Depends on**: Phase 1
**Requirements**: CORE-01 through CORE-06, NEWS-01 through NEWS-06
**Plans**: TBD

### Phase 3: Salary Data Engine
**Goal**: 36 salary pages with deep content, methodology page, and email-gated calculator
**Depends on**: Phase 2
**Requirements**: SAL-01 through SAL-07, QUAL-01 through QUAL-06
**Plans**: TBD

</details>

### v2.0 State of GTME Content Wave (Phases 4-7)

**Milestone Goal:** Build ~85 new data-backed content pages using the State of GTME Report 2026 (n=228), replacing hardcoded salary estimates with real survey data and creating the definitive SEO resource for every GTM Engineering query.

**Phase Numbering:**
- Integer phases (4, 5, 6, 7): Planned milestone work
- Decimal phases (4.1, 5.1): Urgent insertions (marked with INSERTED)

- [x] **Phase 4: Salary Data Overhaul** - Update existing salary data layer with real survey numbers, then build 12 new salary pages (completed 2026-03-13)
- [x] **Phase 5: Career, Agency, and Job Market** - 28 pages covering career paths, agency business, and job market analysis (completed 2026-03-13)
- [x] **Phase 6: Tools and Benchmarks** - 25 pages covering tool adoption data and industry benchmark statistics (completed 2026-03-13)
- [x] **Phase 7: Comparisons, Blog Articles, and Quality Sweep** - 6 comparison pages, 14 blog articles, and site-wide quality/SEO validation (completed 2026-03-14)

## Phase Details

### Phase 4: Salary Data Overhaul
**Goal**: Existing salary pages show real State of GTME Report data instead of estimates, and 12 new salary pages cover compensation angles no competitor touches (coding premium, equity, bonuses, agency fees, age, company size)
**Depends on**: Phase 3 (Wave 1 salary pages must exist)
**Requirements**: SALUP-01, SALUP-02, SALUP-03, SALN-01, SALN-02, SALN-03, SALN-04, SALN-05, SALN-06, SALN-07, SALN-08, SALN-09, SALN-10, SALN-11, SALN-12
**Success Criteria** (what must be TRUE):
  1. Every existing salary page displays $135K US median, $75K non-US median, and $60K-$250K+ range from the State of GTME Report instead of hardcoded estimates
  2. Every salary page (existing and new) cites "Source: State of GTM Engineering Report 2026 (n=228)" with visible attribution
  3. The 12 new salary pages each render with full content (1,200-2,000 words), stats grids, range visualizations, and FAQ sections where applicable
  4. Running `python3 scripts/build.py` generates all updated and new salary pages without errors, and no two pages share the same title or meta description
**Plans**: 3 plans

Plans:
- [ ] 04-01-PLAN.md — Data layer update with real report numbers + source citations on existing pages
- [ ] 04-02-PLAN.md — New salary pages: coding premium, company size, funding stage, experience, age, bonus
- [ ] 04-03-PLAN.md — New salary pages: equity, US vs global, posted vs actual, agency fees, agency fees by region, seed vs enterprise + nav update

### Phase 5: Career, Agency, and Job Market
**Goal**: Visitors can explore 28 pages of career intelligence, agency business data, and job market analysis, each backed by real survey and job posting data
**Depends on**: Phase 4 (salary data layer must be updated; career/agency pages reference salary figures)
**Requirements**: CAREER-01 through CAREER-12, AGENCY-01 through AGENCY-08, JOBMKT-01 through JOBMKT-08
**Success Criteria** (what must be TRUE):
  1. A visitor searching "how to become a GTM engineer" finds a page with self-taught data (121/228), career path breakdown, and actionable steps
  2. Agency-focused pages show real pricing data ($5K-$8K/mo median, regional breakdowns) and business metrics (client retention, pricing models) that a freelancer can use to benchmark their practice
  3. Job market pages display the 5,205% growth narrative with monthly trends, country breakdowns, and salary band data from 3,342 postings
  4. Every page in this phase has 1,200-2,000 words, BreadcrumbList schema, 3+ internal links, and visible source citations
**Plans**: 4 plans

Plans:
- [ ] 05-01-PLAN.md — Career index + first 6 career pages (how to become, operator vs engineer, real career, job market, how got jobs, work-life balance)
- [ ] 05-02-PLAN.md — Remaining 6 career pages (demographics, RevOps convergence, coding needed, reporting, impact, skills gap)
- [ ] 05-03-PLAN.md — 8 agency/freelance pages (pricing, start agency, revenue, retention, client count, pricing models, regional fees, deliverability)
- [ ] 05-04-PLAN.md — 8 job market pages (growth, by country, posted vs actual, top skills, monthly trends, salary bands, India, Spain) + nav update

### Phase 6: Tools and Benchmarks
**Goal**: Visitors can explore the full GTM Engineer tech stack (adoption rates, frustrations, spend) and industry benchmarks (demographics, bottlenecks, predictions) through 25 data-reference pages
**Depends on**: Phase 4 (tool pages reference salary data for context)
**Requirements**: TOOL-01, TOOL-02, TOOL-03, TOOL-04, TOOL-05, TOOL-06, TOOL-07, TOOL-08, TOOL-09, TOOL-10, TOOL-11, TOOL-12, TOOL-13, TOOL-14, TOOL-15, TOOL-16, BENCH-01, BENCH-02, BENCH-03, BENCH-04, BENCH-05, BENCH-06, BENCH-07, BENCH-08, BENCH-09
**Success Criteria** (what must be TRUE):
  1. The tech stack benchmark page shows adoption rates for every major tool category (Clay 84%, CRM 92%, AI coding 71%, n8n 54%) with agency vs in-house splits
  2. Individual tool pages (Clay, Python, SQL, Zapier vs n8n, HubSpot vs Salesforce) provide adoption data, salary impact, and honest criticism grounded in survey responses
  3. Benchmark pages cover the full "state of" picture: 50 key stats, demographics, bottlenecks, headcount trends, and future predictions
  4. Every page meets content depth (1,200-2,000 words) and has working internal links to related salary, career, and tool pages
**Plans**: 4 plans

Plans:
- [ ] 06-01-PLAN.md — Tools index + tech stack benchmark + Clay + CRM + AI coding + n8n pages (TOOL-01 through TOOL-05)
- [ ] 06-02-PLAN.md — Tool frustrations, most exciting, Unify, annual spend, ZoomInfo vs Apollo, wishlist pages (TOOL-06 through TOOL-11)
- [ ] 06-03-PLAN.md — Python, SQL, JavaScript, Zapier vs n8n, HubSpot vs Salesforce pages + nav update (TOOL-12 through TOOL-16)
- [ ] 06-04-PLAN.md — Benchmarks index + 9 benchmark pages (BENCH-01 through BENCH-09) + nav update

### Phase 7: Comparisons, Blog Articles, and Quality Sweep
**Goal**: Six comparison pages and 14 blog articles add the editorial opinion layer, and a final quality sweep confirms every v2.0 page meets SEO and content standards
**Depends on**: Phases 4, 5, 6 (comparisons and blogs reference data from all prior phases)
**Requirements**: COMP-01, COMP-02, COMP-03, COMP-04, COMP-05, COMP-06, BLOG-01, BLOG-02, BLOG-03, BLOG-04, BLOG-05, BLOG-06, BLOG-07, BLOG-08, BLOG-09, BLOG-10, BLOG-11, BLOG-12, BLOG-13, BLOG-14, QUAL2-01, QUAL2-02, QUAL2-03, QUAL2-04, QUAL2-05, QUAL2-06, QUAL2-07, QUAL2-08, QUAL2-09
**Success Criteria** (what must be TRUE):
  1. Comparison pages present data-backed analysis (engineer vs operator $45K gap, in-house vs agency splits, regional salary differences) with visible FAQ sections and FAQPage schema
  2. Blog articles each have 1,500-2,500 words with a specific thesis backed by report data, not generic commentary
  3. Running a full build produces zero duplicate titles or meta descriptions across the entire site (all waves combined)
  4. Every v2.0 page has: unique title (50-60 chars), meta description (150-158 chars), canonical URL, OG/Twitter tags, BreadcrumbList schema, 3+ internal links, visible source citation, and passes writing standards (no em-dashes, no false reframes, no banned words)
  5. Navigation and footer links are updated to surface new content sections (career, tools, benchmarks, blog)
**Plans**: 4 plans

Plans:
- [ ] 07-01-PLAN.md — Comparison index + 6 comparison pages with FAQ sections and FAQPage schema (COMP-01 through COMP-06)
- [ ] 07-02-PLAN.md — Blog index + blog articles 1-7 (BLOG-01 through BLOG-07)
- [ ] 07-03-PLAN.md — Blog articles 8-14 + Blog nav entry (BLOG-08 through BLOG-14)
- [ ] 07-04-PLAN.md — Site-wide quality and SEO validation sweep (QUAL2-01 through QUAL2-09)

## Progress

**Execution Order:**
Phases execute in numeric order: 4 → 5 → 6 → 7

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Build System and HTML Shell | v1.0 | 1/2 | In progress | - |
| 2. Core Pages and Newsletter | v1.0 | 0/2 | Not started | - |
| 3. Salary Data Engine | v1.0 | 0/2 | Not started | - |
| 4. Salary Data Overhaul | v2.0 | 3/3 | Complete | 2026-03-13 |
| 5. Career, Agency, and Job Market | v2.0 | 4/4 | Complete | 2026-03-13 |
| 6. Tools and Benchmarks | v2.0 | 4/4 | Complete | 2026-03-13 |
| 7. Comparisons, Blog, and Quality | 4/4 | Complete   | 2026-03-14 | - |

---
*Roadmap created: 2026-03-10 (Wave 1)*
*v2.0 phases added: 2026-03-13*
*Last updated: 2026-03-13*
