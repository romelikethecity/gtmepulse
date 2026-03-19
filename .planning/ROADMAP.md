# Roadmap: GTME Pulse

## Milestones

- ✅ **v1.0 Wave 1: Foundation + Salary Engine** - Phases 1-3 (shipped)
- ✅ **v2.0 State of GTME Content Wave** - Phases 4-7 ([archived](milestones/v2.0-ROADMAP.md))
- ✅ **v3.0 Tool Reviews, Glossary, and Infrastructure** - Phases 8-12 ([archived](milestones/v3.0-ROADMAP.md))
- [ ] **v4.0 Content Expansion and Go-Live Infrastructure** - Phases 13-17

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

<details>
<summary>✅ v3.0 Tool Reviews, Glossary, and Infrastructure (Phases 8-12) — <a href="milestones/v3.0-ROADMAP.md">archived</a></summary>

130 pages added (133 to 263). 10 plans, 42 commits. 30 tool reviews, 8 category indexes, 20 comparisons, 10 alternatives, 10 roundups, 50 glossary terms, job board, newsletter infrastructure, zero-warning build. All 89 requirements complete.

</details>

### v4.0 Content Expansion and Go-Live Infrastructure

- [ ] **Phase 13: Analytics and Newsletter Go-Live** - GA4 tracking, Search Console, newsletter infrastructure deployed and sending
- [x] **Phase 14: Insight Articles Batch 1** - First 10 data-driven articles (market analysis, tool reports, playbooks) (completed 2026-03-18)
- [x] **Phase 15: Insight Articles Batch 2** - Second 10 articles (hiring guides, rate guides, ROI analysis, pulse reports) (completed 2026-03-19)
- [x] **Phase 16: OG Image Generation** - Playwright-based OG image pipeline for all 280+ pages (completed 2026-03-19)
- [ ] **Phase 17: v4.0 Quality Sweep** - All new pages validated, zero-warning build

## Phase Details

### Phase 13: Analytics and Newsletter Go-Live
**Goal**: Site has GA4 tracking across all pages, Google Search Console is verified, and the newsletter pipeline is live (subscribers can sign up, Monday emails send automatically)
**Depends on**: Phase 12
**Requirements**: ANLYT-01, ANLYT-02, ANLYT-03, NLIVE-01, NLIVE-02, NLIVE-03, NLIVE-04, NLIVE-05, NLIVE-06
**Success Criteria** (what must be TRUE):
  1. Every page on gtmepulse.com includes the GA4 tracking snippet and pageviews appear in the GA4 dashboard
  2. Google Search Console shows gtmepulse.com as a verified property with sitemap submitted
  3. Newsletter signup form on the site creates a contact in the Resend GTME Pulse audience
  4. A test email sends successfully via the Monday cron pipeline and arrives in inbox
  5. GA4 fires a custom event when a visitor submits the newsletter signup form
**Plans**: 2 plans

Plans:
- [ ] 13-01-PLAN.md — GA4 tracking, Search Console verification, signup event tracking
- [ ] 13-02-PLAN.md — Newsletter worker deploy, Resend setup, server cron, e2e test

### Phase 14: Insight Articles Batch 1
**Goal**: 10 published insight articles covering job market analysis, salary trends, tool adoption, the State of GTME 2026 report, and hands-on playbooks for Clay, outbound automation, LinkedIn outreach, email deliverability, and API integration
**Depends on**: Phase 13 (analytics must be live to track article traffic)
**Requirements**: ART-01, ART-02, ART-03, ART-04, ART-05, ART-06, ART-07, ART-08, ART-09, ART-10
**Success Criteria** (what must be TRUE):
  1. 10 article pages are accessible at /insights/[slug] with proper nav integration and breadcrumbs
  2. Each article has Article JSON-LD schema with author Person markup for Rome Thorndike
  3. Each article meets the 1,500-2,500 word target with 3+ internal links and 2+ outbound citations
  4. The insights index page lists all 10 articles with excerpts and links
**Plans**: 4 plans

Plans:
- [x] 14-01-PLAN.md — Infrastructure (Article schema, insights index, validator, nav) + data articles ART-01 through ART-04
- [x] 14-02-PLAN.md — Clay ecosystem (ART-05), outbound stack (ART-06), Clay playbook (ART-07)
- [x] 14-03-PLAN.md — LinkedIn outreach (ART-08), email deliverability (ART-09), API integration (ART-10)
- [x] 14-04-PLAN.md — Gap closure: Add missing outbound citations to 5 articles (ART-02, ART-04, ART-05, ART-07, ART-10)

### Phase 15: Insight Articles Batch 2
**Goal**: 10 more published insight articles covering data enrichment strategy, hiring guides, freelance rates, ROI analysis, intent data, CRM hygiene, pulse report templates, tech stack audits, revenue attribution, and remote market analysis
**Depends on**: Phase 14 (builds on insights index and article template established in Batch 1)
**Requirements**: ART-11, ART-12, ART-13, ART-14, ART-15, ART-16, ART-17, ART-18, ART-19, ART-20
**Success Criteria** (what must be TRUE):
  1. 20 total article pages live at /insights/[slug] (10 from Phase 14 + 10 new)
  2. Each new article has Article JSON-LD schema, meets word count targets, and has proper internal/external links
  3. The insights index page lists all 20 articles organized by category
  4. The monthly pulse report template page (ART-17) pulls data from existing JSON data files
**Plans**: 3 plans

Plans:
- [ ] 15-01-PLAN.md — Registry setup + enrichment waterfall (ART-11), hiring guide (ART-12), freelance rates (ART-13), GTME vs SDR ROI (ART-14)
- [ ] 15-02-PLAN.md — Intent data guide (ART-15), CRM hygiene (ART-16), pulse report template with live data (ART-17)
- [ ] 15-03-PLAN.md — Tech stack audit (ART-18), revenue attribution (ART-19), remote market report (ART-20)

### Phase 16: OG Image Generation
**Goal**: Every page on the site has a unique, auto-generated OG image so that social shares and link previews display branded visuals instead of generic defaults
**Depends on**: Phase 15 (all content pages must exist before generating images for them)
**Requirements**: OG-01, OG-02, OG-03, OG-04
**Success Criteria** (what must be TRUE):
  1. Running `python3 scripts/build.py` generates OG images for all 280+ pages as part of the build pipeline
  2. Every page's HTML includes an `og:image` meta tag pointing to its generated PNG
  3. Pasting any gtmepulse.com URL into Twitter/LinkedIn/Slack shows the branded OG image in the preview card
**Plans**: 1 plan

Plans:
- [ ] 16-01-PLAN.md — OG templates, Playwright generator script, build pipeline integration, meta tag injection

### Phase 17: v4.0 Quality Sweep
**Goal**: All v4.0 additions pass the existing validation suite and the full site builds with zero warnings
**Depends on**: Phase 16
**Requirements**: QUAL4-01, QUAL4-02
**Success Criteria** (what must be TRUE):
  1. All 20 insight articles pass validation checks (title length, word count, internal links, schema markup)
  2. `python3 scripts/build.py` completes with zero warnings across all ~283+ pages
  3. No broken internal links across the entire site
**Plans**: 1 plan

Plans:
- [ ] 17-01-PLAN.md — Add QUAL4 validation checks, fix 8 word count warnings, zero-warning build

## Progress

| Milestone | Phases | Plans | Status | Shipped |
|-----------|--------|-------|--------|---------|
| v1.0 Foundation + Salary | 1-3 | 8 | Complete | 2026-03-10 |
| v2.0 Content Wave | 4-7 | 15 | 3/3 | Complete    | 2026-03-19 | v3.0 Tool Reviews + Infra | 8-12 | 10 | Complete | 2026-03-16 |
| v4.0 Content + Go-Live | 13-17 | 5+ | In progress | - |

---
*Roadmap created: 2026-03-10 (Wave 1)*
*v2.0 archived: 2026-03-14*
*v3.0 archived: 2026-03-16*
*v4.0 phases added: 2026-03-16*
