# GTME Pulse

## What This Is

An independent resource hub for GTM Engineers at gtmepulse.com. Vendor-neutral salary data, tool reviews and comparisons, career guides, glossary, job board, and weekly newsletter. Python static site generator following the therevopsreport.com model. All content attributed to Rome Thorndike.

## Core Value

GTM Engineers can find accurate, vendor-neutral salary benchmarks and career intelligence in one place, with data no competitor provides.

## Current Milestone: v2.0 State of GTME Content Wave

**Goal:** Build ~85 new data-backed content pages using the State of GTME Report 2026 (228 respondents, 3,342 job postings from OneGTM/Sentrion), replacing hardcoded benchmarks with real survey data and creating the definitive SEO-optimized resource for every GTM Engineering query.

**Data source:** "The State of GTME Report - 2026" by OneGTM (Garrett Wolfe, Alex Lindahl, Maja Voje) + Clay Job Data (224 postings via Sentrion). 228 respondents across 32 countries.

**Target content:**
- 12 new salary pages (coding premium, company size, funding stage, experience, age, bonus, equity, US vs global, posted vs actual, agency fees, agency fees by region, seed vs enterprise)
- Update existing 45 salary pages with real survey data ($135K median, not estimates)
- 12 career & breaking-in pages (how to become, career path, job market growth, demographics, work-life balance, coding requirements, reporting structure, skills gap)
- 16 tool pages (tech stack benchmark, Clay 84%, CRM 92%, AI coding 71%, n8n 54%, tool frustrations, most exciting tools, Unify 8.8%, tool spend, tool wishlist)
- 8 agency/freelance pages (pricing guide, how to start, revenue comparison, client retention, client count, pricing models, fees by region, domain rotation)
- 8 job market pages (5,205% growth, jobs by country, posted vs actual salary, top skills, monthly trends, salary bands by location, India boom, Spain market)
- 9 benchmark/state-of pages (50 key stats, demographics, report summary, operator vs engineer, bottlenecks, company understanding, learning resources, headcount trends, future predictions)
- 6 comparison pages (engineer vs operator, in-house vs agency, vs AI SDR, US vs Europe vs APAC, seed vs series B, technical vs low-code)
- 14 long-tail blog articles (equity problems, coding premium, work hours, Gen Z function, Clay love/hate, LATAM/APAC markets, title inflation, pre-seed equity, self-taught, responsibilities, all-in-one tool, bonus data, December 2025 explosion, mid-size company salary)

**Key data points to weave across all pages:**
- US in-house median: $135K (range $60K-$250K+)
- Non-US median: $75K
- Job posting median: $150K (224 listings)
- Coding premium: $45K (low-code ~$90K vs technical)
- 5,205% job posting surge (63 to 3,342 in 2025)
- Clay: 84% adoption (96% agencies)
- CRM: 92% adoption
- AI coding tools: 71% adoption
- 68% have no meaningful equity
- Median age: 25, Gen Z function
- 60% work 40-60 hrs/week
- Self-taught dominates (121/228)
- Agency fees: $5K-$8K/mo median

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Build system skeleton (3-file Python split: build.py, templates.py, nav_config.py)
- [ ] CSS architecture (tokens.css + components.css + styles.css)
- [ ] Homepage with hero, stats grid, section previews, newsletter CTA
- [ ] About page (Rome Thorndike bio, site mission)
- [ ] Newsletter page with fully wired Resend signup via Cloudflare Worker
- [ ] Privacy policy and Terms of service pages
- [ ] 404 error page
- [ ] Salary index page with aggregate stats and links to all breakdowns
- [ ] 4 salary-by-seniority pages (Junior, Mid, Senior, Lead/Staff)
- [ ] 15 salary-by-location pages (SF, NYC, Austin, Seattle, Boston, Denver, Chicago, LA, Miami, Atlanta, Portland, DC, Dallas, San Diego, Remote)
- [ ] 5 salary-by-company-stage pages (Seed, Series A, Series B, Growth, Enterprise)
- [ ] 10 salary-vs-comparison pages (GTM Engineer vs RevOps, Sales Ops, Growth Engineer, SDR, Solutions Engineer, Marketing Ops, Sales Engineer, Data Engineer, Product Manager, AE)
- [ ] Salary calculator page (email-gated full results)
- [ ] Salary methodology page
- [ ] Newsletter infrastructure (Cloudflare Worker + Resend Audiences integration)
- [ ] Auto-generated sitemap.xml, robots.txt, CNAME
- [ ] BreadcrumbList schema on all inner pages
- [ ] FAQPage schema on salary comparison and breakdown pages
- [ ] Organization + WebSite schema on homepage
- [ ] 3+ internal links per page beyond nav/footer
- [ ] Mobile-responsive design (375px, 768px, 1024px breakpoints)

### Out of Scope

- Tool review pages (30 tools) — Wave 2
- Tool comparison pages (20 matchups) — Wave 2
- Career guide pages (~15 pages) — Wave 3
- Glossary pages (50 terms) — Wave 3
- Job board page — Wave 4
- Insight articles — Wave 4
- Email generation + weekly send automation — Wave 4
- OG image auto-generation via Playwright — future enhancement
- Dark mode toggle UI — tokens.css has dark mode variables but no toggle needed for v1

## Context

**GTM Engineer** is a technical, hybrid B2B SaaS role that builds automated outbound/revenue systems using Clay, Apollo, AI APIs, and workflow automation. 205% YoY job posting growth (2024-2025). 3,000+ open roles. $132K-$250K salary range.

**Competitive landscape:** gtmengineerclub.com (5 stale posts), gtmehq.com (Clay template shop, mostly vaporware). Neither has salary data, tool comparisons, job board, or glossary. Wide open.

**Reference implementations:**
- therevopsreport.com (CRO Report) — salary page structure, newsletter worker pattern
- SultanOfSaaS — template architecture, 3-file build system, content module pattern

**Brand:** "Volt" direction. Light-mode dominant, #FF4F1F orange-red accent, Sora/Plus Jakarta Sans/Source Code Pro fonts. All brand assets (logos, favicons, tokens.css, OG template) already in project.

**Data source:** State of GTME Report 2026 (228 respondents, 32 countries) + Clay Job Data (3,342 postings via Sentrion). Salary benchmarks originally hardcoded in build.py for Wave 1, now being replaced with real survey data. Job board data will come from unified scraper (gtme audience, id=8, 21 search terms) in Wave 4.

**Newsletter:** "The GTME Pulse" via Resend + Cloudflare Worker. Signup form on site, automated Monday sends from scraper data (Wave 4).

**Monetization:** Tool affiliate links (Apollo 15-20%, Instantly 20-40%, Clay $50), newsletter sponsorships, job board paid listings, email-gated salary calculator.

## Constraints

- **Tech stack**: Python static site generator only. No frameworks, no JS build tools, no databases.
- **Hosting**: GitHub Pages + Cloudflare DNS. Output to `output/` directory.
- **Content depth**: No thin pages. Every salary page must have 1,200-2,000 words with stats, market context, comp drivers, FAQ, and related links.
- **Writing rules**: No em-dashes, no false reframes, no banned AI words (see CLAUDE.md), no spaces in stat numbers.
- **SEO**: Every page needs title (50-60 chars), description (150-158 chars), canonical URL, schema markup, and internal links.
- **Brand**: Must use tokens.css variables. Sora for headings, Plus Jakarta Sans for body, Source Code Pro for data/stats.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Hardcode salary data in build.py | No external data source yet; move to JSON when scraper data available | — Pending |
| 3-file Python split (build/templates/nav_config) | Proven pattern from SultanOfSaaS; easy to maintain at scale | — Pending |
| Resend + Cloudflare Worker for newsletter | Same stack as therevopsreport.com; Rome already has Resend account and Workers setup | — Pending |
| Wave ordering (salary first) | Salary data is the anchor differentiator; no competitor has it | — Pending |
| Email-gate salary calculator only | Keep most content free for SEO; gate the high-value interactive tool | — Pending |

| Use real State of GTME Report data | First-party survey data (n=228) is more credible than hardcoded estimates | — Pending |
| Cite "Source: State of GTM Engineering Report 2026" on all data pages | Establishes authority, makes pages the definitive reference | — Pending |

---
*Last updated: 2026-03-13 after milestone v2.0 initialization*
