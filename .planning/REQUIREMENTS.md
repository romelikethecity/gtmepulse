# Requirements: GTME Pulse v2.0 — State of GTME Content Wave

**Defined:** 2026-03-13
**Core Value:** GTM Engineers can find accurate, vendor-neutral salary benchmarks and career intelligence in one place, with data no competitor provides.
**Data Source:** State of GTME Report 2026 (n=228, 32 countries) + Clay Job Data (3,342 postings via Sentrion)

## v1.0 Requirements (Wave 1 — Prior Milestone)

*48 requirements across Build System, HTML Shell, Schema, Core Pages, Salary Pages, Newsletter, Content Standards. See git history for full v1.0 REQUIREMENTS.md.*

## v2.0 Requirements

### Salary Data Update

- [x] **SALUP-01**: Existing salary pages display real survey data ($135K US in-house median, $75K non-US, $60K-$250K+ range) replacing hardcoded estimates
- [x] **SALUP-02**: Every salary page cites "Source: State of GTM Engineering Report 2026 (n=228)" with sample size context
- [x] **SALUP-03**: Salary data dict in build.py is restructured to use real report numbers (by seniority, location, stage, role comparisons)

### New Salary Pages

- [x] **SALN-01**: Salary page showing coding vs no-code compensation gap ($45K premium, bimodal skill distribution)
- [x] **SALN-02**: Salary page breaking down compensation by company size (201-1,000 employees pay most)
- [x] **SALN-03**: Salary page showing compensation by funding stage (Series B & D+ lead at $145K median)
- [x] **SALN-04**: Salary page showing compensation by experience level ($105K median <1yr, scaling up)
- [x] **SALN-05**: Salary page showing compensation by age bracket (36+ earns $140K median)
- [x] **SALN-06**: Page detailing GTM Engineer bonus structures (51% receive bonus, 56% get 10-25% of base)
- [x] **SALN-07**: Page analyzing GTM Engineer equity compensation (68% no meaningful equity, by funding stage)
- [x] **SALN-08**: Salary comparison page for US vs global markets (US $135K vs non-US $75K)
- [x] **SALN-09**: Page comparing posted salaries vs actual reported salaries (posted $150K vs reported $135K)
- [x] **SALN-10**: Agency fee guide page ($1K-$33K/mo range, median $5K-$8K/mo, pricing models)
- [x] **SALN-11**: Agency fee comparison page by region (US premium, APAC $3K, MEA $4K)
- [x] **SALN-12**: Salary comparison page for seed stage vs enterprise (equity trade-offs)

### Career & Breaking-In Pages

- [x] **CAREER-01**: "How to Become a GTM Engineer in 2026" guide (self-taught 121/228, top paths)
- [x] **CAREER-02**: Career path page on operator vs engineer bifurcation (bimodal coding, $45K gap)
- [x] **CAREER-03**: "Is GTM Engineering a Real Career?" page (5,205% surge, $135K median)
- [x] **CAREER-04**: Job market analysis page (63 to 3,342 postings, monthly breakdown)
- [x] **CAREER-05**: How GTMEs got their jobs page (self-taught, agency, freelance breakdown)
- [x] **CAREER-06**: Work-life balance page (60% work 40-60 hrs, 23% work 60+)
- [x] **CAREER-07**: Demographics page (median age 25, Gen Z, 32 countries)
- [x] **CAREER-08**: "GTM Engineer vs RevOps: The Convergence" page (9.6% predict convergence)
- [x] **CAREER-09**: "Do You Need to Code?" page (bimodal distribution, $45K premium)
- [x] **CAREER-10**: Reporting structure page (Sales and Marketing most common)
- [x] **CAREER-11**: Impact measurement page (most tie to measurable pipeline)
- [x] **CAREER-12**: Skills gap page (Clay, HubSpot, Salesforce, Python, SQL from postings)

### Tool Pages

- [ ] **TOOL-01**: "GTM Engineer Tech Stack: 2026 Benchmark" page (full tooling adoption data)
- [ ] **TOOL-02**: Clay deep-dive page (84% adoption, 96% agencies, most loved AND most frustrating)
- [ ] **TOOL-03**: CRM adoption page (Salesforce/HubSpot 92%)
- [ ] **TOOL-04**: AI coding tools page (Cursor & Claude Code 71% adoption)
- [ ] **TOOL-05**: n8n adoption page (54% adoption, agency vs in-house usage)
- [ ] **TOOL-06**: Tool frustrations page (integration, UX, docs as top complaints)
- [ ] **TOOL-07**: "Most Exciting GTM Tools in 2026" page (Claude 39, Cursor 11, n8n 8)
- [ ] **TOOL-08**: Unify analysis page (8.8% adoption despite positioning)
- [ ] **TOOL-09**: Annual tool spend page (US vs non-US, 55% agencies $5-25K)
- [ ] **TOOL-10**: ZoomInfo vs Apollo for GTM Engineers (65% adoption)
- [ ] **TOOL-11**: Tool wishlist page (all-in-one outbound #1, AI SDR requested)
- [ ] **TOOL-12**: Python for GTM Engineers page (coding skill data, salary impact)
- [ ] **TOOL-13**: SQL for GTM Engineers page (job posting frequency, use cases)
- [ ] **TOOL-14**: Zapier vs n8n for GTM Engineers (adoption, cost, agency preferences)
- [ ] **TOOL-15**: HubSpot vs Salesforce for GTM Engineers (92% CRM, by company size)
- [ ] **TOOL-16**: JavaScript for GTM Engineers page (posting frequency, vs Python)

### Agency & Freelance Pages

- [ ] **AGENCY-01**: Agency Pricing Guide ($5K-$8K/mo median, $1K-$33K range)
- [ ] **AGENCY-02**: "How to Start a GTM Engineering Agency" guide (30% are agency/claygency)
- [ ] **AGENCY-03**: Agency vs freelance revenue comparison (67 vs 30 respondents)
- [ ] **AGENCY-04**: Client retention page (44% 3-6 month, 24% 6-12 month engagements)
- [ ] **AGENCY-05**: Client count analysis (47% <5 clients, 33% 5-10)
- [ ] **AGENCY-06**: Pricing models page (monthly most common, hybrid, project, pay-per-outcome)
- [ ] **AGENCY-07**: Agency fees by region (US, APAC $3K, MEA $4K, Europe, LATAM)
- [ ] **AGENCY-08**: Deliverability practices page (89.7% domain rotation)

### Job Market Pages

- [ ] **JOBMKT-01**: Job growth page (5,205% surge, 63 to 3,342 postings)
- [ ] **JOBMKT-02**: Jobs by country page (US 25.7%, India 17.4%, Spain 15.3%, UK 7.7%)
- [ ] **JOBMKT-03**: Posted vs actual salary gap page ($150K vs $135K)
- [ ] **JOBMKT-04**: Top skills in postings page (Clay, HubSpot, Salesforce, Python, SQL)
- [ ] **JOBMKT-05**: Monthly hiring trends page (Jan-Dec 2025, Dec peaked 624)
- [ ] **JOBMKT-06**: Salary bands by location from postings (US widest: $128K-$175K)
- [ ] **JOBMKT-07**: India GTM Engineering market page (17.4%, 2nd largest)
- [ ] **JOBMKT-08**: Spain/Europe GTM Engineer market page (15.3%, 3rd globally)

### Benchmark & Statistics Pages

- [ ] **BENCH-01**: "50 Key Numbers" roundup page (all top stats from report)
- [ ] **BENCH-02**: Demographics deep-dive (228 respondents, 32 countries, distributions)
- [ ] **BENCH-03**: Report summary and analysis page (editorial commentary)
- [ ] **BENCH-04**: "Operator vs Engineer Divide" analysis (bimodal, salary gap, bifurcation)
- [ ] **BENCH-05**: Bottlenecks page (25% bandwidth, 17% tool complexity, 8% buy-in)
- [ ] **BENCH-06**: "Does Your Company Understand GTM Engineering?" (45% yes, 9% partially)
- [ ] **BENCH-07**: Learning resources page (LinkedIn 174, YouTube, Peers)
- [ ] **BENCH-08**: Headcount trends page (majority plan to grow in 2026)
- [ ] **BENCH-09**: Future of GTM Engineering page (AI, RevOps convergence, agents, consolidation)

### Comparison Pages

- [ ] **COMP-01**: "GTM Engineer vs GTM Operator: The $45K Difference" page
- [ ] **COMP-02**: In-house vs agency comparison (56% in-house vs 30% agency)
- [ ] **COMP-03**: GTM Engineer vs AI SDR page (replacement predictions)
- [ ] **COMP-04**: US vs Europe vs APAC salary comparison (regional data)
- [ ] **COMP-05**: Seed stage vs Series B compensation comparison
- [ ] **COMP-06**: Technical vs low-code operator comparison (skills, salary, trajectory)

### Long-Tail Blog Articles

- [ ] **BLOG-01**: "Why 68% of GTM Engineers Have No Meaningful Equity" article
- [ ] **BLOG-02**: "The $45K Coding Premium" article
- [ ] **BLOG-03**: "60% of In-House GTMEs Work 40-60 Hours a Week" article
- [ ] **BLOG-04**: "GTM Engineering Is a Gen Z Function" article (median age 25)
- [ ] **BLOG-05**: "Why Clay Is Both the Most Loved and Most Hated GTM Tool" article
- [ ] **BLOG-06**: "LATAM and APAC Are Agency-Driven GTM Markets" article
- [ ] **BLOG-07**: "The GTM Engineer Title Is Getting Watered Down" article
- [ ] **BLOG-08**: "Pre-Seed GTM Engineers Get the Best Equity Deals" article
- [ ] **BLOG-09**: "Most GTM Engineers Are Self-Taught" article (121/228)
- [ ] **BLOG-10**: "91% of GTM Engineers Do Lead Gen (But That's Not All)" article
- [ ] **BLOG-11**: "The All-in-One Outbound Tool Doesn't Exist Yet" article
- [ ] **BLOG-12**: "GTM Engineer Bonus Data: 51% Get One" article
- [ ] **BLOG-13**: "December 2025: The Month GTM Engineering Exploded" article
- [ ] **BLOG-14**: "Why Mid-Size Companies Pay GTMEs the Most" article

### Content Quality & SEO

- [ ] **QUAL2-01**: Every new page has unique title (50-60 chars), meta description (150-158 chars), canonical URL, OG/Twitter Card
- [ ] **QUAL2-02**: Every new page has BreadcrumbList JSON-LD schema
- [ ] **QUAL2-03**: Every new page has 3+ internal links beyond nav/footer
- [ ] **QUAL2-04**: Salary, career, tool, and benchmark pages have 1,200-2,000 words
- [ ] **QUAL2-05**: Blog articles have 1,500-2,500 words each
- [ ] **QUAL2-06**: Comparison and analysis pages include FAQ section (3-4 Q&A) with FAQPage JSON-LD
- [ ] **QUAL2-07**: No duplicate titles or meta descriptions across entire site
- [ ] **QUAL2-08**: All stat references cite State of GTME Report 2026 as source
- [ ] **QUAL2-09**: All pages follow writing standards (no em-dashes, no false reframes, no banned words)

## Future Requirements

### v2.1+ (Deferred)

- **FUTURE-01**: 30 individual tool review pages with deep reviews
- **FUTURE-02**: 8 tool category index pages
- **FUTURE-03**: 10 "Best for" roundup pages
- **FUTURE-04**: 10 alternatives pages
- **FUTURE-05**: 50 glossary term pages
- **FUTURE-06**: Job board page wired to scraper data

## Out of Scope

| Feature | Reason |
|---------|--------|
| Interactive data visualizations (charts) | Static site, no JS frameworks. Use HTML/CSS range bars. |
| User-generated comments | No backend. Static site only. |
| PDF download of report | Copyright belongs to OneGTM. Cite and link, don't redistribute. |
| Real-time job posting counts | Requires scraper integration (Wave 4). Use report point-in-time data. |
| Video content or podcasts | Text-first strategy. |
| Gated content beyond calculator | Keep most content free for SEO. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SALUP-01 | Phase 4 | Complete |
| SALUP-02 | Phase 4 | Complete |
| SALUP-03 | Phase 4 | Complete |
| SALN-01 | Phase 4 | Complete |
| SALN-02 | Phase 4 | Complete |
| SALN-03 | Phase 4 | Complete |
| SALN-04 | Phase 4 | Complete |
| SALN-05 | Phase 4 | Complete |
| SALN-06 | Phase 4 | Complete |
| SALN-07 | Phase 4 | Complete |
| SALN-08 | Phase 4 | Complete |
| SALN-09 | Phase 4 | Complete |
| SALN-10 | Phase 4 | Complete |
| SALN-11 | Phase 4 | Complete |
| SALN-12 | Phase 4 | Complete |
| CAREER-01 | Phase 5 | Complete |
| CAREER-02 | Phase 5 | Complete |
| CAREER-03 | Phase 5 | Complete |
| CAREER-04 | Phase 5 | Complete |
| CAREER-05 | Phase 5 | Complete |
| CAREER-06 | Phase 5 | Complete |
| CAREER-07 | Phase 5 | Complete |
| CAREER-08 | Phase 5 | Complete |
| CAREER-09 | Phase 5 | Complete |
| CAREER-10 | Phase 5 | Complete |
| CAREER-11 | Phase 5 | Complete |
| CAREER-12 | Phase 5 | Complete |
| AGENCY-01 | Phase 5 | Pending |
| AGENCY-02 | Phase 5 | Pending |
| AGENCY-03 | Phase 5 | Pending |
| AGENCY-04 | Phase 5 | Pending |
| AGENCY-05 | Phase 5 | Pending |
| AGENCY-06 | Phase 5 | Pending |
| AGENCY-07 | Phase 5 | Pending |
| AGENCY-08 | Phase 5 | Pending |
| JOBMKT-01 | Phase 5 | Pending |
| JOBMKT-02 | Phase 5 | Pending |
| JOBMKT-03 | Phase 5 | Pending |
| JOBMKT-04 | Phase 5 | Pending |
| JOBMKT-05 | Phase 5 | Pending |
| JOBMKT-06 | Phase 5 | Pending |
| JOBMKT-07 | Phase 5 | Pending |
| JOBMKT-08 | Phase 5 | Pending |
| TOOL-01 | Phase 6 | Pending |
| TOOL-02 | Phase 6 | Pending |
| TOOL-03 | Phase 6 | Pending |
| TOOL-04 | Phase 6 | Pending |
| TOOL-05 | Phase 6 | Pending |
| TOOL-06 | Phase 6 | Pending |
| TOOL-07 | Phase 6 | Pending |
| TOOL-08 | Phase 6 | Pending |
| TOOL-09 | Phase 6 | Pending |
| TOOL-10 | Phase 6 | Pending |
| TOOL-11 | Phase 6 | Pending |
| TOOL-12 | Phase 6 | Pending |
| TOOL-13 | Phase 6 | Pending |
| TOOL-14 | Phase 6 | Pending |
| TOOL-15 | Phase 6 | Pending |
| TOOL-16 | Phase 6 | Pending |
| BENCH-01 | Phase 6 | Pending |
| BENCH-02 | Phase 6 | Pending |
| BENCH-03 | Phase 6 | Pending |
| BENCH-04 | Phase 6 | Pending |
| BENCH-05 | Phase 6 | Pending |
| BENCH-06 | Phase 6 | Pending |
| BENCH-07 | Phase 6 | Pending |
| BENCH-08 | Phase 6 | Pending |
| BENCH-09 | Phase 6 | Pending |
| COMP-01 | Phase 7 | Pending |
| COMP-02 | Phase 7 | Pending |
| COMP-03 | Phase 7 | Pending |
| COMP-04 | Phase 7 | Pending |
| COMP-05 | Phase 7 | Pending |
| COMP-06 | Phase 7 | Pending |
| BLOG-01 | Phase 7 | Pending |
| BLOG-02 | Phase 7 | Pending |
| BLOG-03 | Phase 7 | Pending |
| BLOG-04 | Phase 7 | Pending |
| BLOG-05 | Phase 7 | Pending |
| BLOG-06 | Phase 7 | Pending |
| BLOG-07 | Phase 7 | Pending |
| BLOG-08 | Phase 7 | Pending |
| BLOG-09 | Phase 7 | Pending |
| BLOG-10 | Phase 7 | Pending |
| BLOG-11 | Phase 7 | Pending |
| BLOG-12 | Phase 7 | Pending |
| BLOG-13 | Phase 7 | Pending |
| BLOG-14 | Phase 7 | Pending |
| QUAL2-01 | Phase 7 | Pending |
| QUAL2-02 | Phase 7 | Pending |
| QUAL2-03 | Phase 7 | Pending |
| QUAL2-04 | Phase 7 | Pending |
| QUAL2-05 | Phase 7 | Pending |
| QUAL2-06 | Phase 7 | Pending |
| QUAL2-07 | Phase 7 | Pending |
| QUAL2-08 | Phase 7 | Pending |
| QUAL2-09 | Phase 7 | Pending |

**Coverage:**
- v2.0 requirements: 88 total (SALUP:3, SALN:12, CAREER:12, TOOL:16, AGENCY:8, JOBMKT:8, BENCH:9, COMP:6, BLOG:14, QUAL2:9)
- Mapped to phases: 88/88
- Phase 4: 15 (SALUP:3, SALN:12)
- Phase 5: 28 (CAREER:12, AGENCY:8, JOBMKT:8)
- Phase 6: 25 (TOOL:16, BENCH:9)
- Phase 7: 29 (COMP:6, BLOG:14, QUAL2:9)
- Unmapped: 0

---
*Requirements defined: 2026-03-13*
*Last updated: 2026-03-13 after roadmap creation*
