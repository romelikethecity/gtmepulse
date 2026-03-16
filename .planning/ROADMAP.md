# Roadmap: GTME Pulse

## Milestones

- ✅ **v1.0 Wave 1: Foundation + Salary Engine** - Phases 1-3 (shipped)
- ✅ **v2.0 State of GTME Content Wave** - Phases 4-7 ([archived](milestones/v2.0-ROADMAP.md))
- 🚧 **v3.0 Tool Reviews, Glossary, and Infrastructure** - Phases 8-12 (in progress)

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
**Plans**: 3 plans

### Phase 3: Salary Data Engine
**Goal**: 36 salary pages with deep content, methodology page, and email-gated calculator
**Depends on**: Phase 2
**Requirements**: SAL-01 through SAL-07, QUAL-01 through QUAL-06
**Plans**: 3 plans

</details>

<details>
<summary>✅ v2.0 State of GTME Content Wave (Phases 4-7) — <a href="milestones/v2.0-ROADMAP.md">archived</a></summary>

82 pages added (51 to 133). 15 plans, 50 commits. Salary data overhaul, 28 career/agency/job-market pages, 25 tools/benchmarks pages, 6 comparisons, 14 blog articles, site-wide quality sweep. All 88 requirements complete.

</details>

### v3.0 Tool Reviews, Glossary, and Infrastructure

**Milestone Goal:** Add the full tool review vertical (30 reviews, 8 category indexes, 20 comparisons, 10 alternatives, 10 roundups), 50 glossary terms, a job board wired to scraper data, and newsletter automation. Target ~130+ new pages plus infrastructure.

- [x] **Phase 8: Tool Reviews** - 30 individual tool review pages with SoftwareApplication schema and honest criticism (completed 2026-03-14)
- [x] **Phase 9: Tool Categories and Comparisons** - 8 category index pages and 20 head-to-head comparison pages (completed 2026-03-14)
- [x] **Phase 10: Alternatives and Roundups** - 10 alternatives pages and 10 best-for roundup pages (completed 2026-03-14)
- [x] **Phase 11: Glossary, Job Board, and Newsletter** - 50 glossary terms, job board with scraper pipeline, newsletter automation (completed 2026-03-14)
- [x] **Phase 12: Quality Sweep** - Site-wide validation, schema audit, zero-warning build (completed 2026-03-16)

## Phase Details

### Phase 8: Tool Reviews
**Goal**: Users can read in-depth, vendor-neutral reviews of 30 GTM Engineering tools, each with honest criticism, pricing context, and structured schema markup
**Depends on**: Phase 7 (v2.0 complete)
**Requirements**: TREV-01, TREV-02, TREV-03, TREV-04, TREV-05, TREV-06, TREV-07, TREV-08, TREV-09, TREV-10, TREV-11, TREV-12, TREV-13, TREV-14, TREV-15, TREV-16, TREV-17, TREV-18, TREV-19, TREV-20, TREV-21, TREV-22, TREV-23, TREV-24, TREV-25, TREV-26, TREV-27, TREV-28, TREV-29, TREV-30
**Success Criteria** (what must be TRUE):
  1. User can navigate to /tools/[tool-slug]/ and read a 1,500-2,500 word review for each of 30 tools
  2. Every review includes honest criticism, pricing section, GTM Engineer-specific use cases, and a verdict
  3. Every review page has SoftwareApplication JSON-LD schema in the page source
  4. Reviews cross-link to related tool reviews and existing tool/benchmark pages via related links section
  5. Tools nav and index page link to all 30 review pages
**Plans**: 2 plans

Plans:
- [ ] 08-01-PLAN.md — Review generator infrastructure + 21 reviews (Data Enrichment, Outbound, CRM)
- [ ] 08-02-PLAN.md — Remaining 9 reviews (Workflow Automation, Intent, Analytics, LinkedIn)

### Phase 9: Tool Categories and Comparisons
**Goal**: Users can browse tools by category and read detailed head-to-head comparisons between competing tools
**Depends on**: Phase 8
**Requirements**: TCAT-01, TCAT-02, TCAT-03, TCAT-04, TCAT-05, TCAT-06, TCAT-07, TCAT-08, TCMP-01, TCMP-02, TCMP-03, TCMP-04, TCMP-05, TCMP-06, TCMP-07, TCMP-08, TCMP-09, TCMP-10, TCMP-11, TCMP-12, TCMP-13, TCMP-14, TCMP-15, TCMP-16, TCMP-17, TCMP-18, TCMP-19, TCMP-20
**Success Criteria** (what must be TRUE):
  1. User can visit 8 category index pages, each listing tools in that category with summary cards and links to individual reviews
  2. User can read 20 comparison pages (3,000-5,000 words each) with feature tables, pricing comparisons, and a clear winner recommendation
  3. Every comparison page has FAQPage schema with 3+ Q&A pairs matching visible FAQ content
  4. Category and comparison pages cross-link to relevant reviews, alternatives, and existing site content
**Plans**: 2 plans

Plans:
- [ ] 09-01-PLAN.md — 8 category index pages + first 10 comparisons
- [ ] 09-02-PLAN.md — Remaining 10 comparisons

### Phase 10: Alternatives and Roundups
**Goal**: Users searching for "[Tool] alternatives" or "best [category] tools" find comprehensive, opinionated pages with clear recommendations
**Depends on**: Phase 9
**Requirements**: TALT-01, TALT-02, TALT-03, TALT-04, TALT-05, TALT-06, TALT-07, TALT-08, TALT-09, TALT-10, TBST-01, TBST-02, TBST-03, TBST-04, TBST-05, TBST-06, TBST-07, TBST-08, TBST-09, TBST-10
**Success Criteria** (what must be TRUE):
  1. User can find 10 alternatives pages (e.g., /tools/clay-alternatives/) listing 5-8 alternatives each with pros, cons, and pricing
  2. User can find 10 best-for roundup pages (e.g., /tools/best-gtm-tools-startups/) with ranked recommendations and use-case guidance
  3. Alternatives and roundup pages link to individual tool reviews and comparison pages where relevant
  4. Every alternatives and roundup page has FAQ section with 3+ Q&A pairs
**Plans**: 2 plans

Plans:
- [ ] 10-01-PLAN.md — 10 alternatives pages with content modules and generator infrastructure
- [ ] 10-02-PLAN.md — 10 best-for roundup pages with content modules and generator infrastructure

### Phase 11: Glossary, Job Board, and Newsletter
**Goal**: Users can look up GTM Engineering terms, browse live job postings, and subscribe to automated weekly email updates
**Depends on**: Phase 8 (reviews exist for cross-linking)
**Requirements**: GLOS-01, GLOS-02, JOBS-01, JOBS-02, NEWS-01, NEWS-02, NEWS-03, NEWS-04
**Success Criteria** (what must be TRUE):
  1. User can browse /glossary/ index with alphabetical listing and category grouping, and click through to 50 individual term pages (300-600 words each)
  2. User can visit /jobs/ and see job cards with title, company, location, salary range, remote badge, and filter by seniority/location/remote
  3. Job board reads from scraper JSON exports in data/ directory and displays aggregate stats banner
  4. Newsletter signup Cloudflare Worker accepts email submissions and adds contacts to Resend Audiences
  5. Weekly email is auto-generated from scraper data and sent every Monday via cron
**Plans**: 3 plans

Plans:
- [ ] 11-01-PLAN.md — Glossary index + 50 term pages
- [ ] 11-02-PLAN.md — Job board page + scraper data pipeline
- [ ] 11-03-PLAN.md — Newsletter worker + weekly email generator + cron

### Phase 12: Quality Sweep
**Goal**: Every new page passes site-wide validation with zero warnings, all schema markup is correct, and the full build completes cleanly
**Depends on**: Phases 8-11
**Requirements**: QUAL3-01, QUAL3-02, QUAL3-03
**Success Criteria** (what must be TRUE):
  1. Every tool review page has valid SoftwareApplication JSON-LD schema verified by build validation
  2. Every comparison page has FAQPage schema with 3+ Q&A pairs matching visible content
  3. `python3 scripts/build.py` completes with zero validation warnings across all ~260+ pages
**Plans**: 1 plan

Plans:
- [ ] 12-01-PLAN.md — Schema validation enhancement + fix all 97 warnings + zero-warning build

## Progress

**Execution Order:**
Phases execute in numeric order: 8 → 9 → 10 → 11 → 12

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Build System and HTML Shell | v1.0 | 1/2 | In progress | - |
| 2. Core Pages and Newsletter | v1.0 | 0/2 | Not started | - |
| 3. Salary Data Engine | v1.0 | 0/2 | Not started | - |
| 4-7. State of GTME Content Wave | v2.0 | 15/15 | Archived | 2026-03-14 |
| 8. Tool Reviews | 2/2 | Complete   | 2026-03-14 | - |
| 9. Tool Categories and Comparisons | 2/2 | Complete   | 2026-03-14 | - |
| 10. Alternatives and Roundups | 2/2 | Complete    | 2026-03-14 | - |
| 11. Glossary, Job Board, and Newsletter | 3/3 | Complete   | 2026-03-14 | - |
| 12. Quality Sweep | 1/1 | Complete   | 2026-03-16 | - |

---
*Roadmap created: 2026-03-10 (Wave 1)*
*v2.0 archived: 2026-03-14*
*v3.0 roadmap: 2026-03-14*
