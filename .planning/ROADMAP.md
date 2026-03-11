# Roadmap: GTME Pulse (Wave 1)

## Overview

Wave 1 delivers the GTME Pulse site foundation and its anchor differentiator: salary data for a role no competitor covers. Three phases build bottom-up: a working build system and HTML shell, then core pages with newsletter infrastructure to prove the pipeline end-to-end, then 45 salary pages with the email-gated calculator. When Phase 3 completes, gtmepulse.com is a live site with ~51 pages of deep salary content and a working email capture funnel.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Build System and HTML Shell** - Python build pipeline, CSS architecture, responsive HTML shell, schema helpers, and content standards enforcement
- [ ] **Phase 2: Core Pages and Newsletter Infrastructure** - Homepage, about, newsletter, legal pages, 404, Cloudflare Worker signup, Resend integration
- [ ] **Phase 3: Salary Data Engine** - Methodology page, salary index, 34 salary breakdown/comparison pages, salary calculator with email gate, content quality enforcement

## Phase Details

### Phase 1: Build System and HTML Shell
**Goal**: A working build pipeline that generates valid, responsive HTML pages with correct schema markup, CSS architecture, and sitemap from a single `python3 scripts/build.py` command
**Depends on**: Nothing (first phase)
**Requirements**: BUILD-01, BUILD-02, BUILD-03, BUILD-04, BUILD-05, BUILD-06, BUILD-07, BUILD-08, HTML-01, HTML-02, HTML-03, HTML-04, HTML-05, SEO-01, SEO-02, SEO-03, SEO-04, CONTENT-01, CONTENT-02, CONTENT-03, CONTENT-04, CONTENT-05, CONTENT-06
**Success Criteria** (what must be TRUE):
  1. Running `python3 scripts/build.py` produces an output/ directory with valid HTML files, copied assets, sitemap.xml, robots.txt, and CNAME, and prints a page count summary
  2. Opening any generated page in a browser shows a responsive layout with working nav, footer, breadcrumbs, and correct fonts at 375px, 768px, and 1024px widths
  3. Every generated page has a unique title (50-60 chars), unique meta description (150-158 chars), canonical URL, OG tags, and appropriate JSON-LD schema (Organization+WebSite on homepage, BreadcrumbList on inner pages)
  4. The CSS cascade works without conflicts: tokens.css variables load, components.css provides reusable classes, styles.css adds page-scoped styles via body class, and cache-busting query params are present
**Plans**: TBD

Plans:
- [ ] 01-01: TBD
- [ ] 01-02: TBD

### Phase 2: Core Pages and Newsletter Infrastructure
**Goal**: Six core pages live and functional, with a working newsletter signup flow from form submission through Cloudflare Worker to Resend Audiences
**Depends on**: Phase 1
**Requirements**: CORE-01, CORE-02, CORE-03, CORE-04, CORE-05, CORE-06, NEWS-01, NEWS-02, NEWS-03, NEWS-04, NEWS-05, NEWS-06
**Success Criteria** (what must be TRUE):
  1. Homepage displays hero with key stats (3,000+ roles, $132K-$250K, 205% growth), section previews linking to salary/tools/career sections, and a newsletter signup CTA
  2. About page shows Rome Thorndike bio and site mission; Privacy, Terms, and 404 pages render with correct content and navigation
  3. Entering an email on the /newsletter page, homepage hero, or footer mini-form successfully adds the subscriber to the Resend Audience (confirmed via Resend dashboard) with visible success/error feedback
  4. The Cloudflare Worker (subscribe.js) accepts POSTs from gtmepulse.com and localhost:8090, rejects other origins, validates email format, and returns appropriate status codes
**Plans**: TBD

Plans:
- [ ] 02-01: TBD
- [ ] 02-02: TBD

### Phase 3: Salary Data Engine
**Goal**: 36 salary pages deliver deep, differentiated content with the methodology page establishing data credibility, the calculator gating full results behind email signup, and every page meeting quality thresholds
**Depends on**: Phase 2
**Requirements**: SAL-01, SAL-02, SAL-03, SAL-04, SAL-05, SAL-06, SAL-07, QUAL-01, QUAL-02, QUAL-03, QUAL-04, QUAL-05, QUAL-06
**Success Criteria** (what must be TRUE):
  1. The methodology page explains data sources, collection methods, sample sizes, limitations, and update frequency, and is linked from every salary page
  2. Salary index page shows aggregate stats and links to all 34 breakdown/comparison sub-pages; each sub-page has a stats grid, range visualization, market context, comp drivers, and related links section
  3. Every salary page has 1,200-2,000 words of content with 30%+ unique market context compared to sibling pages of the same type, 3+ internal links beyond nav/footer, and no duplicate titles or meta descriptions across the site
  4. Salary comparison pages each have a visible FAQ section with 3-4 unique Q&A pairs and matching FAQPage JSON-LD schema
  5. The salary calculator page shows a free preview and gates full percentile results behind an email signup form that adds the subscriber to Resend before revealing results
**Plans**: TBD

Plans:
- [ ] 03-01: TBD
- [ ] 03-02: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Build System and HTML Shell | 0/0 | Not started | - |
| 2. Core Pages and Newsletter Infrastructure | 0/0 | Not started | - |
| 3. Salary Data Engine | 0/0 | Not started | - |

---
*Roadmap created: 2026-03-10*
*Last updated: 2026-03-10*
